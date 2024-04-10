from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from app.databases.postgresdb import query_users
from app.databases.postgresdb.schemas import UserSignUp
from sqlalchemy.orm import Session
from app.databases.postgresdb.database import get_db
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
from app.databases.postgresdb.authentication import (
    create_access_token,
    SESSION_COOKIE_NAME,
)
from dotenv import load_dotenv
from pathlib import Path
import os


directory_path = Path(__file__).parent
env_file_path = directory_path.parent / ".env"

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI, allow_insecure_http=True
)

router = APIRouter(prefix="/google")


@router.get("/login", tags=["Google SSO"])
async def google_login(request: Request):
    with google_sso:
        return await google_sso.get_login_redirect(
            params={"prompt": "consent", "access_type": "offline"}
        )


@router.get("/callback", tags=["Google SSO"])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Process login response from Google and return user info"""

    try:
        with google_sso:
            user = await google_sso.verify_and_process(request)
        user_stored = query_users.get_user(db, user.email, provider=user.provider)
        if not user_stored:
            user_to_add = UserSignUp(
                username=user.email,
                password=None,
                fullname=user.display_name,
                picture=user.picture,
            )
            user_stored = query_users.add_user(db, user_to_add, provider=user.provider)
        access_token = create_access_token(
            username=user_stored.username, provider=user.provider
        )
        response = RedirectResponse(
            url="/job-applications/", status_code=status.HTTP_302_FOUND
        )
        response.set_cookie(SESSION_COOKIE_NAME, access_token)
    except query_users.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
    return response
