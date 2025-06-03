from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Home route to load HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Resume analysis route
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data.get('resume', '')
    job_desc_text = data.get('job_description', '')

    if not resume_text or not job_desc_text:
        return jsonify({'error': 'Both resume and job_description are required.'}), 400

    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b\w+\b', job_desc_text.lower()))

    matched = resume_words.intersection(job_words)
    score = round((len(matched) / len(job_words)) * 100, 2) if job_words else 0

    return jsonify({
        'match_score': score,
        'matched_keywords': list(matched)
    })

if __name__ == '__main__':
    app.run(debug=True)
