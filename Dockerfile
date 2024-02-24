# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.10

# Set the working directory in the container
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the current directory contents into the container at /app
COPY ./ /src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
