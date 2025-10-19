import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="GPA/CGPA Calculator - CIIT",
    page_icon="📊",
    layout="wide"
)

# Grading system based on the transcript
GRADING_SYSTEM = {
    'A': {'range': (85, 100), 'grade_points': 4.0},
    'B+': {'range': (80, 84), 'grade_points': 3.33},
    'B': {'range': (75, 79), 'grade_points': 3.0},
    'C+': {'range': (70, 74), 'grade_points': 2.33},
    'C': {'range': (65, 69), 'grade_points': 2.0},
    'D+': {'range': (60, 64), 'grade_points': 1.33},
    'D': {'range': (50, 59), 'grade_points': 1.0},
    'F': {'range': (0, 49), 'grade_points': 0.0}
}

def calculate_grade_points(marks):
    """Calculate grade points based on marks"""
    for grade, info in GRADING_SYSTEM.items():
        min_range, max_range = info['range']
        if min_range <= marks <= max_range:
            return info['grade_points'], grade
    return 0.0, 'F'

def calculate_gpa(courses_data):
    """Calculate GPA for given courses"""
    total_credit_points = 0
    total_credits = 0
    
    for course in courses_data:
        credit_hours = course['credit']
        marks = course['marks']
        
        grade_points, letter_grade = calculate_grade_points(marks)
        credit_points = credit_hours * grade_points
        
        total_credit_points += credit_points
        total_credits += credit_hours
        
        # Update course data with calculated values
        course['grade_points'] = grade_points
        course['letter_grade'] = letter_grade
        course['credit_points'] = credit_points
    
    gpa = total_credit_points / total_credits if total_credits > 0 else 0.0
    return gpa, total_credits

def main():
    st.title("🎓 CIIT GPA/CGPA Calculator")
    st.markdown("---")
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. Enter your course details
        2. Add marks for each course
        3. Click 'Calculate GPA'
        4. View your results
        
        **Grading System:**
        - A: 85-100 (4.0)
        - B+: 80-84 (3.33)
        - B: 75-79 (3.0)
        - C+: 70-74 (2.33)
        - C: 65-69 (2.0)
        - D+: 60-64 (1.33)
        - D: 50-59 (1.0)
        - F: 0-49 (0.0)
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Course Entry")
        
        # Initialize session state for courses
        if 'courses' not in st.session_state:
            st.session_state.courses = []
        
        # Course entry form
        with st.form("course_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                course_code = st.text_input("Course Code", placeholder="e.g., STA322")
            with col2:
                course_name = st.text_input("Course Title", placeholder="e.g., Probability")
            with col3:
                credit_hours = st.number_input("Credit Hours", min_value=1, max_value=4, value=3)
            
            marks_obtained = st.slider("Marks Obtained", min_value=0, max_value=100, value=70)
            
            add_course = st.form_submit_button("Add Course")
            
            if add_course:
                if course_code and course_name:
                    new_course = {
                        'code': course_code,
                        'name': course_name,
                        'credit': credit_hours,
                        'marks': marks_obtained
                    }
                    st.session_state.courses.append(new_course)
                    st.success(f"Added {course_code}: {course_name}")
                else:
                    st.error("Please enter both course code and name")
        
        # Display current courses
        if st.session_state.courses:
            st.subheader("Current Courses")
            courses_df = pd.DataFrame(st.session_state.courses)
            st.dataframe(courses_df, use_container_width=True)
            
            # Clear courses button
            if st.button("Clear All Courses"):
                st.session_state.courses = []
                st.rerun()
    
    with col2:
        st.header("Calculate GPA")
        
        if st.session_state.courses:
            if st.button("Calculate GPA", type="primary"):
                gpa, total_credits = calculate_gpa(st.session_state.courses)
                
                # Display results
                st.success(f"🎯 **GPA Calculated: {gpa:.2f}**")
                st.info(f"📚 **Total Credit Hours: {total_credits}**")
                
                # Detailed results table
                st.subheader("Detailed Results")
                results_data = []
                for course in st.session_state.courses:
                    results_data.append({
                        'Course Code': course['code'],
                        'Course Title': course['name'],
                        'Credit Hrs': course['credit'],
                        'Marks': course['marks'],
                        'Grade': course['letter_grade'],
                        'Grade Points': f"{course['grade_points']:.2f}",
                        'Credit Points': f"{course['credit_points']:.2f}"
                    })
                
                results_df = pd.DataFrame(results_data)
                st.dataframe(results_df, use_container_width=True)
                
                # Performance analysis
                st.subheader("Performance Analysis")
                total_courses = len(st.session_state.courses)
                passed_courses = sum(1 for course in st.session_state.courses if course['marks'] >= 50)
                failed_courses = total_courses - passed_courses
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Courses", total_courses)
                with col2:
                    st.metric("Passed Courses", passed_courses)
                with col3:
                    st.metric("Failed Courses", failed_courses)
        
        else:
            st.warning("Please add courses first to calculate GPA")
    
    # CGPA Calculator Section
    st.markdown("---")
    st.header("CGPA Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Semester")
        current_gpa = st.number_input("Current Semester GPA", min_value=0.0, max_value=4.0, value=0.0, step=0.01)
        current_credits = st.number_input("Current Semester Credit Hours", min_value=0, max_value=30, value=0)
    
    with col2:
        st.subheader("Previous Semesters")
        previous_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=4.0, value=0.0, step=0.01)
        previous_credits = st.number_input("Previous Total Credit Hours", min_value=0, max_value=200, value=0)
    
    if st.button("Calculate CGPA"):
        if current_credits > 0 or previous_credits > 0:
            total_previous_points = previous_cgpa * previous_credits
            total_current_points = current_gpa * current_credits
            total_all_credits = previous_credits + current_credits
            
            if total_all_credits > 0:
                cgpa = (total_previous_points + total_current_points) / total_all_credits
                st.success(f"🎓 **Your CGPA is: {cgpa:.2f}**")
                
                # Display calculation breakdown
                st.info(f"""
                **Calculation Breakdown:**
                - Previous Points: {total_previous_points:.2f}
                - Current Points: {total_current_points:.2f}
                - Total Credits: {total_all_credits}
                """)
            else:
                st.error("Total credit hours cannot be zero")
        else:
            st.error("Please enter credit hours for at least one semester")

if __name__ == "__main__":
    main()
