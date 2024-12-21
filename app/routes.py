from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app.utils.cv_parser import CVParser
from app.utils.llm_handler import LLMHandler
from app.utils.document_generator import DocumentGenerator
import os

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if job description is provided
        if 'jobDescription' not in request.form:
            return jsonify({'error': 'No job description provided'}), 400

        job_description = request.form['jobDescription']
        
        # Handle file upload
        if 'cv' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['cv']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        # Parse CV
        cv_parser = CVParser()
        cv_data = cv_parser.parse_pdf(file.stream)
        print('CV data')
        print(cv_data)
        # Generate tailored content using LLM
        llm_handler = LLMHandler()
        tailored_content = llm_handler.generate_tailored_content(cv_data, job_description)
        print('tailored content')
        print(tailored_content)
        # Generate resume document
        doc_generator = DocumentGenerator()
        output_path = doc_generator.generate_resume(cv_data['contact'], tailored_content)

        return jsonify({
            'status': 'success',
            'message': 'Resume generated successfully',
            'download_url': '/download'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/download')
def download():
    try:
        return send_file(
            os.path.join(current_app.root_path, 'static', 'generated', 'resume.docx'),
            as_attachment=True,
            download_name='tailored_resume.docx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500