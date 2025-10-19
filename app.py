import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CIIT GPA & CGPA Calculator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .gpa-display {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .grade-table {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .ciit-header {
        background: linear-gradient(135deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def calculate_gpa(marks, credit_hours):
    """Calculate GPA based on marks and credit hours using CIIT grading system"""
    total_credits = 0
    total_grade_points = 0
    
    for mark, credit in zip(marks, credit_hours):
        grade_point, grade = convert_to_grade_point(mark)
        total_grade_points += grade_point * credit
        total_credits += credit
    
    if total_credits == 0:
        return 0, 0
    gpa = total_grade_points / total_credits
    return gpa, total_credits

def convert_to_grade_point(mark):
    """Convert marks to grade points according to CIIT grading system"""
    # Based on the transcript provided
    if mark >= 85:
        return 4.0, "A"
    elif mark >= 80:
        return 3.33, "B+"
    elif mark >= 75:
        return 3.0, "B"
    elif mark >= 70:
        return 2.66, "B-"
    elif mark >= 65:
        return 2.33, "C+"
    elif mark >= 60:
        return 2.0, "C"
    elif mark >= 55:
        return 1.33, "D+"
    elif mark >= 50:
        return 1.0, "D"
    else:
        return 0.0, "F"

def get_grade_description(grade):
    """Get description for each grade"""
    grade_descriptions = {
        "A": "Excellent",
        "B+": "Very Good",
        "B": "Good",
        "B-": "Good Minus",
        "C+": "Satisfactory Plus",
        "C": "Satisfactory",
        "D+": "Pass Plus",
        "D": "Pass",
        "F": "Fail"
    }
    return grade_descriptions.get(grade, "")

def main():
    # CIIT Header
    st.markdown("""
    <div class="ciit-header">
        <h1>🎓 COMSATS University Islamabad</h1>
        <h3>GPA & CGPA Calculator</h3>
        <p>Bachelor of Science in Statistics (BST) Program</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display CIIT Grading System
    st.markdown("---")
    st.markdown("### 📋 CIIT Grading System")
    
    grading_data = {
        "Marks (%)": ["85-100", "80-84", "75-79", "70-74", "65-69", "60-64", "55-59", "50-54", "Below 50"],
        "Grade": ["A", "B+", "B", "B-", "C+", "C", "D+", "D", "F"],
        "Grade Points": ["4.0", "3.33", "3.0", "2.66", "2.33", "2.0", "1.33", "1.0", "0.0"],
        "Description": ["Excellent", "Very Good", "Good", "Good Minus", "Satisfactory Plus", 
                       "Satisfactory", "Pass Plus", "Pass", "Fail"]
    }
    
    grading_df = pd.DataFrame(grading_data)
    st.dataframe(grading_df, use_container_width=True, hide_index=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose Calculator", 
                                   ["Single Semester GPA", "Multiple Semesters CGPA"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **CIIT Grading Scale:**
    - A: 85-100% (4.0)
    - B+: 80-84% (3.33)
    - B: 75-79% (3.0)
    - B-: 70-74% (2.66)
    - C+: 65-69% (2.33)
    - C: 60-64% (2.0)
    - D+: 55-59% (1.33)
    - D: 50-54% (1.0)
    - F: Below 50% (0.0)
    """)
    
    if app_mode == "Single Semester GPA":
        single_semester_gpa()
    else:
        multiple_semesters_cgpa()

def single_semester_gpa():
    st.markdown('<div class="sub-header">📚 Single Semester GPA Calculator</div>', unsafe_allow_html=True)
    
    # Student info
    col1, col2, col3 = st.columns(3)
    with col1:
        reg_no = st.text_input("Registration No", placeholder="CIIT/FA23-BST-089/LHR")
    with col2:
        student_name = st.text_input("Student Name", placeholder="AMINA")
    with col3:
        semester = st.text_input("Semester", placeholder="Fall 2024")
    
    # Number of subjects
    num_subjects = st.number_input(
        "Number of Subjects",
        min_value=1,
        max_value=20,
        value=6,
        step=1
    )
    
    st.markdown("### Enter Subject Details")
    
    # Create input fields for subjects
    subjects_data = []
    marks_list = []
    credits_list = []
    
    for i in range(num_subjects):
        st.markdown(f"**Subject {i+1}**")
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            subject_code = st.text_input(f"Course Code", placeholder="e.g., STA322", key=f"code_{i}")
            subject_name = st.text_input(f"Course Title", placeholder="e.g., Probability and Probability Distribution", key=f"name_{i}")
        with col2:
            marks = st.number_input(
                f"Marks", 
                min_value=0.0, 
                max_value=100.0, 
                value=75.0, 
                step=0.5,
                key=f"marks_{i}"
            )
        with col3:
            credit_hours = st.number_input(
                f"Credit Hours", 
                min_value=1.0, 
                max_value=5.0, 
                value=3.0, 
                step=0.5,
                key=f"credit_{i}"
            )
        with col4:
            # Display calculated grade
            grade_point, grade = convert_to_grade_point(marks)
            st.metric("Grade", f"{grade} ({grade_point})")
        
        grade_point, grade = convert_to_grade_point(marks)
        
        subjects_data.append({
            'Course Code': subject_code,
            'Course Title': subject_name,
            'Credit Hours': credit_hours,
            'Marks': marks,
            'Grade': grade,
            'Grade Points': grade_point,
            'Description': get_grade_description(grade)
        })
        marks_list.append(marks)
        credits_list.append(credit_hours)
    
    # Calculate GPA
    if st.button("Calculate GPA", type="primary"):
        gpa, total_credits = calculate_gpa(marks_list, credits_list)
        
        # Display results
        st.markdown("---")
        st.markdown('<div class="sub-header">📊 Semester Results</div>', unsafe_allow_html=True)
        
        # Display student info
        if reg_no or student_name or semester:
            col1, col2, col3 = st.columns(3)
            if reg_no:
                col1.metric("Registration No", reg_no)
            if student_name:
                col2.metric("Student Name", student_name)
            if semester:
                col3.metric("Semester", semester)
        
        # Display subjects table
        df = pd.DataFrame(subjects_data)
        st.dataframe(df, use_container_width=True)
        
        # Display GPA and summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Total Credit Hours", f"{total_credits}")
            st.metric("Total Subjects", f"{num_subjects}")
            st.metric("Grading Scale", "CIIT 4.0 Scale")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="gpa-display">GPA: {gpa:.2f}/4.0</div>', unsafe_allow_html=True)
            
            # Grade interpretation for CIIT system
            if gpa >= 3.7:
                st.success("🏆 Excellent Performance! First Class with Distinction")
            elif gpa >= 3.3:
                st.success("🎉 Very Good! First Class")
            elif gpa >= 3.0:
                st.info("👍 Good Performance! Second Class Upper")
            elif gpa >= 2.5:
                st.info("📚 Satisfactory! Second Class Lower")
            elif gpa >= 2.0:
                st.warning("✅ Acceptable Performance")
            elif gpa >= 1.0:
                st.warning("⚠️ Pass - Needs Improvement")
            else:
                st.error("❌ Fail - Academic Probation")
            
            st.markdown('</div>', unsafe_allow_html=True)

def multiple_semesters_cgpa():
    st.markdown('<div class="sub-header">🎓 Multiple Semesters CGPA Calculator</div>', unsafe_allow_html=True)
    
    # Student info
    col1, col2 = st.columns(2)
    with col1:
        reg_no = st.text_input("Registration No", placeholder="CIIT/FA23-BST-089/LHR", key="cgpa_reg")
    with col2:
        student_name = st.text_input("Student Name", placeholder="AMINA", key="cgpa_name")
    
    num_semesters = st.number_input(
        "Number of Semesters",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )
    
    semesters_data = []
    semester_gpas = []
    semester_credits_list = []
    
    for sem in range(num_semesters):
        st.markdown(f"### Semester {sem + 1} Details")
        
        sem_col1, sem_col2 = st.columns(2)
        with sem_col1:
            semester_name = st.text_input(
                f"Semester {sem + 1} Name",
                placeholder=f"Fall {2023 + sem}",
                key=f"sem_{sem}_name"
            )
        
        with sem_col2:
            num_subjects = st.number_input(
                f"Number of Subjects in Semester {sem + 1}",
                min_value=1,
                max_value=15,
                value=5,
                step=1,
                key=f"sem_{sem}_subjects"
            )
        
        semester_marks = []
        semester_credits = []
        semester_subjects = []
        
        for i in range(num_subjects):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                subject_code = st.text_input(
                    f"Sem {sem+1} - Course Code", 
                    placeholder="e.g., STA322",
                    key=f"sem{sem}_code_{i}"
                )
                subject_name = st.text_input(
                    f"Sem {sem+1} - Course Title", 
                    placeholder="e.g., Probability",
                    key=f"sem{sem}_name_{i}"
                )
            with col2:
                marks = st.number_input(
                    f"Marks", 
                    min_value=0.0, 
                    max_value=100.0, 
                    value=75.0, 
                    step=0.5,
                    key=f"sem{sem}_marks_{i}"
                )
            with col3:
                credit_hours = st.number_input(
                    f"Credit Hours", 
                    min_value=1.0, 
                    max_value=5.0, 
                    value=3.0, 
                    step=0.5,
                    key=f"sem{sem}_credit_{i}"
                )
            
            semester_marks.append(marks)
            semester_credits.append(credit_hours)
            semester_subjects.append({
                'code': subject_code,
                'name': subject_name,
                'marks': marks,
                'credits': credit_hours
            })
        
        # Calculate semester GPA
        sem_gpa, total_credits = calculate_gpa(semester_marks, semester_credits)
        
        semesters_data.append({
            'Semester': semester_name or f"Semester {sem + 1}",
            'GPA': sem_gpa,
            'Total Credits': total_credits,
            'Subjects': num_subjects
        })
        
        semester_gpas.append(sem_gpa)
        semester_credits_list.append(total_credits)
        
        st.info(f"📊 {semester_name or f'Semester {sem + 1}'} - GPA: {sem_gpa:.2f}/4.0 | Total Credits: {total_credits} | Subjects: {num_subjects}")
        st.markdown("---")
    
    # Calculate CGPA
    if st.button("Calculate CGPA", type="primary"):
        total_credits_all = sum(semester_credits_list)
        weighted_gpa_sum = sum(gpa * credits for gpa, credits in zip(semester_gpas, semester_credits_list))
        
        if total_credits_all > 0:
            cgpa = weighted_gpa_sum / total_credits_all
        else:
            cgpa = 0
        
        # Display results
        st.markdown("---")
        st.markdown('<div class="sub-header">📈 CGPA Results</div>', unsafe_allow_html=True)
        
        # Display student info
        if reg_no or student_name:
            col1, col2 = st.columns(2)
            if reg_no:
                col1.metric("Registration No", reg_no)
            if student_name:
                col2.metric("Student Name", student_name)
        
        # Display semesters summary
        df = pd.DataFrame(semesters_data)
        st.dataframe(df, use_container_width=True)
        
        # Display CGPA
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.metric("Total Semesters", num_semesters)
            st.metric("Total Credits", f"{total_credits_all}")
            st.metric("Average Semester GPA", f"{np.mean(semester_gpas):.2f}/4.0")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="gpa-display">CGPA: {cgpa:.2f}/4.0</div>', unsafe_allow_html=True)
            
            # CGPA interpretation for CIIT system
            if cgpa >= 3.7:
                st.success("🏆 Outstanding! First Class with Distinction")
            elif cgpa >= 3.3:
                st.success("🎉 Excellent! First Class")
            elif cgpa >= 3.0:
                st.info("👍 Very Good! Second Class Upper")
            elif cgpa >= 2.5:
                st.info("📚 Good! Second Class Lower")
            elif cgpa >= 2.0:
                st.warning("✅ Satisfactory Performance")
            elif cgpa >= 1.0:
                st.warning("⚠️ Minimum Passing CGPA")
            else:
                st.error("❌ Below Passing Requirements")
            
            # Scholastic Status based on CIIT standards
            if cgpa >= 2.0:
                scholastic_status = "Good Academic Standing (GAS)"
                st.success(f"**Scholastic Status:** {scholastic_status}")
            else:
                scholastic_status = "Academic Probation"
                st.error(f"**Scholastic Status:** {scholastic_status}")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
