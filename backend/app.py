import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from docx import Document
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('.env')
app = Flask(__name__, static_folder="../frontend", static_url_path="/")

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    

CORS(app)  # Enable CORS

GEMINI_API_KEY="AIzaSyC05l0XtlWU8xtgUGrOJr0hgZh901buR6A"
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta2/generateText"

# Function to extract text from .docx files
def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

# Function to extract text from .pdf files
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Serve the main frontend page
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Serve other static files like CSS and JS
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Print all files in the request for debugging purposes
    print(request.files.getlist('file'))  # You can print all files sent in the request
 
    # Retrieve the file from the request
    file = request.files.get('file')  # Use .get to safely access the file
 
    # Check if the file was provided
    if file is None:
        return 'No file part', 400
 
    # Get the filename from the file object
    filename = file.filename
 
    # Check if a file was selected (filename must not be empty)
    if not filename:
        return 'No selected file', 400
 
    # Validate file extension (only allow CSV files)
    if not allowed_file(filename):
        print("hello",filename)
        return 'Only CSV files are allowed', 400
 
    # Retrieve the text input (prompt) from the form
    # prompt = request.form.get('textInput')
 
    # Ensure the media folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
 
    # Define the path where the file will be saved
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
 
    # Save the file to the media folder
    file.save(file_path)
 
 
 
# "Healthcare: Develop a patient medical history summarization tool.
 
# Upload patient medical records, lab reports, or imaging reports.
# Generate concise summaries of past medical conditions, treatments, and allergies."
 
 
    print("sendint the response")
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(f'./uploads/{filename}')
    print(sample_pdf)
    response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
    print(response.text)
 
    # Return a success message with file path and text input
    return f'{response.text}'
 
    
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-1.5-flash")
# sample_pdf = genai.upload_file("C:\\Users\\aarushia\\Downloads\\sample.pdf")
# response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
# print(response.text)
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8090)