from app.databases.mongodb.database import mongo_database
from app.databases.mongodb import schemas
from bson import ObjectId
from datetime import datetime, timedelta
import random
from app.databases.mongodb.schemas import JobStatus


def create_user_application(data: schemas.JobApplication):
    # Insert job application into MongoDB
    try:
        user_application_data = {
            "userid": data["userid"],
            "Company Name": data["company_name"],
            "Application Link": data["source"],
            "Application Date": data["date_applied"],
            "Job Title": data["jobtitle"],
            "Job Description": data["description"],
            "Status": data["status"],
        }
        user_application_collection = mongo_database["job_applications"]
        user_application_collection.insert_one(user_application_data)
        return {"status_code": 200, "message": "Job application created successfully"}
    except Exception as e:
        return {"status_code": 500, "message": str(e)}


def update_user_application_status(data: schemas.UpdateJobStatus):
    # Update job application status in MongoDB
    try:
        user_application_collection = mongo_database["job_applications"]
        query_res = user_application_collection.find_one({"_id": ObjectId(data["id"])})
        if not query_res:
            return {"status_code": 404, "message": "Job application not found"}
        user_application_collection.update_one(
            {"_id": ObjectId(data["id"])}, {"$set": {"Status": data["status"]}}
        )
        return {"status_code": 200, "message": "Job status updated successfully"}
    except Exception as e:
        return {"status_code": 500, "message": str(e)}


def generate_dummy_data(num_entries: int):
    dummy_data = []
    for _ in range(num_entries):
        userid = 1
        company_name = f"Company {random.randint(1, 100)}"
        source = f"https://example.com/{random.randint(1, 1000)}"
        date_applied = datetime.now() - timedelta(days=random.randint(1, 365))
        job_title = f"Job Title {random.randint(1, 100)}"
        description = f"Job Description {random.randint(1, 100)}"
        status = random.choice(list(JobStatus))

        user_application_data = {
            "userid": userid,
            "Company Name": company_name,
            "Application Link": source,
            "Application Date": date_applied,
            "Job Title": job_title,
            "Job Description": description,
            "Status": status,
        }
        dummy_data.append(user_application_data)

    return dummy_data


def insert_application(data: schemas.JobApplication):
    for user_application_data in data:
        user_application_collection = mongo_database["job_applications"]
        user_application_collection.insert_one(user_application_data)


# Generate 10 dummy data entries
# dummy_data = generate_dummy_data(50)
# insert_application(dummy_data)
