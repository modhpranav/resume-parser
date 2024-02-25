import re
import hashlib
import json
import os
from pdfminer.high_level import extract_text
from app import nlp, skill_extractor, skillList
from rapidfuzz import process, fuzz
from datetime import datetime





