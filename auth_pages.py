import streamlit as st
import auth
from PIL import Image
import requests
from io import BytesIO

def load_image_from_url(url):
    """Load image from URL"""
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except:
        return None

def show_home_page():
    """Display the home page"""
    st.markdown("""
        <style>
        .main-title {
            font-size: 48px;
            font-weight: bold;
            color: #4A90E2;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #666;
            text-align: center;
            margin-bottom: 40px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            font-size: 18px;
            padding: 10px 30px;
            border-radius: 25px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #357ABD;
            transform: scale(1.05);
        }
        .feature-card {
            background-color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 15px 0;
            border-left: 5px solid #4A90E2;
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-icon {
            font-size: 32px;
            margin-bottom: 15px;
        }
        .feature-title {
            color: #4A90E2;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .feature-description {
            color: #666;
            line-height: 1.6;
        }
        .benefits-section {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }
        .benefit-item {
            display: flex;
            align-items: center;
            margin: 15px 0;
        }
        .benefit-icon {
            font-size: 24px;
            margin-right: 15px;
            color: #4A90E2;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and subtitle
    st.markdown('<div class="main-title">Welcome to EduTutor AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Personal AI Learning Assistant</div>', unsafe_allow_html=True)

    # Banner image
    banner_url = "https://sl.bing.net/gLOis0wPOYS"
    banner_image = load_image_from_url(banner_url)
    if banner_image:
        st.image(banner_image, use_column_width=True)

    # Login and Register buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login Now", key="home_login"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("Register Free", key="home_register"):
            st.session_state.page = "register"
            st.rerun()

    # Key Features Section
    st.markdown("## ✨ Key Features")
    features = [
        {
            "title": "AI-Powered Learning",
            "description": "Get personalized lessons and explanations tailored to your learning style and pace. Our AI adapts to your needs and provides detailed, easy-to-understand content.",
            "icon": "🎯"
        },
        {
            "title": "Smart Flashcards",
            "description": "Create and study with AI-generated flashcards. Perfect for memorizing key concepts, definitions, and important information. Customize the number of cards and difficulty level.",
            "icon": "📚"
        },
        {
            "title": "Interactive Quizzes",
            "description": "Test your knowledge with AI-generated quizzes. Get immediate feedback and explanations for each answer. Choose from different difficulty levels and topics.",
            "icon": "📝"
        },
        {
            "title": "File Analysis",
            "description": "Upload your study materials (PDF, Word, Text) and get AI-powered analysis. Ask questions about the content and receive detailed explanations.",
            "icon": "📄"
        },
        {
            "title": "24/7 AI Tutor",
            "description": "Get instant help with any subject or topic. Ask questions, request examples, or get step-by-step explanations whenever you need them.",
            "icon": "🤖"
        },
        {
            "title": "Progress Tracking",
            "description": "Monitor your learning progress with detailed analytics. Track your quiz scores, study time, and areas that need improvement.",
            "icon": "📊"
        }
    ]

    # Display features in a grid
    cols = st.columns(2)
    for idx, feature in enumerate(features):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <div class="feature-title">{feature['title']}</div>
                    <div class="feature-description">{feature['description']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Benefits Section
    st.markdown("## 💡 Why Choose EduTutor AI?")
    st.markdown("""
        <div class="benefits-section">
            <div class="benefit-item">
                <span class="benefit-icon">⚡</span>
                <span>Instant access to AI-powered learning tools</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">🎓</span>
                <span>Personalized learning experience</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">📱</span>
                <span>Access from any device, anywhere</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">🔄</span>
                <span>Continuous learning and improvement</span>
            </div>
            <div class="benefit-item">
                <span class="benefit-icon">💡</span>
                <span>Smart content generation and analysis</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Support section
    st.markdown("## 💬 Need Help?")
    st.markdown("""
        Our support team is here to help you with any questions or issues you might have.
        Contact us at support@edututor.ai or use the chat widget below.
    """)

def show_login_page():
    """Display the login page"""
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-title {
            color: #4A90E2;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-title"><h2>Login to EduTutor AI</h2></div>', unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if email and password:
                success, message = auth.login_user(email, password)
                if success:
                    st.session_state.user_email = email
                    user_info = auth.get_user_info(email)
                    st.session_state.user_name = user_info["full_name"]
                    st.success(message)
                    # Redirect to the main app's home page
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please fill in all fields")

    # Back to home button
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_register_page():
    """Display the registration page"""
    st.markdown("""
        <style>
        .register-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .register-title {
            color: #4A90E2;
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="register-title"><h2>Create Your Account</h2></div>', unsafe_allow_html=True)

    # Registration form
    with st.form("register_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if full_name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = auth.register_user(full_name, email, password)
                    if success:
                        st.success(message)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields")

    # Back to home button
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun() 