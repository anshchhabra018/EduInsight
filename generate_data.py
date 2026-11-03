"""
generate_data.py
----------------
Generates a realistic dataset of 500 students and saves it to 'students_data.csv'.
Created for Python for Data Science mini project.
"""

import random
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker('en_IN')
Faker.seed(42)
random.seed(42)
np.random.seed(42)

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics & Comm.",
    "Mechanical Engg.",
    "Civil Engg."
]
SEMESTERS = [f"Semester {i}" for i in range(1, 9)]
GENDERS = ["Male", "Female"]

def get_grade_and_result(total_marks):
    if total_marks >= 90:
        return "A+", "Pass", 10.0
    elif total_marks >= 80:
        return "A", "Pass", 9.0
    elif total_marks >= 70:
        return "B+", "Pass", 8.0
    elif total_marks >= 60:
        return "B", "Pass", 7.0
    elif total_marks >= 50:
        return "C", "Pass", 6.0
    elif total_marks >= 40:
        return "D", "Pass", 5.0
    else:
        return "F", "Fail", 0.0

def generate_students(num_students=500):
    records = []
    
    for i in range(1, num_students + 1):
        student_id = f"STU{1000 + i}"
        gender = random.choice(GENDERS)
        name = fake.name_male() if gender == "Male" else fake.name_female()
        age = random.randint(18, 23)
        dept = random.choice(DEPARTMENTS)
        semester = random.choice(SEMESTERS)
        
        # Correlated realistic values:
        # More study hours and higher attendance generally correlate with better marks
        study_hours = round(float(np.random.normal(18, 6)), 1)
        study_hours = max(4.0, min(38.0, study_hours))
        
        attendance = round(float(np.random.normal(76, 12)), 1)
        attendance = max(45.0, min(99.0, attendance))
        
        # Base ability influenced slightly by attendance and study hours
        perf_factor = (study_hours / 38.0) * 0.45 + (attendance / 100.0) * 0.45 + random.uniform(-0.1, 0.1)
        
        midterm = int(np.clip(perf_factor * 50 + np.random.normal(0, 5), 10, 50))
        final = int(np.clip(perf_factor * 50 + np.random.normal(0, 5), 12, 50))
        total_marks = midterm + final
        
        grade, result, base_cgpa = get_grade_and_result(total_marks)
        # CGPA roughly aligns with total_marks / 10 with minor noise
        cgpa = round(min(10.0, max(3.5, (total_marks / 10.0) + random.uniform(-0.3, 0.3))), 2)
        if result == "Fail":
            cgpa = min(cgpa, 4.5)
            
        records.append({
            "Student_ID": student_id,
            "Name": name,
            "Gender": gender,
            "Age": age,
            "Department": dept,
            "Semester": semester,
            "Study_Hours_Per_Week": study_hours,
            "Attendance_Pct": attendance,
            "Midterm_Marks": midterm,
            "Final_Marks": final,
            "Total_Marks": total_marks,
            "CGPA": cgpa,
            "Grade": grade,
            "Result": result
        })
        
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_students(500)
    output_path = "students_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} student records in '{output_path}'!")
    print(df.head())
