import logging

from app.utils.parsing import Parser

class InsightAnalysis:
    def __init__(self, text, job_description):
        self.text = text
        self.job_description = job_description
        self.data = {}
    
    def get_minor_attributes(self):
        
        # Check for security clearance and sponsorship mentions
        self.data["clearance_lines"] = [
            line.strip() + "."
            for line in self.job_description.split(".")
            if "clearance" in line.lower()
        ]
        self.data["sponsorship_lines"] = [
            line.strip() + "."
            for line in self.job_description.split(".")
            if "sponsorship" in line.lower()
        ]
    
    def get_major_attributes(self):
        
        # Extract entities from the resume
        self.data["jd_skills"] = Parser().extract_skills(self.job_description, "jd")

        self.data["resume_skills"] = Parser().extract_skills(self.text, "resume")

        self.data["matching_skills"] = set(self.data["resume_skills"]).intersection(set(self.data["jd_skills"]))

        self.data["unmatched_skills"] = set(self.data["jd_skills"]).difference(set(self.data["resume_skills"]))

        try:
            self.data["match_percentage"] = (
                str(round((len(self.data["matching_skills"]) / len(self.data["jd_skills"]) * 100), 2)) + "%"
            )
        except ZeroDivisionError:
            logging.error("No skills found in the job description")
            self.data["match_percentage"] = "0%"

    def prepare_insights(self):

        insights = {
            "total_resume_skills": len(self.data["resume_skills"]),
            "total_jd_skills": len(self.data["jd_skills"]),
            "matching_skills": list(self.data["matching_skills"]),
            "unmatched_skills": list(self.data["unmatched_skills"]),
            "total_unmatched_skills": len(self.data["unmatched_skills"]),
            "match_percentage": self.data["match_percentage"],
            "clearance_information": (
                self.data["clearance_lines"]
                if len(self.data["clearance_lines"]) > 0
                else "Clearance Information Unknown"
            ),
            "sponsorship_information": (
                self.data["sponsorship_lines"]
                if len(self.data["sponsorship_lines"]) > 0
                else "Sponsorship Information Unknown"
            ),
            "resume_skills": list(self.data["resume_skills"]),
            "jd_skills": list(self.data["jd_skills"]),
            "clearance_bool": len(self.data["clearance_lines"]) > 0,
            "sponsorship_bool": len(self.data["sponsorship_lines"]) > 0,
        }

        return insights
    
    def analyze(self):
        self.get_minor_attributes()
        self.get_major_attributes()
        return self.prepare_insights()