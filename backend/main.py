from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from database import SessionLocal, engine
from models import Base, Report

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/report")
async def create_report(
    description: str = Form(...),
    location: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Secure filename
    ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    report = Report(
        description=description,
        location=location,
        image_path=file_path
    )

    db.add(report)
    db.commit()

    return {"message": "Report submitted successfully"}

    @app.get("/admin/reports")
def get_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).all()

    return reports


@app.put("/admin/update/{report_id}")
def update_status(report_id: int, status: str, db: Session = Depends(get_db)):

    report = db.query(Report).filter(Report.id == report_id).first()

    report.status = status
    db.commit()

    return {"message": "Status updated"}