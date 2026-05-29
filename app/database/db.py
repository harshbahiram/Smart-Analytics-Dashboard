from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import Config


DATABASE_URL = (

    f"postgresql://"
    f"{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"

)

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Please check your environment variables."
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