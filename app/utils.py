import re
import hashlib
import json
import os
from pdfminer.high_level import extract_text
from app import nlp, skill_extractor, skillList
from rapidfuzz import process, fuzz
from datetime import datetime

JD_SKILLS_STORAGE_PATH = "app/config/jdskills.json"
RESUME_SKILLS_STORAGE_PATH = "app/config/resumeskills.json"

skills_path = {
    "jd": JD_SKILLS_STORAGE_PATH,
    "resume": RESUME_SKILLS_STORAGE_PATH
}

def create_hash(text: str, algorithm='sha256') -> str:
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode('utf-8'))
    print(hasher.hexdigest())
    return hasher.hexdigest()

def load_skilljson(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

async def extract_text_from_pdf(pdf_file) -> str:
    # Extract text from PDF
    text = extract_text(pdf_file)
    return text.lower()


async def get_insights(text, job_description) -> dict:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Extract entities from the job description
    jd_skills = await extract_skills(job_description, "jd")

    # Extract entities from the resume
    resume_skills = await extract_skills(text, "resume")

    matching_skills = set(resume_skills).intersection(set(jd_skills))

    unmatched_skills = set(jd_skills).difference(set(resume_skills))

    match_percentage = (
        str(round((len(matching_skills) / len(jd_skills) * 100), 2)) + "%"
    )

    # Check for security clearance and sponsorship mentions
    clearance_lines = [
        line.strip() + "."
        for line in job_description.split(".")
        if "clearance" in line.lower()
    ]
    sponsorship_lines = [
        line.strip() + "."
        for line in job_description.split(".")
        if "sponsorship" in line.lower()
    ]

    insights = {
        "total_resume_skills": len(resume_skills),
        "total_jd_skills": len(jd_skills),
        "matching_skills": list(matching_skills),
        "unmatched_skills": list(unmatched_skills),
        "total_unmatched_skills": len(unmatched_skills),
        "match_percentage": match_percentage,
        "clearance_information": (
            clearance_lines
            if len(clearance_lines) > 0
            else "Clearance Information Unknown"
        ),
        "sponsorship_information": (
            sponsorship_lines
            if len(sponsorship_lines) > 0
            else "Sponsorship Information Unknown"
        ),
        "resume_skills": list(resume_skills),
        "jd_skills": list(jd_skills),
        "clearance_bool": len(clearance_lines) > 0,
        "sponsorship_bool": len(sponsorship_lines) > 0,
    }

    return insights

def spacy_processing(line):
    doc = nlp(line)

    tokens = [
        token
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
        and token.ent_type_
        not in ["PERSON", "ORG", "GPE", "LOC", "DATE", "EMAIL", "PHONE_NUM"]
    ]

    ent_type = {}
    for token in tokens:
        ent_type[token.ent_type_] = ent_type.get(token.ent_type_, 0) + 1

    # Reconstruct the cleaned text
    text = " ".join(token.text for token in tokens)
    text = re.sub(r"\S+@\S+", "", text)
    return text

def fuzzy_matching(text):
    skills = []
    for keyword in skillList:
        match = process.extractOne(keyword, [text], scorer=fuzz.WRatio, score_cutoff=95)
        if match:
            skills.append(keyword)
        for word in text.split(' '):
            if fuzz.WRatio(keyword, word) > 95:
                skills.append(keyword)
    return skills

def short_skill_filter(full_matchskills):
    full_matchskills = list(set(full_matchskills))
    sorted_keywords = sorted(full_matchskills, key=len, reverse=True)
    
    filtered_keywords = set()
    for keyword in sorted_keywords:
        if not any(keyword in other_keyword for other_keyword in filtered_keywords if keyword != other_keyword):
            filtered_keywords.add(keyword)
            
    return list(filtered_keywords)

async def extract_skills(text, skill_type):
    text = text.lower()
    data_json = load_skilljson(skills_path[skill_type])
    text_hash = create_hash(text)
    skills = data_json.get(text_hash, None)
    if skills:
        return skills
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        annotations = skill_extractor.annotate(text)
        skills = [
            x["doc_node_value"]
            for x in annotations["results"]["full_matches"]
            if len(x["doc_node_value"]) > 1
        ]
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        text = text.split(',')
        for sentence in text:
            sentence = sentence.split('\n')
            for line in sentence:
                if line and len(line) > 3:
                    text = spacy_processing(line)
                    skills.extend(fuzzy_matching(text))
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(set(skills))
        skills = short_skill_filter(skills)
        data_json[text_hash] = list(set(skills))
        with open(skills_path[skill_type], 'w') as file:
            json.dump(data_json, file, indent=4)
        return skills
