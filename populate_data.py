import json
import random
from models import Base, Users, Groups
from database import MySQLDB


def populate_data(db, data):
    for group in data['groups']:
        print(group)
        new_group = Groups(name=group)
        db.add(new_group)
    db.commit()

    groups = db.query(Groups).all()
    
    for i, user in enumerate(data['users']):
        if i % 3 == 0:
            group = None  # None == don't join any groups
        else:
            group = random.choice(groups)
        new_user = Users(name=user, group=group)
        db.add(new_user)
    db.commit()

    print("Successfully populated data!")
    db.close()


if __name__ == "__main__":
    with open('example_data.json', 'r') as f:
        data = json.load(f)

    db_manager = MySQLDB()
    db_session = db_manager.SessionLocal()

    try:
        Base.metadata.create_all(bind=db_manager.engine)  # check if tables exist
        populate_data(db_session, data)
    finally:
        db_session.close()