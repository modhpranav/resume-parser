import hashlib
import os
import json


class Service:

    @staticmethod
    def create_hash(text: str, algorithm=os.getenv("HASH_ALGO")) -> str:
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()

    @staticmethod
    def load_skilljson(file_path: str) -> dict:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def short_skill_filter(text):
        full_matchskills = list(set(text))
        sorted_keywords = sorted(full_matchskills, key=len, reverse=True)

        filtered_keywords = set()
        for keyword in sorted_keywords:
            if not any(
                keyword in other_keyword
                for other_keyword in filtered_keywords
                if keyword != other_keyword
            ):
                filtered_keywords.add(keyword)

        return list(filtered_keywords)
