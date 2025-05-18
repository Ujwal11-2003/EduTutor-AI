from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLMcan you make me like home and learing page 
llm = ChatOpenAI(
    model="mistralai/mixtral-8x7b-instruct",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE")
)

def generate_lesson(topic, detail_level="Basic", difficulty="Intermediate", learning_style=["Visual"]):
    """
    Generate a personalized lesson on the given topic
    
    Args:
        topic (str): The topic to generate a lesson about
        detail_level (str): Level of detail ("Overview", "Basic", "Detailed", "Comprehensive")
        difficulty (str): Difficulty level ("Beginner", "Intermediate", "Advanced")
        learning_style (list): Preferred learning styles (e.g., ["Visual", "Auditory"])
    
    Returns:
        str: Generated lesson content
    """
    prompt_template = PromptTemplate(
        input_variables=["topic", "detail_level", "difficulty", "learning_style"],
        template="""Create a {detail_level} lesson about {topic} for a {difficulty} level student who prefers {learning_style} learning style. 
        Structure the lesson with:
        1. Clear learning objectives
        2. Main content with examples
        3. Key takeaways
        4. Suggested practice activities
        
        Make it engaging and suitable for the specified level. Use markdown formatting for headings, lists, and emphasis."""
    )
    
    prompt = prompt_template.format(
        topic=topic,
        detail_level=detail_level,
        difficulty=difficulty,
        learning_style=", ".join(learning_style)
    )
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating lesson: {str(e)}"

def generate_quiz(topic, difficulty="Intermediate"):
    """
    Generate a quiz with questions about the given topic
    
    Args:
        topic (str): The topic to generate a quiz about
        difficulty (str): Difficulty level ("Beginner", "Intermediate", "Advanced")
    
    Returns:
        str: Generated quiz content
    """
    prompt_template = PromptTemplate(
        input_variables=["topic", "difficulty"],
        template="""Create a 5-question multiple choice quiz about {topic} suitable for {difficulty} level students. 
        Format each question with:
        - Question stem
        - 4 options (A-D)
        - Correct answer marked with (Correct)
        
        Include a mix of factual and conceptual questions. Add explanations for the answers at the end.
        Use markdown formatting for clear presentation."""
    )
    
    prompt = prompt_template.format(
        topic=topic,
        difficulty=difficulty
    )
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def generate_flashcards(topic, count=5):
    """
    Generate flashcards for the given topic
    
    Args:
        topic (str): The topic to generate flashcards about
        count (int): Number of flashcards to generate
    
    Returns:
        str: Generated flashcards content
    """
    prompt_template = PromptTemplate(
        input_variables=["topic", "count"],
        template="""Create {count} flashcards about {topic}. For each flashcard:
        Front: [Term/Question]
        Back: [Definition/Answer]
        
        Make the back side concise (1-2 sentences). Format the response with clear separation between cards.
        Ensure the flashcards cover key concepts and important details about the topic."""
    )
    
    prompt = prompt_template.format(
        topic=topic,
        count=count
    )
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating flashcards: {str(e)}"

def generate_practice_exercises(topic, difficulty="Intermediate"):
    """
    Generate practice exercises for the given topic
    
    Args:
        topic (str): The topic to generate exercises about
        difficulty (str): Difficulty level ("Beginner", "Intermediate", "Advanced")
    
    Returns:
        str: Generated exercises with solutions
    """
    prompt_template = PromptTemplate(
        input_variables=["topic", "difficulty"],
        template="""Create 3 practice exercises about {topic} suitable for {difficulty} level students.
        For each exercise include:
        - Problem statement
        - Step-by-step solution
        - Explanation of key concepts
        
        Make the exercises progressively more challenging. Use markdown formatting for clear presentation."""
    )
    
    prompt = prompt_template.format(
        topic=topic,
        difficulty=difficulty
    )
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating practice exercises: {str(e)}"

def summarize_content(content, length="short"):
    """
    Summarize the given content to the specified length
    
    Args:
        content (str): Content to summarize
        length (str): Desired length ("short", "medium", "long")
    
    Returns:
        str: Generated summary
    """
    prompt_template = PromptTemplate(
        input_variables=["content", "length"],
        template="""Create a {length} summary of the following content:
        {content}
        
        The summary should capture the key points and main ideas while being concise."""
    )
    
    prompt = prompt_template.format(
        content=content,
        length=length
    )
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"