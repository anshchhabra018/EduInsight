"""
🎓 EduInsight — Student Performance Analytics Dashboard
---------------------------------------------------------
A clean and intuitive Data Science dashboard built with Python,
Pandas, NumPy, Matplotlib, and Streamlit.

Course: Python for Data Science
Dataset: 500 Students (students_data.csv)
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduInsight | Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for clean modern look
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    .sub-title {
        font-size: 16px;
        color: #7f8c8d;
        margin-bottom: 24px;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 12px 18px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Load the 500-student dataset; generates it automatically if missing."""
    csv_file = "students_data.csv"
    if not os.path.exists(csv_file):
        from generate_data import generate_students
        df_gen = generate_students(500)
        df_gen.to_csv(csv_file, index=False)
    
    df = pd.read_csv(csv_file)
    return df

df = load_data()


# -----------------------------------------------------------------------------
# 3. SIDEBAR FILTERS (Pandas Data Slicing)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 Filter Records")

# Department Filter
departments = ["All"] + sorted(df["Department"].unique().tolist())
selected_dept = st.sidebar.selectbox("Department", departments)

# Semester Filter
semesters = ["All"] + sorted(df["Semester"].unique().tolist())
selected_sem = st.sidebar.selectbox("Semester", semesters)

# Gender Filter
genders = ["All"] + sorted(df["Gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)

# Attendance Range Slider
min_att, max_att = int(df["Attendance_Pct"].min()), int(df["Attendance_Pct"].max())
selected_attendance = st.sidebar.slider(
    "Attendance Range (%)",
    min_value=min_att,
    max_value=max_att,
    value=(min_att, max_att)
)

# Apply filters
filtered_df = df.copy()

if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Department"] == selected_dept]

if selected_sem != "All":
    filtered_df = filtered_df[filtered_df["Semester"] == selected_sem]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]

filtered_df = filtered_df[
    (filtered_df["Attendance_Pct"] >= selected_attendance[0]) &
    (filtered_df["Attendance_Pct"] <= selected_attendance[1])
]

st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df)}** of **{len(df)}** total students.")


# -----------------------------------------------------------------------------
# 4. DASHBOARD HEADER & KPIS
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🎓 EduInsight: Student Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Python for Data Science — Exploratory Data Analysis & Student Analytics</div>', unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No student records match the selected filter criteria. Please broaden your selection.")
    st.stop()

# Key Performance Indicator (KPI) Metrics
total_students = len(filtered_df)
avg_marks = round(filtered_df["Total_Marks"].mean(), 1)
avg_attendance = round(filtered_df["Attendance_Pct"].mean(), 1)
avg_cgpa = round(filtered_df["CGPA"].mean(), 2)
pass_count = (filtered_df["Result"] == "Pass").sum()
pass_rate = round((pass_count / total_students) * 100, 1)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("👥 Students", total_students)
kpi2.metric("📊 Avg Marks", f"{avg_marks} / 100")
kpi3.metric("🎯 Pass Rate", f"{pass_rate}%")
kpi4.metric("🕒 Avg Attendance", f"{avg_attendance}%")
kpi5.metric("⭐ Avg CGPA", avg_cgpa)

st.markdown("---")


# -----------------------------------------------------------------------------
# 5. DASHBOARD TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview Charts",
    "📈 Data Science EDA & Correlation",
    "🧑‍🎓 Student Directory & Toppers",
    "📋 Statistical Summary & Export"
])


# =============================================================================
# TAB 1: OVERVIEW CHARTS
# =============================================================================
with tab1:
    st.subheader("Distribution and Categorical Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Grade Distribution
        grade_order = ["A+", "A", "B+", "B", "C", "D", "F"]
        grade_counts = filtered_df["Grade"].value_counts().reindex(grade_order, fill_value=0).reset_index()
        grade_counts.columns = ["Grade", "Count"]
        
        fig_grade = px.bar(
            grade_counts,
            x="Grade",
            y="Count",
            color="Grade",
            text="Count",
            title="Distribution of Grades",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_grade.update_traces(textposition='outside')
        fig_grade.update_layout(showlegend=False, template="plotly_white")
        st.plotly_chart(fig_grade, use_container_width=True)

    with col2:
        # Result (Pass vs Fail) Donut Chart
        res_counts = filtered_df["Result"].value_counts().reset_index()
        res_counts.columns = ["Result", "Count"]
        
        fig_res = px.pie(
            res_counts,
            names="Result",
            values="Count",
            hole=0.45,
            title="Overall Pass vs. Fail Ratio",
            color="Result",
            color_discrete_map={"Pass": "#2ecc71", "Fail": "#e74c3c"}
        )
        fig_res.update_traces(textinfo="percent+label")
        fig_res.update_layout(template="plotly_white")
        st.plotly_chart(fig_res, use_container_width=True)

    col3, col4 = st.columns(2)
    
    with col3:
        # Department Wise Average Marks
        dept_avg = filtered_df.groupby("Department")["Total_Marks"].mean().round(1).reset_index()
        dept_avg = dept_avg.sort_values(by="Total_Marks", ascending=False)
        
        fig_dept = px.bar(
            dept_avg,
            x="Total_Marks",
            y="Department",
            orientation="h",
            color="Total_Marks",
            color_continuous_scale="Viridis",
            title="Average Total Marks by Department"
        )
        fig_dept.update_layout(template="plotly_white")
        st.plotly_chart(fig_dept, use_container_width=True)

    with col4:
        # Gender Distribution
        gender_counts = filtered_df["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        
        fig_gender = px.pie(
            gender_counts,
            names="Gender",
            values="Count",
            title="Gender Representation",
            color_discrete_sequence=["#3498db", "#e84393"]
        )
        fig_gender.update_layout(template="plotly_white")
        st.plotly_chart(fig_gender, use_container_width=True)


# =============================================================================
# TAB 2: DATA SCIENCE EDA & CORRELATION (Pure Matplotlib)
# =============================================================================
with tab2:
    st.subheader("Exploratory Data Analysis (EDA) — Matplotlib")
    st.write("Statistical analysis and relationships between academic metrics using standard Matplotlib charts.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # 1. Total Marks Distribution (Matplotlib Histogram)
        fig_hist, ax_hist = plt.subplots(figsize=(6, 4.2))
        ax_hist.hist(filtered_df["Total_Marks"], bins=15, color="#4834d4", edgecolor="black", alpha=0.75)
        ax_hist.set_title("Total Marks Distribution (Histogram)", fontsize=11, fontweight='bold')
        ax_hist.set_xlabel("Total Marks (out of 100)")
        ax_hist.set_ylabel("Student Count")
        ax_hist.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig_hist)
        plt.close(fig_hist)
        
    with c2:
        # 2. Correlation Heatmap (Matplotlib imshow)
        numeric_cols = ["Attendance_Pct", "Study_Hours_Per_Week", "Midterm_Marks", "Final_Marks", "Total_Marks", "CGPA"]
        corr_matrix = filtered_df[numeric_cols].corr()
        short_labels = ["Attd", "Study", "Mid", "Final", "Total", "CGPA"]
        
        fig_corr, ax_corr = plt.subplots(figsize=(6, 4.2))
        cax = ax_corr.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
        fig_corr.colorbar(cax, ax=ax_corr, fraction=0.046, pad=0.04)
        
        ax_corr.set_xticks(range(len(short_labels)))
        ax_corr.set_yticks(range(len(short_labels)))
        ax_corr.set_xticklabels(short_labels, rotation=45, ha="right", fontsize=9)
        ax_corr.set_yticklabels(short_labels, fontsize=9)
        
        # Display numerical values inside each cell
        for i in range(len(short_labels)):
            for j in range(len(short_labels)):
                val = corr_matrix.iloc[i, j]
                text_color = "white" if abs(val) > 0.55 else "black"
                ax_corr.text(j, i, f"{val:.2f}", ha="center", va="center",
                             color=text_color, fontsize=9, fontweight="bold")
                
        ax_corr.set_title("Correlation Heatmap (Matplotlib)", fontsize=11, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_corr)
        plt.close(fig_corr)
        
    st.markdown("---")
    
    c3, c4 = st.columns(2)
    
    with c3:
        # 3. Attendance vs Marks (Matplotlib Scatter Plot)
        fig_scatter, ax_scatter = plt.subplots(figsize=(6, 4.2))
        pass_mask = filtered_df["Result"] == "Pass"
        
        ax_scatter.scatter(
            filtered_df.loc[pass_mask, "Attendance_Pct"],
            filtered_df.loc[pass_mask, "Total_Marks"],
            color="#00b894", alpha=0.7, label="Pass"
        )
        ax_scatter.scatter(
            filtered_df.loc[~pass_mask, "Attendance_Pct"],
            filtered_df.loc[~pass_mask, "Total_Marks"],
            color="#d63031", alpha=0.8, label="Fail"
        )
        ax_scatter.set_title("Attendance (%) vs. Total Marks (Scatter Plot)", fontsize=11, fontweight='bold')
        ax_scatter.set_xlabel("Attendance (%)")
        ax_scatter.set_ylabel("Total Marks")
        ax_scatter.legend()
        ax_scatter.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig_scatter)
        plt.close(fig_scatter)
        
    with c4:
        # 4. Box Plot: Marks Distribution across Departments (Matplotlib Boxplot)
        fig_box, ax_box = plt.subplots(figsize=(6, 4.2))
        depts = filtered_df["Department"].unique()
        dept_marks = [filtered_df[filtered_df["Department"] == d]["Total_Marks"].values for d in depts]
        
        # Short labels for cleaner display
        display_depts = [d[:11] + ".." if len(d) > 11 else d for d in depts]
        ax_box.boxplot(dept_marks, tick_labels=display_depts, patch_artist=True)
        ax_box.set_title("Marks Spread by Department (Boxplot)", fontsize=11, fontweight='bold')
        ax_box.set_ylabel("Total Marks")
        ax_box.tick_params(axis="x", rotation=25)
        ax_box.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig_box)
        plt.close(fig_box)


# =============================================================================
# TAB 3: STUDENT DIRECTORY & TOPPERS
# =============================================================================
with tab3:
    st.subheader("Search & Individual Student Records")
    
    # Search box
    search_query = st.text_input("🔎 Search by Student Name or Student ID", "")
    
    display_df = filtered_df.copy()
    if search_query:
        query = search_query.strip().lower()
        display_df = display_df[
            display_df["Name"].str.lower().str.contains(query) |
            display_df["Student_ID"].str.lower().str.contains(query)
        ]
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(display_df)} student records.")
    
    st.markdown("---")
    top_col, risk_col = st.columns(2)
    
    with top_col:
        st.markdown("##### 🏆 Top 5 Rank Holders (Toppers)")
        top_students = filtered_df.sort_values(by=["CGPA", "Total_Marks"], ascending=False).head(5)
        st.dataframe(
            top_students[["Student_ID", "Name", "Department", "Total_Marks", "CGPA", "Grade"]],
            use_container_width=True,
            hide_index=True
        )
        
    with risk_col:
        st.markdown("##### ⚠️ Attendance Warning List (< 75% Attendance)")
        low_attendance = filtered_df[filtered_df["Attendance_Pct"] < 75.0].sort_values(by="Attendance_Pct").head(5)
        if not low_attendance.empty:
            st.dataframe(
                low_attendance[["Student_ID", "Name", "Department", "Attendance_Pct", "Result"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("All selected students have attendance 75% or higher!")


# =============================================================================
# TAB 4: STATISTICAL SUMMARY & EXPORT
# =============================================================================
with tab4:
    st.subheader("Descriptive Statistics (Pandas describe)")
    st.write("Summary statistics for numerical features (Mean, Standard Deviation, Quartiles, Min, Max):")
    
    stats_df = filtered_df.describe().round(2).T
    st.dataframe(stats_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📥 Export Filtered Dataset")
    st.write("Download the currently filtered student records as a CSV file for reporting or further offline analysis.")
    
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data (CSV)",
        data=csv_bytes,
        file_name="eduinsight_filtered_students.csv",
        mime="text/csv",
        use_container_width=False
    )
