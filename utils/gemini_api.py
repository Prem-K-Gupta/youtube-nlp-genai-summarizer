import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() 

# Configure API key based on environment variable
genai_api_key = os.getenv("GOOGLE_API_KEY")  
if not genai_api_key:
    raise ValueError("Google API key is not set. Please configure the 'GOOGLE_API_KEY' environment variable.")

genai.configure(api_key=genai_api_key)

def gemini_extract_topics(text):
    """
    Extract topics from the provided text using the Google Gemini API.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Extract topics from the following text:\n{text}")
    return response.text.split(", ")

def gemini_key_concepts(text):
    """
    Extract key concepts from the provided text using the Google Gemini API.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Extract key concepts from the following text:\n{text}")
    return response.text.split(", ")

def gemini_contextual_insights(concepts):
    """
    Generate detailed contextual insights for a list of concepts using the Google Gemini API.
    """
    insights = {}
    model = genai.GenerativeModel("gemini-1.5-flash")
    for concept in concepts:
        response = model.generate_content(f"Provide a detailed explanation for '{concept}':")
        insights[concept] = response.text
    return insights



'''import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=genai_api_key)

def gemini_extract_topics(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Extract topics from the following text:\n{text}")
    return response.text.split(", ")

def gemini_key_concepts(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Extract key concepts from the following text:\n{text}")
    return response.text.split(", ")

def gemini_contextual_insights(concepts):
    insights = {}
    model = genai.GenerativeModel("gemini-1.5-flash")
    for concept in concepts:
        response = model.generate_content(f"Provide a detailed explanation for '{concept}':")
        insights[concept] = response.text
    return insights'''
