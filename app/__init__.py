import spacy
import nltk
import os
import pandas as pd
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB

# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from dotenv import load_dotenv

load_dotenv()

# init skill extractor
nlp = spacy.load(os.getenv("SPACY_MODEL"))
nltk.download("wordnet")
nltk.download("omw-1.4")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

skill_csv = pd.read_csv("app/config/Skills.csv")
skill_csv["Skillset"] = skill_csv["Skillset"].apply(lambda x: x.lower())

moreskill_csv = pd.read_csv("app/config/suggestedSkills.csv")
full_list = (
    pd.concat([moreskill_csv[col] for col in moreskill_csv], ignore_index=True)
    .dropna()
    .apply(lambda x: x.lower())
    .tolist()
)


skillList = set(list(skill_csv["Skillset"]) + full_list)
