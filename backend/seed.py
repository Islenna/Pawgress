from config.database import SessionLocal
from models.Category import Category
from models.Skill import Skill

# Seed data
categories = [
    {"name": "General", "description": "Foundational clinical and hospital tasks."},
    {"name": "Anesthesia", "description": "Sedation, monitoring, and maintenance."},
    {"name": "Surgery", "description": "Pre-, intra-, and post-operative duties."},
    {"name": "Emergency", "description": "Urgent care, triage, and stabilization."},
    {"name": "Oncology", "description": "Cancer therapy and chemo protocols."},
    {"name": "Dentistry", "description": "Oral procedures and maintenance."},
]

skills = [
    {"name": "IVC Placement", "description": "Peripheral venous access via aseptic technique.", "category": "General"},
    {"name": "Anesthetic Induction", "description": "Safely induce general anesthesia.", "category": "Anesthesia"},
    {"name": "Instrument Pack Prep", "description": "Clean, organize, and sterilize packs.", "category": "Surgery"},
    {"name": "Triage Patient", "description": "Assess incoming patients for urgency.", "category": "Emergency"},
    {"name": "Chemo Safety Protocols", "description": "Safely handle/administer chemo.", "category": "Oncology"},
    {"name": "Dental Charting", "description": "Document dental pathology accurately.", "category": "Dentistry"},
]

def seed():
    db = SessionLocal()
    category_objs = {}

    # Create categories if they don't already exist
    for cat in categories:
        existing = db.query(Category).filter_by(name=cat["name"]).first()
        if not existing:
            category_obj = Category(name=cat["name"], description=cat["description"])
            db.add(category_obj)
            db.commit()  # commit to get the ID
            category_objs[cat["name"]] = category_obj
        else:
            category_objs[cat["name"]] = existing

    # Create skills if they don't already exist
    for skill in skills:
        existing = db.query(Skill).filter_by(name=skill["name"]).first()
        if not existing:
            category = category_objs.get(skill["category"])
            if category:
                db_skill = Skill(
                    name=skill["name"],
                    description=skill["description"],
                    category_id=category.id
                )
                db.add(db_skill)

    db.commit()
    db.close()
    print("✅ Seed complete!")

if __name__ == "__main__":
    seed()
