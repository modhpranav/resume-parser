# Resume Parser

## Overview
Resume Parser is a web application designed to streamline the recruitment process by extracting skills from PDF resumes and comparing them against job descriptions. This tool provides insights such as matched skills, the percentage of match, and unmatched skills, aiding recruiters in making informed decisions.

## Web URL
**[ResumeParser](http://13.233.142.200:8000/)**

## Features
- **Skill Extraction**: Automatically extracts skills from PDF resumes.
- **Skill Matching**: Compares extracted skills against job descriptions to identify skills required.
- **Insightful Analytics**: Provides detailed analytics, including matched/unmatched skills and the percentage of match.

## Requirements
This project is built using Python and FastAPI, and it's containerized with Docker. The following are major dependencies:
- FastAPI for the web framework.
- Spacy for natural language processing.
- pdfminer.six for PDF processing.

For a complete list of dependencies, refer to the `requirements.txt` file.

## Installation

### Prerequisites
- Docker and docker-compose
- Git (optional)

### Setup Instructions
1. **Clone the repository** (optional if you download the project as a zip file):
   ```
   git clone https://yourrepositorylink.com/resume-parser.git
   cd resume-parser
   ```
2. **Build the Docker container**:
   ```
   docker-compose build
   ```
3. **Run the application**:
   ```
   docker-compose up
   ```

## Usage

### Extracting Skills from Resume
1. Access the web application through your browser.
2. Upload a PDF resume.
3. View the extracted skills displayed on the web interface.

### Comparing Resume against Job Description
1. Upload a job description and a PDF resume.
2. The application will analyze the documents and display the matched skills, unmatched skills, and the percentage of match.

## Deployment
This application is deployed on EC2. For deploying your instance, follow the standard Heroku deployment steps, ensuring your Docker environment is properly set up for AWS EC2.

## Contributing
Contributions are welcome! Please fork the repository and open a pull request with your improvements.