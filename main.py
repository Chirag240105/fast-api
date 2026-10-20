
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
import json

# BaseModel	- Defines the structure of incoming request bodies
# Field	- Adds validation constraints to model fields

app = FastAPI(title="Patient Management System API")


# ---------- Models ----------

class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int = Field(ge=0, le=120)
    gender: str
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    blood_group: Optional[str] = None


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[str] = None
    height_cm: Optional[float] = Field(default=None, gt=0)
    weight_kg: Optional[float] = Field(default=None, gt=0)
    blood_group: Optional[str] = None


# ---------- File operations ----------

def load_data():
    with open("patient.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

# json.dump(data, f) converts Python data into JSON and writes it to the file.
# indent=4 formats the output to make it readable.

def calculate_bmi(patient):
    height_m = patient["height_cm"] / 100
    patient["bmi"] = round(
        patient["weight_kg"] / (height_m ** 2), 2
    )


# ---------- Basic routes ----------

@app.get("/")
def rootAPI():
    return {"Message": "Patient management system API"}


@app.get("/about")
def about():
    return {
        "Message": "API to manage patient records"
    }


@app.get("/view")
def view():
    return load_data()


# ---------- GET: All patients + query parameters ----------

@app.get("/patients")  #http://localhost:8000/patients??age_min=25&age_max=40&gender=male&max_bmi=25
def get_patients(
    age_min: Optional[int] = Query(default=None, ge=0),
    age_max: Optional[int] = Query(default=None, ge=0),
    gender: Optional[str] = None,
    max_bmi: Optional[float] = Query(default=None, gt=0)
):
    data = load_data()
    patients = data["patients"]

    if age_min is not None:
        patients = [
            p for p in patients if p["age"] >= age_min
        ]

    if age_max is not None:
        patients = [
            p for p in patients if p["age"] <= age_max
        ]

    if gender is not None:
        patients = [
            p for p in patients
            if p["gender"].lower() == gender.lower()
        ]

    if max_bmi is not None:
        patients = [
            p for p in patients
            if p.get("bmi") is not None
            and p["bmi"] <= max_bmi
        ]

    return {
        "count": len(patients),
        "patients": patients
    }


# ---------- GET: One patient ----------

@app.get("/patient/{patient_id}")
def patient_info(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P001"
    )
):
    data = load_data()

    for patient in data["patients"]:
        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient ID not found"
    )


# ---------- POST: Add a patient ----------

@app.post("/patient", status_code=201)
def add_patient(patient: PatientCreate):
    data = load_data()

    for existing in data["patients"]:
        if existing["patient_id"] == patient.patient_id:
            raise HTTPException(
                status_code=409,
                detail="Patient ID already exists"
            )

    new_patient = patient.model_dump()
    calculate_bmi(new_patient)

    data["patients"].append(new_patient)
    save_data(data)

    return {
        "message": "Patient added successfully",
        "patient": new_patient
    }


# ---------- PUT: Update a patient ----------

@app.put("/patient/{patient_id}")
def update_patient(
    patient_id: str,
    updates: PatientUpdate
):
    data = load_data()

    for patient in data["patients"]:
        if patient["patient_id"] == patient_id:

            changes = updates.model_dump(exclude_unset=True)

            patient.update(changes)

            if "height_cm" in changes or "weight_kg" in changes:
                calculate_bmi(patient)

            save_data(data)

            return {
                "message": "Patient updated successfully",
                "patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient ID not found"
    )


# ---------- DELETE: Remove a patient ----------

@app.delete("/patient/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    for index, patient in enumerate(data["patients"]):
        if patient["patient_id"] == patient_id:
            deleted_patient = data["patients"].pop(index)
            save_data(data)

            return {
                "message": "Patient deleted successfully",
                "patient": deleted_patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient ID not found"
    )
