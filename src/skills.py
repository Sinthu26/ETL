import re

SKILL_TAXONOMY = {
    "languages": ["python", "sql", "java", "javascript", "c++"],
    "data_tools": ["pandas", "numpy", "spark", "airflow"],
    "databases": ["postgresql", "mysql", "sqlite", "mongodb"],
    "cloud": ["azure", "aws", "docker", "kubernetes"],
    "bi_tools": ["tableau", "power bi", "excel", "looker"],
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