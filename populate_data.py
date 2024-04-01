from models import Base, Users, Groups
from database import MySQLDB
import random

# 20 groups
# 100 users
data = {
    'groups': [
        "Basketball", "Math", "Literature", "Science", "Music",
        "Art", "History", "Technology", "Chess", "Programming",
        "Hiking", "Photography", "Cooking", "Travel", "Language",
        "Cinema", "Theatre", "Fitness", "Yoga", "Meditation"
    ],
    'users': [
    "Olivia Smith", "Noah Johnson", "Emma Williams", "Liam Brown", "Ava Jones",
    "Sophia Garcia", "Isabella Miller", "Mia Davis", "Charlotte Rodriguez", "Amelia Martinez",
    "Harper Hernandez", "Evelyn Lopez", "Abigail Gonzalez", "Ella Wilson", "Elizabeth Anderson",
    "Camila Thomas", "Luna Moore", "Sofia Taylor", "Avery Jackson", "Mila White",
    "Scarlett Lee", "Emily Harris", "Aria Clark", "Madison Lewis", "Layla Walker",
    "Chloe Hall", "Ellie Young", "Lily Allen", "Zoey King", "Grace Wright",
    "Victoria Scott", "Stella Green", "Hazel Adams", "Natalie Baker", "Zoe Hill",
    "Riley Nelson", "Penelope Carter", "Leah Mitchell", "Savannah Perez", "Aubrey Roberts",
    "Brooklyn Collins", "Lucy Ramirez", "Aaliyah Flores", "Anna Stewart", "Samantha Sanchez",
    "Isla Morris", "Delilah Rogers", "Addison Reed", "Nora Cook", "Eliana Bailey",
    "Violet Rivera", "Hannah Cooper", "Lillian Richardson", "Zoe Cox", "Charlotte Brooks",
    "Layla Edwards", "Ruby Ward", "Sofia Coleman", "Josephine Jenkins", "Sarah Kim",
    "Peyton Long", "Claire Sanders", "Ivy Bell", "Isabel Murphy", "Ariana Price",
    "Elena Howard", "Gabriella Ward", "Alice Perry", "Sadie Powell", "Hailey Patterson",
    "Eva Hughes", "Emilia Grant", "Caroline Ross", "Eleanor Myers", "Kennedy Martin",
    "Madelyn Foster", "Kinsley James", "Allison Reed", "Maya Kelley", "Sarah Snyder",
    "Adalyn Hoffman", "Arianna Russell", "Elena Ortiz", "Melanie Wood", "Lyla Fisher",
    "Jasmine Roberts", "Lilly Dixon", "Adaline Marshall", "Daisy Wells", "Reagan Richardson"
    ]
}


def populate_data(db_session, data):
    for group in data['groups']:
        new_group = Groups(name=group)
        db_session.add(new_group)
    db_session.commit()

    groups = db_session.query(Groups).all()
    
    for i, user in enumerate(data['users']):
        if i % 5 == 0:
            group = None  # None == don't join any groups
        else:    
            group = random.choice(groups)
        new_user = Users(name=user, group=group)
        db_session.add(new_user)
    db_session.commit()

    print("Successfully populated data!")
    db_session.close()

if __name__ == "__main__":
    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()
    try:
        Base.metadata.create_all(bind=db_manager.engine)  # check if tables exist
        populate_data(db_session, data)
    finally:
        db_session.close()