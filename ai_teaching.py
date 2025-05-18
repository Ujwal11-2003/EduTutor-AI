import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from transformers import pipeline
import json
import os
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv()

class AITeachingAssistant:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        # Initialize question generation pipeline
        self.question_generator = pipeline(
            "text2text-generation",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        # Initialize answer grading pipeline
        self.answer_grader = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )

    def generate_lesson(self, topic, detail_level="Basic", difficulty="Intermediate", learning_style=["Visual"]):
        """Generate a personalized lesson"""
        prompt_template = PromptTemplate(
            input_variables=["topic", "detail_level", "difficulty", "learning_style"],
            template="""Create a {detail_level} lesson about {topic} for a {difficulty} level student who prefers {learning_style} learning style. \nInclude:\n1. Learning Objectives\n2. Main content with examples\n3. Key takeaways\n4. Practice activities\nUse markdown for formatting with headings, bullet points, and bold text for emphasis."""
        )
        prompt = prompt_template.format(
            topic=topic,
            detail_level=detail_level,
            difficulty=difficulty,
            learning_style=", ".join(learning_style)
        )
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_quiz(self, content, num_questions=5, question_type="multiple_choice"):
        """Generate quiz questions from content"""
        prompt_template = PromptTemplate(
            input_variables=["content", "num_questions", "question_type"],
            template="""Based on the following content, generate {num_questions} {question_type} questions:\n\n{content}\n\nFormat each question as:\nQuestion: [question text]\nOptions: [A-D]\nCorrect Answer: [letter]\nExplanation: [brief explanation]\n\nUse markdown formatting."""
        )
        prompt = prompt_template.format(
            content=content,
            num_questions=num_questions,
            question_type=question_type
        )
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def grade_answer(self, question, student_answer, correct_answer):
        """Grade a student's answer"""
        prompt_template = PromptTemplate(
            input_variables=["question", "student_answer", "correct_answer"],
            template="""Grade the following answer:\n\nQuestion: {question}\nStudent's Answer: {student_answer}\nCorrect Answer: {correct_answer}\n\nProvide:\n1. Score (0-100)\n2. Feedback\n3. Suggestions for improvement\n\nUse markdown formatting."""
        )
        prompt = prompt_template.format(
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer
        )
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_content(self, content):
        """Analyze content for key concepts and difficulty level"""
        prompt_template = PromptTemplate(
            input_variables=["content"],
            template="""Analyze the following content:\n\n{content}\n\nProvide:\n1. Key concepts\n2. Difficulty level\n3. Prerequisites\n4. Estimated study time\n5. Recommended learning path\n\nUse markdown formatting."""
        )
        prompt = prompt_template.format(content=content)
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_summary(self, content, length="concise"):
        """Generate a summary of the content"""
        prompt_template = PromptTemplate(
            input_variables=["content", "length"],
            template="""Create a {length} summary of the following content:\n\n{content}\n\nFocus on the main points and key takeaways.\nUse markdown formatting."""
        )
        prompt = prompt_template.format(
            content=content,
            length=length
        )
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_practice_exercises(self, content, num_exercises=3):
        """Generate practice exercises"""
        prompt_template = PromptTemplate(
            input_variables=["content", "num_exercises"],
            template="""Create {num_exercises} practice exercises based on this content:\n\n{content}\n\nFor each exercise, include:\n1. Problem statement\n2. Step-by-step solution\n3. Hints\n4. Common mistakes to avoid\n\nUse markdown formatting."""
        )
        prompt = prompt_template.format(
            content=content,
            num_exercises=num_exercises
        )
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

# Initialize AI teaching assistant
ai_teaching = AITeachingAssistant()
