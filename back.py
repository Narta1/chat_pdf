from flask import Flask, request, jsonify
import openai
import pdfplumber
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    file = request.files['pdf']
    query = request.form['query']
    
    
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Text from the PDF: {text}\n\nUser Query: {query}"}
        ]
    )

    
    response_message = response.choices[0].message['content']
    print(response_message)

    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)
