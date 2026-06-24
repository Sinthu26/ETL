import sqlite3

from src.db import SessionLocal
from src.models import Location, Skill, Posting, PostingSkill
from src.skills import match_skills, SKILL_TAXONOMY


SKILL_CATEGORY = {name: category
                  for category, names in SKILL_TAXONOMY.items()
                  for name in names}


def main():
    old = sqlite3.connect("data/canadalens.db")
    old.row_factory = sqlite3.Row
    session = SessionLocal()

    pairs = old.execute("SELECT DISTINCT city, province FROM postings").fetchall()
    for row in pairs:
        session.add(Location(city=row["city"], province=row["province"]))
    session.commit()
    print(f"A. inserted {len(pairs)} locations")

    found = set()
    for row in old.execute("SELECT job_title FROM postings"):
        for skill_name in match_skills(row["job_title"]):
            found.add(skill_name)
    for skill_name in found:
        session.add(Skill(name=skill_name, category=SKILL_CATEGORY[skill_name]))
    session.commit()
    print(f"B. inserted {len(found)} skills")

    location_id = {(loc.city, loc.province): loc.location_id
                   for loc in session.query(Location).all()}
    skill_id = {sk.name: sk.skill_id for sk in session.query(Skill).all()}

    count = 0
    for row in old.execute("SELECT * FROM postings"):
        session.add(Posting(
            posting_id=row["posting_id"],
            title=row["job_title"],
            salary_min=None,
            salary_max=row["salary_maximum"],
            has_salary=row["has_salary"],
            contract_time=None,
            date_first_seen=row["date_first_seen"],
            date_last_seen=row["date_last_seen"],
            expired_fast=row["expired_fast"],
            location_id=location_id[(row["city"], row["province"])],
            employer_id=None,
        ))
        count += 1
    session.commit()
    print(f"C. inserted {count} postings")

    links = 0
    for row in old.execute("SELECT posting_id, job_title FROM postings"):
        for skill_name in match_skills(row["job_title"]):
            session.add(PostingSkill(
                posting_id=row["posting_id"],
                skill_id=skill_id[skill_name],
            ))
            links += 1
    session.commit()
    print(f"D. inserted {links} posting_skills")

    session.close()
    old.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
