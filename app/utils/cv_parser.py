import PyPDF2
import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

class CVParser:
    def __init__(self):
        self.sections = {
            'education': r'EDUCATION',
            'experience': r'PROFESSIONAL EXPERIENCE|WORK EXPERIENCE',
            'skills': r'SKILLS',
            'projects': r'PROJECTS',
            'research': r'RESEARCH PAPERS'
        }
    
    def parse_pdf(self, file_stream):
        """Parse CV from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file_stream)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return self.extract_sections(text)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def parse_gdrive(self, file_id):
        """Parse CV from Google Drive"""
        # Implementation depends on your Google Drive setup
        pass
    
    def extract_sections(self, text):
        """Extract different sections from CV text"""
        cv_data = {}
        
        # Extract sections using regex patterns
        for section, pattern in self.sections.items():
            section_match = re.search(f"{pattern}(.*?)(?={pattern}|$)", 
                                    text, 
                                    re.DOTALL | re.IGNORECASE)
            if section_match:
                cv_data[section] = section_match.group(1).strip()
        
        # Extract contact info
        cv_data['contact'] = self.extract_contact_info(text)
        
        return cv_data
    
    def extract_contact_info(self, text):
        """Extract contact information"""
        contact = {}
        
        # Email
        email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
        if email_match:
            contact['email'] = email_match.group()
            
        # Phone
        phone_match = re.search(r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            contact['phone'] = phone_match.group()
            
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
            
        return contact