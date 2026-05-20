from app.database.db import SessionLocal
from app.database.models import UploadedFile

def save_uploaded_file(
        filename,
        filepath,
        rows,
        columns
):
    
    db = SessionLocal()

    try:
        file_record = UploadedFile(
            filename = filename,
            filepath=filepath,
            rows=rows,
            columns=columns
        )

        db.add(file_record)
        db.commit()

    finally:
        db.close()