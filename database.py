from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# engine_url = "mysql+pymysql://root:1qaz2wsx@localhost:3306/lilee"  # for local tests
engine_url = "mysql+pymysql://root:1qaz2wsx@mysqlDB:3306/lilee"

engine = create_engine(engine_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
