from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = "locations"
    
    location_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    province: Mapped[str]
    
    __table_args__ = (UniqueConstraint("city", "province"),)
    
class Employer(Base):
    __tablename__ = "employers"
    
    employer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
class Skill(Base):
    __tablename__ = "skills"
    
    skill_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[str]

class Posting(Base):
    __tablename__ = "postings"
    
    posting_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    salary_min: Mapped[float | None]
    salary_max: Mapped[float | None]
    has_salary: Mapped[int | None]
    contract_time: Mapped[str | None]
    date_first_seen: Mapped[str | None]
    date_last_seen: Mapped[str | None]
    expired_fast: Mapped[int] = mapped_column(default=0)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.location_id"))
    employer_id: Mapped[int | None] = mapped_column(ForeignKey("employers.employer_id"))
    
class PostingSkill(Base):
    __tablename__ = "posting_skills"
    posting_id: Mapped[str] = mapped_column(ForeignKey("postings.posting_id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.skill_id"), primary_key=True)
       