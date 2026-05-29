from sqlalchemy import Column, DateTime, Integer, String

from datetime import datetime

from app.database.db import Base


class UploadedFile(Base):
    """Stores metasdata for uploaded files."""
    __tablename__ = "uploaded_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    filepath = Column(
        String,
        nullable=False
    )

    rows = Column(
        Integer,
        nullable=False
    )

    columns = Column(
        Integer,
        nullable=False
    )

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )