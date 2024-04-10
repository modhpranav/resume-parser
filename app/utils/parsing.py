import os
import re
import json
import logging

from pdfminer.high_level import extract_text
from app import nlp, skill_extractor, skillList
from rapidfuzz import process, fuzz
from datetime import datetime
from app.utils.services import Service


class Parser:
    def __init__(self):
        self.skills_path = {
            "jd": os.getenv("JD_SKILLS_STORAGE_PATH"),
            "resume": os.getenv("RESUME_SKILLS_STORAGE_PATH"),
        }

    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        # Extract text from PDF
        text = extract_text(pdf_file)
        return text.lower()

    def extract_skills(self, text, skill_type):
        text = text.lower()
        data_json = Service.load_skilljson(self.skills_path[skill_type])
        text_hash = Service.create_hash(text)
        skills = data_json.get(text_hash, None)
        if skills:
            return skills
        else:
            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            annotations = skill_extractor.annotate(text)
            skills = [
                x["doc_node_value"]
                for x in annotations["results"]["full_matches"]
                if len(x["doc_node_value"]) > 1
            ]
            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            text = text.split(",")
            for sentence in text:
                sentence = sentence.split("\n")
                for line in sentence:
                    if line and len(line) > 3:
                        data = TextProcessing(line).run()
                        skills.extend(data)
            logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            logging.info(set(skills))
            skills = Service.short_skill_filter(skills)
            data_json[text_hash] = list(set(skills))
            with open(self.skills_path[skill_type], "w") as file:
                json.dump(data_json, file, indent=4)
            return skills


class TextProcessing:
    def __init__(self, line):
        self.line = line
        self.text = None

    def spacy_processing(self):
        doc = nlp(self.line)

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
        self.text = re.sub(r"\S+@\S+", "", text)

    def fuzzy_matching(self):
        skills = []
        for keyword in skillList:
            match = process.extractOne(
                keyword, [self.text], scorer=fuzz.WRatio, score_cutoff=95
            )
            if match:
                skills.append(keyword)
            for word in self.text.split(" "):
                if fuzz.WRatio(keyword, word) > 95:
                    skills.append(keyword)
        return skills

    def run(self):
        self.spacy_processing()
        return self.fuzzy_matching()
