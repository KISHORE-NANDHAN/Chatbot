import os
from pymongo import MongoClient
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient("mongodb+srv://Admin:Manager@cluster0.vths3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/CollegeDB")
db = client["Test"]
faculty_collection = db["departments"]

# Load text generation model from Hugging Face (BART for summarization)
generator = pipeline("text-generation", model="facebook/bart-large-cnn")

# Function to fetch faculty details
def fetch_faculty_info(name):
    faculty = faculty_collection.find_one({"name": {"$regex": name, "$options": "i"}})  # Case-insensitive search
    if not faculty:
        return "Sorry, I couldn't find information on that faculty member."

    faculty_info = f"{faculty['name']} is a {faculty['designation']} in the {faculty['department']} department. "
    faculty_info += f"They specialize in {', '.join(faculty['research_areas'])} and have {faculty['experience']} years of experience. "
    faculty_info += f"They have completed their PhD from {faculty['education']['phd']}."

    return faculty_info

# Generate response using Hugging Face model
def generate_response(query):
    faculty_info = fetch_faculty_info(query)
    gpt_prompt = f"Generate a user-friendly response for: {faculty_info}"

    response = generator(gpt_prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text'].strip()

# Example Usage
query = "Tell me about Mr.Rajendra Prasad Banavathu"
print(generate_response(query))
