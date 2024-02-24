import spacy
import nltk
from spacy.matcher import PhraseMatcher

# load default skills data base
from skillNer.general_params import SKILL_DB

# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init skill extractor
nlp = spacy.load("en_core_web_md")
nltk.download("wordnet")
nltk.download("omw-1.4")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
# skill_extractor = None
