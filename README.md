# 🎓 EduInsight — Student Performance Analytics Dashboard

A simple, medium-level **Student Performance Analytics Dashboard** built for **Python for Data Science** using **Pandas, NumPy, Matplotlib, Plotly, and Streamlit**.

---

## 📌 Project Overview

EduInsight is an interactive exploratory data analysis (EDA) and student performance monitoring tool. It allows teachers and students to filter, inspect, and analyze student academic data without requiring any database setup or complex configurations.

---

## 🗂️ Project Structure (Just 3 Main Files!)

```text
EduInsight/
│
├── app.py               # Main Streamlit dashboard (EDA, KPIs, Matplotlib Charts, Directory)
├── generate_data.py     # Python script to generate the 500-student dataset
├── students_data.csv    # Pre-generated 500-student dataset
├── requirements.txt     # Python library dependencies
└── README.md            # Project guide and instructions
```

---

## ✨ Key Features

1. **Direct Access**: No login or password required — launches straight into the main dashboard.
2. **Pure Python (No SQL Required)**: Works directly with CSV data using Pandas and NumPy.
3. **500-Student Realistic Dataset**: Includes student ID, name, gender, department, semester, study hours, attendance, midterm/final marks, total marks, CGPA, grade, and pass/fail status.
4. **Interactive Filters**:
   - Filter by Department / Branch
   - Filter by Semester (1 to 8)
   - Filter by Gender
   - Attendance range slider
5. **Key KPI Cards**:
   - Total Students
   - Class Average Marks
   - Overall Pass Percentage
   - Average Attendance
   - Average CGPA
6. **Data Science Visualizations (Matplotlib & Plotly)**:
   - Grade Distribution Bar Chart
   - Pass vs. Fail Ratio Donut Chart
   - Average Marks by Department
   - Marks Distribution with Histogram (Matplotlib `plt.hist`)
   - Correlation Heatmap of academic metrics (Matplotlib `plt.imshow`)
   - Attendance vs. Total Marks Scatter Plot (Matplotlib `plt.scatter`)
   - Department-wise Marks Spread & Outliers (Matplotlib `plt.boxplot`)
7. **Student Directory & Search**:
   - Search by student name or ID
   - 🏆 Top 5 rank holders / toppers list
   - ⚠️ Low attendance warning list (< 75%)
8. **Statistical Summary & Export**:
   - Descriptive statistics table (`df.describe()`)
   - One-click export of filtered records to CSV

---

## 🧰 Tech Stack (Python for Data Science)

- **Streamlit**: Web dashboard framework
- **Pandas**: Data manipulation and filtering
- **NumPy**: Numerical operations
- **Matplotlib**: Statistical charts (Histogram, Boxplot, Scatter, Heatmap)
- **Plotly Express**: Interactive charts

---

## ▶️ How to Run

### Step 1: Install Dependencies
Open your terminal/command prompt in the `EduInsight` folder and run:

```bash
pip install -r requirements.txt
```

### Step 2: (Optional) Re-generate Dataset
The dataset `students_data.csv` is already included. If you ever want to generate a fresh dataset:

```bash
python generate_data.py
```

### Step 3: Launch the Dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.
