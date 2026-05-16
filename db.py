from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://1YePifG77EB8tKx.root:3Czn4w7cOTBBFeul@gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com:4000/test"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": None
        }
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Connected to TiDB!")
    except Exception as e:
        print(f"Failed: {e}")