# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.10

# Set the working directory in the container
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy entrypoint script
# COPY entrypoint.sh /usr/local/bin/

# Make entrypoint script executable
# RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script to be executed
# ENTRYPOINT ["entrypoint.sh"]

# Copy the current directory contents into the container at /app
COPY ./ /src

WORKDIR /src/app

CMD ["fastapi", "run"]
