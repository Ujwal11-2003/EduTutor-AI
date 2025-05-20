import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import requests
from streamlit_option_menu import option_menu
import database as db
import ai_teaching as ai
import dashboard as dash
import json
from datetime import datetime
import fitz  # PyMuPDF for PDF reading
import docx  # python-docx for DOCX reading

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE = os.getenv("OPENAI_API_BASE")

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1  # Default student ID
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Student"  # Default student name
if 'user_role' not in st.session_state:
    st.session_state.user_role = "student"  # Default role
if 'current_session' not in st.session_state:
    st.session_state.current_session = None

# Initialize LLM using ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    api_key=API_KEY,
    base_url=API_BASE
)

# Function to load lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://lottie.host/4d266ee4-2d6f-4c86-83a9-4fd050c61bc5/qwJ6zNUzBc.json")

# ---------- UI Configuration ----------
st.set_page_config(
    page_title="EduTutor AI",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
html, body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f0f4f8;
    margin: 0;
    padding: 0;
}

.main-title {
    font-size: 50px;
    font-weight: bold;
    background: linear-gradient(90deg, #1d8cf8, #f96332);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: fadeIn 1s ease-in;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 30px;
    animation: fadeInUp 1.5s ease-in-out;
}

.stButton>button {
    background: linear-gradient(to right, #ff416c, #89CFF0);
    color: white;
    font-size: 18px;
    padding: 10px 24px;
    border-radius: 12px;
    border: none;
    transition: all 0.4s ease-in-out;
    box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: transform 0.3s ease;
    border-left: 4px solid #4B8BBE;
}

.card:hover {
    transform: translateY(-5px);
}

/* Animation keyframes */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInUp {
    from { 
        opacity: 0;
        transform: translateY(20px);
    }
    to { 
        opacity: 1;
        transform: translateY(0);
    }
}

/* Custom container for better spacing */
.custom-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Form styling */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea,
.stSelectbox>div>div>select {
    border-radius: 8px !important;
    border: 1px solid #ddd !important;
    padding: 10px !important;
}

.stTextInput>div>div>input:focus, 
.stTextArea>div>div>textarea:focus,
.stSelectbox>div>div>select:focus {
    border-color: #4B8BBE !important;
    box-shadow: 0 0 0 2px rgba(75, 139, 190, 0.2) !important;
}

/* Custom divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #4B8BBE, transparent);
    margin: 2rem 0;
}

/* Speech interface styles */
.speech-container {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.speech-button {
    background-color: #4B8BBE;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.speech-button:hover {
    background-color: #357ABD;
    transform: scale(1.05);
}

/* Dashboard styles */
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #4B8BBE;
}

.metric-label {
    color: #666;
    margin-top: 5px;
}

.edututor-hero {
    background: linear-gradient(90deg, #1d8cf8 0%, #f96332 100%);
    border-radius: 18px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
}
.edututor-feature-card {
    background: linear-gradient(135deg, #fff 60%, #e0f7fa 100%);
    border-radius: 16px;
    padding: 1.5rem 1.2rem;
    margin: 0.5rem;
    box-shadow: 0 2px 12px rgba(75,139,190,0.08);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: transform 0.2s;
}
.edututor-feature-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 6px 24px rgba(75,139,190,0.18);
}
.edututor-feature-icon {
    font-size: 2.2rem;
    margin-right: 0.7rem;
}
.edututor-cta {
    background: linear-gradient(90deg, #f96332 0%, #1d8cf8 100%);
    color: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-size: 1.3rem;
    text-align: center;
    margin-top: 2rem;
    font-weight: 600;
    box-shadow: 0 2px 12px rgba(255, 75, 75, 0.12);
}

/* News-ticker style banner for key benefits */
.edututor-ticker-container {
    width: 100%;
    overflow: hidden;
    background: linear-gradient(90deg, #1d8cf8 0%, #f96332 100%);
    border-radius: 12px;
    margin: 1.5rem 0 2rem 0;
    box-shadow: 0 2px 12px rgba(75,139,190,0.10);
}
.edututor-ticker {
    display: inline-block;
    white-space: nowrap;
    padding: 0.7rem 0;
    font-size: 1.15rem;
    color: #fff;
    font-weight: 600;
    animation: ticker-move 22s linear infinite;
}
@keyframes ticker-move {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}
</style>
""", unsafe_allow_html=True)

# Main app UI
def show_main_ui():
    with st.container():
        selected = option_menu(
            menu_title=None,
            options=["Home", "Learn", "Quiz", "Practice", "Video Recommendations", "Dashboard", "Settings"],  # Removed "Quiz Generator"
            icons=["house", "book", "question-square", "pencil-square", "youtube", "graph-up", "gear"],       # Removed corresponding icon
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#ffffff",
                    "box-shadow": "0 2px 10px rgba(0,0,0,0.1)"
                },
                "icon": {"color": "#4B8BBE", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#f0f2f6",
                    "color": "#333",
                },
                "nav-link-selected": {
                    "background-color": "#4B8BBE",
                    "font-weight": "500"
                },
            }
        )

    if selected == "Home":
        show_home_page()
    elif selected == "Learn":
        show_learn_page()
    elif selected == "Quiz":
        show_quiz_page()
    elif selected == "Practice":
        show_practice_page()
    elif selected == "Video Recommendations":
        show_video_recommendations_page()
    elif selected == "Dashboard":
        show_dashboard_page()
    elif selected == "Settings":
        show_settings_page()

def show_home_page():
    st.markdown(
        """
        <div class="edututor-hero">
            <h1 style="font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem;">
                Welcome to <span style="color: #ffe066;">EduTutor AI</span> 🚀
            </h1>
            <p style="font-size: 1.3rem; margin-bottom: 0.7rem;">
                <b>EduTutor</b> is your all-in-one, AI-powered learning companion. Whether you're a student, teacher, or lifelong learner, EduTutor adapts to your style and helps you master any topic with personalized lessons, quizzes, and analytics.
            </p>
            <ul style="font-size: 1.1rem; margin-bottom: 0.7rem;">
                <li>✨ <b>Personalized Learning</b> — Lessons and quizzes tailored just for you</li>
                <li>🧠 <b>AI-Powered Insights</b> — Track your progress and get smart recommendations</li>
                <li>🌍 <b>Anytime, Anywhere</b> — Learn at your own pace, on any device</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # News-ticker style banner for key benefits
    st.markdown(
        """
        <div class="edututor-ticker-container">
            <div class="edututor-ticker">
                🌍 Anytime, Anywhere — Learn at your own pace, on any device &nbsp; • &nbsp;
                📚 AI Lessons — Get custom lessons on any topic, at any level &nbsp; • &nbsp;
                📝 Smart Quizzes — Test your knowledge with instant feedback &nbsp; • &nbsp;
                📊 Progress Dashboard — Visualize your learning journey and achievements &nbsp; • &nbsp;
                ⚙️ Customizable Experience — Set your preferences, goals, and notifications
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Feature cards with more color
    st.markdown("""
    <div style='display: flex; flex-wrap: wrap; justify-content: center;'>
        <div class="edututor-feature-card" style="background: linear-gradient(135deg, #e3f0ff 60%, #a8e063 100%); box-shadow: 0 4px 16px rgba(29,140,248,0.10);">
            <span class="edututor-feature-icon" style="color: #1d8cf8; background: #e3f0ff; border-radius: 50%; padding: 0.5rem;">📚</span>
            <div>
                <b style="color: #1d8cf8;">AI Lessons</b><br>
                <span style="color: #333;">Get custom lessons on any topic, at any level.</span>
            </div>
        </div>
        <div class="edututor-feature-card" style="background: linear-gradient(135deg, #fffbe7 60%, #f9d423 100%); box-shadow: 0 4px 16px rgba(249,99,50,0.10);">
            <span class="edututor-feature-icon" style="color: #f96332; background: #fffbe7; border-radius: 50%; padding: 0.5rem;">📝</span>
            <div>
                <b style="color: #f96332;">Smart Quizzes</b><br>
                <span style="color: #333;">Test your knowledge with instant feedback.</span>
            </div>
        </div>
        <div class="edututor-feature-card" style="background: linear-gradient(135deg, #e0f7fa 60%, #4dd0e1 100%); box-shadow: 0 4px 16px rgba(75,139,190,0.10);">
            <span class="edututor-feature-icon" style="color: #00bcd4; background: #e0f7fa; border-radius: 50%; padding: 0.5rem;">📊</span>
            <div>
                <b style="color: #00bcd4;">Progress Dashboard</b><br>
                <span style="color: #333;">Visualize your learning journey and achievements.</span>
            </div>
        </div>
        <div class="edututor-feature-card" style="background: linear-gradient(135deg, #f3e7ff 60%, #a770ef 100%); box-shadow: 0 4px 16px rgba(167,112,239,0.10);">
            <span class="edututor-feature-icon" style="color: #a770ef; background: #f3e7ff; border-radius: 50%; padding: 0.5rem;">⚙️</span>
            <div>
                <b style="color: #a770ef;">Customizable Experience</b><br>
                <span style="color: #333;">Set your preferences, goals, and notifications.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Lottie animation (right side)
    if lottie_ai:
        st.components.v1.html(
            """
            <div style="text-align: center; margin-top: 2rem;">
                <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
                <lottie-player
                    src="https://lottie.host/4d266ee4-2d6f-4c86-83a9-4fd050c61bc5/qwJ6zNUzBc.json"
                    background="transparent"
                    speed="1"
                    style="width: 100%; height: 300px;"
                    loop
                    autoplay>
                </lottie-player>
            </div>
            """,
            height=300,
        )
    # Call to action
    st.markdown(
        """
        <div class="edututor-cta">
            Ready to start your smart learning journey?<br>
            <span style="font-size: 1.1rem;">Choose a feature from the menu above and let EduTutor guide you!</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_learn_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #4B8BBE;'>📚 Learn with AI</h1>
            <p style="color: #555;">Choose a topic, upload your own material, and let AI create a personalized lesson for you.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)

    # --- File Upload Section ---
    st.markdown("#### 📂 Upload a File (PDF or DOCX)")
    uploaded_file = st.file_uploader("Upload your study material (optional)", type=["pdf", "docx"], help="You can upload a PDF or Word document to generate a lesson or summary from your own content.")
    file_content = None
    file_text = None
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join(page.get_text() for page in pdf)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            import docx
            uploaded_file.seek(0)
            doc = docx.Document(uploaded_file)
            file_text = "\n".join([para.text for para in doc.paragraphs])
        st.success("File uploaded successfully!")
        st.markdown("**Preview:**")
        st.text_area("File Content Preview", file_text[:2000] + ("..." if len(file_text) > 2000 else ""), height=150)

    with st.form("lesson_form"):
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("What would you like to learn?", placeholder="Enter a topic")
            detail_level = st.selectbox("Detail Level", ["Overview", "Basic", "Detailed", "Comprehensive"])
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
            learning_style = st.multiselect("Learning Style(s)", ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"], default=["Visual"])
        submitted = st.form_submit_button("Generate Lesson", type="primary")

    # --- Lesson Generation ---
    if submitted or (uploaded_file and st.session_state.get('generate_from_file')):
        if topic or file_text:
            with st.spinner("Creating your personalized lesson..."):
                session_id = db.start_study_session(st.session_state.user_id, topic or "(from file)", "lesson")
                st.session_state.current_session = session_id
                # If file uploaded, use its content for lesson
                if file_text:
                    lesson = ai.ai_teaching.generate_lesson(file_text, detail_level, difficulty, learning_style)
                else:
                    lesson = ai.ai_teaching.generate_lesson(topic, detail_level, difficulty, learning_style)
                st.markdown("---")
                st.markdown("### Your Custom Lesson")
                st.markdown(lesson, unsafe_allow_html=True)
                st.download_button(
                    label="Download Lesson",
                    data=lesson,
                    file_name=f"{topic or 'uploaded_file'}_lesson.md",
                    mime="text/markdown"
                )
        else:
            st.warning("Please enter a topic or upload a file to generate a lesson.")

    # --- File Summary/Analysis ---
    if uploaded_file and file_text:
        if st.button("Summarize/Analyze Uploaded File"):
            with st.spinner("Analyzing your file..."):
                summary = ai.ai_teaching.generate_summary(file_text, length="concise")
                st.markdown("---")
                st.markdown("### File Summary/Analysis")
                st.markdown(summary, unsafe_allow_html=True)

    # --- Lesson History Section ---
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 🕑 Lesson History (Recent)")
    # Example: Show last 5 lessons (replace with real DB/history if available)
    if 'lesson_history' not in st.session_state:
        st.session_state.lesson_history = []
    if submitted or (uploaded_file and st.session_state.get('generate_from_file')):
        st.session_state.lesson_history.insert(0, topic or uploaded_file.name)
        st.session_state.lesson_history = st.session_state.lesson_history[:5]
    for i, hist in enumerate(st.session_state.lesson_history):
        st.markdown(f"{i+1}. {hist}")

def show_quiz_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #4B8BBE;'>📝 Quiz Time</h1>
            <p style="color: #555;">Test your knowledge with AI-generated quizzes.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("quiz_form"):
        topic = st.text_input("Quiz Topic", placeholder="Enter a topic")
        num_questions = st.slider("Number of Questions", 3, 10, 5)
        question_type = st.selectbox("Question Type", 
                                   ["Multiple Choice", "Fill in the Blank", "Short Answer"])
        
        submitted = st.form_submit_button("Generate Quiz", type="primary")
    
    if submitted:
        if topic:
            with st.spinner("Creating your quiz..."):
                # Start study session
                session_id = db.start_study_session(st.session_state.user_id, topic, "quiz")
                st.session_state.current_session = session_id
                
                # Generate quiz
                quiz = ai.ai_teaching.generate_quiz(topic, num_questions, question_type.lower())
                
                # Display quiz
                st.markdown("---")
                st.markdown("### Your Quiz")
                st.markdown(quiz, unsafe_allow_html=True)
                
                # Add download button
                st.download_button(
                    label="Download Quiz",
                    data=quiz,
                    file_name=f"{topic}_quiz.md",
                    mime="text/markdown"
                )
        else:
            st.warning("Please enter a topic to generate a quiz.")

def show_practice_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #4B8BBE;'>✏️ Practice Exercises</h1>
            <p style="color: #555;">Get hands-on practice with AI-generated exercises and flashcards.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("practice_form"):
        topic = st.text_input("Practice Topic", placeholder="Enter a topic")
        num_exercises = st.slider("Number of Exercises", 2, 5, 3)
        generate_flashcards = st.checkbox("Also generate flashcards for this topic?", value=True)
        submitted = st.form_submit_button("Generate Exercises", type="primary")
    
    if submitted:
        if topic:
            with st.spinner("Creating practice exercises..."):
                # Start study session
                session_id = db.start_study_session(st.session_state.user_id, topic, "practice")
                st.session_state.current_session = session_id
                
                # Generate exercises
                exercises = ai.ai_teaching.generate_practice_exercises(topic, num_exercises)
                
                # Display exercises
                st.markdown("---")
                st.markdown("### Practice Exercises")
                st.markdown(exercises, unsafe_allow_html=True)
                
                # Add download button
                st.download_button(
                    label="Download Exercises",
                    data=exercises,
                    file_name=f"{topic}_exercises.md",
                    mime="text/markdown"
                )
                
                # Flashcard generation
                if generate_flashcards and hasattr(ai.ai_teaching, 'generate_flashcards'):
                    with st.spinner("Generating flashcards..."):
                        flashcards = ai.ai_teaching.generate_flashcards(topic, 5)
                        st.markdown("---")
                        st.markdown("### Flashcards for Practice Topic")
                        st.markdown(flashcards, unsafe_allow_html=True)
        else:
            st.warning("Please enter a topic to generate exercises.")

def show_dashboard_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #4B8BBE;'>📊 Learning Dashboard</h1>
            <p style="color: #555;">Track your progress and achievements.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Show learning progress
    st.markdown("### 📈 Learning Progress")
    dash.dashboard.show_learning_progress(st.session_state.user_id)
    
    # Show quiz performance
    st.markdown("### 📝 Quiz Performance")
    dash.dashboard.show_quiz_performance(st.session_state.user_id)
    
    # Show study analytics
    st.markdown("### ⏱️ Study Analytics")
    dash.dashboard.show_study_analytics(st.session_state.user_id)
    
    # Show achievements
    st.markdown("### 🏆 Achievements")
    dash.dashboard.show_achievements(st.session_state.user_id)
    
    # Show learning path
    st.markdown("### 🗺️ Learning Path")
    dash.dashboard.show_learning_path(st.session_state.user_id)

def show_settings_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #4B8BBE;'>⚙️ Settings</h1>
            <p style="color: #555;">Customize your learning experience and account preferences.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)

    # --- Profile Card ---
    with st.container():
        st.markdown("""
        <div class="card" style="display: flex; align-items: center;">
            <div style="flex: 1;">
                <h3 style='color: #4B8BBE; margin-bottom: 0;'>👤 Profile</h3>
                <p style='margin: 0;'><b>Name:</b> {}</p>
                <p style='margin: 0;'><b>Email:</b> {}</p>
                <p style='margin: 0;'><b>Role:</b> {}</p>
            </div>
        </div>
        """.format(
            st.session_state.get('user_name', 'Student'),
            st.session_state.get('user_email', 'student@email.com'),
            st.session_state.get('user_role', 'student')
        ), unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # --- Theme Switcher ---
    st.markdown("### 🎨 Theme")
    theme = st.radio("Choose your theme:", ["Light", "Dark"], horizontal=True)

    # --- Learning Preferences ---
    st.markdown("### 🎯 Learning Preferences")
    learning_styles = st.multiselect(
        "Learning Styles",
        ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
        default=["Visual"]
    )
    daily_goal = st.slider("Daily Study Goal (minutes)", 10, 180, 30, step=5)

    # --- Notification Settings ---
    st.markdown("### 🔔 Notifications")
    email_notifications = st.checkbox("Email Notifications", value=True)
    study_reminders = st.checkbox("Study Reminders", value=True)
    notif_freq = st.selectbox("Notification Frequency", ["Never", "Daily", "Weekly", "Only for important updates"], index=1)

    # --- Account Actions ---
    st.markdown("### 🗑️ Account Actions")
    if st.button("Delete Account", type="secondary"):
        st.warning("Are you sure you want to delete your account? This action cannot be undone.")
        if st.button("Confirm Delete", type="primary"):
            st.error("Account deletion is not implemented in this demo.")

    # --- Save Button ---
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# --- Quiz Generator Page ---
def show_quiz_generator_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #f96332;'>💡 Quiz Generator</h1>
            <p style="color: #555;">Create a custom quiz on any topic, with your choice of difficulty and question type.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)
    topic = st.text_input("Quiz Topic (Custom)", placeholder="Enter a topic")
    num_questions = st.slider("Number of Questions", 3, 15, 5)
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    question_type = st.selectbox("Question Type", ["Multiple Choice", "Fill in the Blank", "Short Answer"])
    if st.button("Generate Custom Quiz", type="primary"):
        with st.spinner("Generating quiz..."):
            quiz = ai.ai_teaching.generate_quiz(topic, num_questions, question_type.lower())
            st.markdown("---")
            st.markdown("### Your Custom Quiz")
            st.markdown(quiz, unsafe_allow_html=True)

# --- Video Recommendations Page ---
def show_video_recommendations_page():
    st.markdown("""
        <div class="custom-container">
            <h1 style='color: #FF0000;'>🎬 Video Recommendations</h1>
            <p style="color: #555;">Get top YouTube video recommendations for any subject or topic.</p>
            <div class="custom-divider"></div>
        </div>
    """, unsafe_allow_html=True)
    subject = st.text_input("Enter a subject or topic for video recommendations", placeholder="e.g. Algebra, Photosynthesis, World War II")
    max_results = st.slider("Number of Videos", 1, 10, 5)
    if st.button("Get Recommendations", type="primary"):
        if not subject:
            st.warning("Please enter a subject or topic.")
        else:
            with st.spinner("Fetching video recommendations..."):
                videos = get_youtube_videos(subject, max_results)
                if videos:
                    st.markdown("---")
                    st.markdown("### Recommended Videos")
                    for video in videos:
                        st.markdown(f"**[{video['title']}]({video['url']})**  ")
                        st.markdown(f"<iframe width='100%' height='315' src='https://www.youtube.com/embed/{video['id']}' frameborder='0' allowfullscreen></iframe>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#888;'>{video['description'][:120]}...</span>", unsafe_allow_html=True)
                        st.markdown("---")
                else:
                    st.info("No videos found or API limit reached.")

# --- YouTube API Helper ---
def get_youtube_videos(query, max_results=5):
    import requests
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        st.error("YouTube API key not set. Please set YOUTUBE_API_KEY in your .env file.")
        return []
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = []
        for item in data.get("items", []):
            video = {
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        return videos
    else:
        return []

# Main app flow
show_main_ui()
