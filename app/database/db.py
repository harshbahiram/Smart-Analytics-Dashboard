from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

if not Config.DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD is not set in .env"
    )

DATABASE_URL = (

    f"postgresql://"
    f"{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"

)
 
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()