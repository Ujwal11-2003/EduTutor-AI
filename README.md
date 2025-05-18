# EduTutor AI - Modern AI-Powered Learning Platform

EduTutor AI is a comprehensive educational platform that leverages artificial intelligence to provide personalized learning experiences. The platform features a modern, responsive interface and includes various tools for learning, practice, and progress tracking.

## 🌟 Features

### 🔐 Authentication
- Secure user registration and login system
- Session management
- User profile management

### 📚 AI Teaching Assistant
- Personalized lesson generation
- Interactive quizzes
- Practice exercises
- Content analysis and summarization

### 🎤 Speech & Translation
- Text-to-speech for lessons and content
- Speech-to-text for voice input
- Multi-language support with automatic translation

### 📊 Smart Dashboard
- Learning progress tracking
- Quiz performance analytics
- Study time statistics
- Achievement system

### 🎯 Learning Features
- Customizable learning paths
- Multiple learning styles support
- Interactive practice exercises
- Progress tracking and analytics

## 🛠️ Tech Stack

### Frontend/UI
- Streamlit
- Streamlit Components
- Lottie animations
- Custom CSS

### Backend/Logic
- Python
- LangChain
- Hugging Face Transformers
- IBM LLM

### Database
- SQLite

### Speech & Translation
- Google Speech Recognition
- gTTS
- Hugging Face translation models

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/edututor-ai.git
cd edututor-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=your_openai_api_base
```

5. Run the application:
```bash
streamlit run app.py
```

## 📝 Usage

1. Register a new account or login with existing credentials
2. Navigate through different sections:
   - Home: Overview and quick access
   - Learn: Generate personalized lessons
   - Quiz: Take AI-generated quizzes
   - Practice: Work on practice exercises
   - Dashboard: View progress and analytics
   - Settings: Customize your experience

3. Use the AI teaching assistant to:
   - Generate lessons on any topic
   - Create quizzes and practice exercises
   - Get explanations and summaries
   - Track your learning progress

## 🔧 Configuration

The application can be configured through:
- Environment variables in `.env`
- User settings in the Settings page
- Database configuration in `database.py`

## 📚 Documentation

Detailed documentation for each component:
- [Authentication System](docs/auth.md)
- [AI Teaching Assistant](docs/ai_teaching.md)
- [Speech & Translation](docs/speech_translation.md)
- [Dashboard & Analytics](docs/dashboard.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit for the web framework
- LangChain for AI integration
- Hugging Face for ML models
- Google for speech services 