import re

SKILL_TAXONOMY = {
    "data_roles": ["data analyst", "data engineer", "data scientist", "business analyst", "analytics"],
    "software_roles": ["software developer", "software engineer", "developer", "programmer", "full stack"],
    "infrastructure": ["devops", "cloud engineer", "systems administrator", "network engineer", "site reliability"],
    "management": ["project manager", "product manager", "scrum master", "team lead", "it manager"],
    "support": ["technical support", "help desk", "it support", "systems analyst", "qa analyst"],
}

ALL_SKILLS = [skill for skills in SKILL_TAXONOMY.values() for skill in skills]

def match_skills(text):
    """
    * Takes a string as input
    * Converts it to lowercase
    * Loops through ALL_SKILLS using regex with word boundaries
    * Returns a list of matched skills
    """
    if not text:
        return []
    
    text = text.lower()
    found = []
    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return found