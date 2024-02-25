import re
from pdfminer.high_level import extract_text
from app import nlp, skill_extractor
from nltk.stem import WordNetLemmatizer


async def extract_text_from_pdf(pdf_file) -> str:
    # Extract text from PDF
    text = extract_text(pdf_file)
    return text


async def get_insights(text, job_description) -> dict:
    # Extract entities from the job description
    jd_skills = await extract_skills(job_description)

    # Extract entities from the resume
    resume_skills = await extract_skills(text)

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


async def extract_skills(text):
    doc = nlp(text.lower())

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

    # Remove numbers
    text = re.sub(r"\d+", "", text)
    annotations = skill_extractor.annotate(text)
    full_matchskills = [
        x["doc_node_value"]
        for x in annotations["results"]["full_matches"]
        if len(x["doc_node_value"]) > 1
    ]
    ngram_matchskills = [
        x["doc_node_value"]
        for x in annotations["results"]["ngram_scored"]
        if len(x["doc_node_value"]) > 1
    ]
    return await remove_redundancy(full_matchskills + ngram_matchskills)


async def remove_redundancy(words):
    lemmatizer = WordNetLemmatizer()

    # Lemmatize words to get their base form
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]

    # Handle repeated words (e.g., "docker docker" -> "docker")
    cleaned_words = [
        " ".join(sorted(set(word.split()), key=word.split().index))
        for word in lemmatized_words
    ]

    # Remove duplicates while preserving order
    seen = set()
    result = [word for word in cleaned_words if not (word in seen or seen.add(word))]
    return result
