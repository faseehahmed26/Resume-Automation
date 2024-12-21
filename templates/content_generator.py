from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

class ResumeContentGenerator:
    def __init__(self, template_path='templates/resume_template.docx'):
        self.template_path = template_path

    def format_education(self, education_data):
        """Format education section with proper alignment and bullets"""
        formatted = ""
        for edu in education_data:
            formatted += f"{edu['institution']}, {edu['location']}, {edu['degree']}\n"
            formatted += f"Coursework: {edu['coursework']}\n"
            formatted += f"GPA: {edu['gpa']}\n\n"
        return formatted

    def format_skills(self, skills_data):
        """Format skills section with categories"""
        formatted = ""
        for category, skills in skills_data.items():
            formatted += f"{category}: {', '.join(skills)}\n"
        return formatted

    def format_experience(self, experience_data):
        """Format experience section with bullets"""
        formatted = ""
        for exp in experience_data:
            formatted += f"{exp['company']}, {exp['location']} - {exp['position']}\n"
            formatted += f"{exp['date']}\n"
            for bullet in exp['bullets']:
                formatted += f"• {bullet}\n"
            formatted += "\n"
        return formatted

    def format_projects(self, projects_data):
        """Format projects section"""
        formatted = ""
        for project in projects_data:
            formatted += f"{project['name']}\n"
            for bullet in project['bullets']:
                formatted += f"• {bullet}\n"
            formatted += "\n"
        return formatted

    def generate_resume(self, data):
        """Generate resume with the provided data"""
        doc = Document(self.template_path)
        
        # Replace all placeholders
        for paragraph in doc.paragraphs:
            for key, value in data.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in paragraph.text:
                    if key == 'education':
                        value = self.format_education(value)
                    elif key == 'skills':
                        value = self.format_skills(value)
                    elif key == 'experience':
                        value = self.format_experience(value)
                    elif key == 'projects':
                        value = self.format_projects(value)
                    
                    paragraph.text = paragraph.text.replace(placeholder, value)

        return doc

# Example usage:
if __name__ == "__main__":
    sample_data = {
        "full_name": "Mohammad Faseeh Ahmed",
        "email": "mm9514@rit.edu",
        "phone": "+1 585 202 5217",
        "linkedin": "LinkedIn",
        "github": "Github",
        "portfolio": "Portfolio",
        "kaggle": "Kaggle",
        "tableau": "Tableau",
        "education": [
            {
                "institution": "Rochester Institute of Technology",
                "location": "Rochester, NY",
                "degree": "M.S in Data Science",
                "coursework": "Neural Networks, Software Engineering for Data Science, Applied Statistics",
                "gpa": "3.84/4.00"
            }
        ],
        "skills": {
            "Programming Languages": ["Java", "Python", "C++", "R", "JavaScript"],
            "Frameworks": ["PyTorch", "Keras", "Scikit-learn"],
            "Databases": ["SQL", "MongoDB", "PostgreSQL"]
        },
        # Add other sections as needed
    }

    generator = ResumeContentGenerator()
    doc = generator.generate_resume(sample_data)
    doc.save('output_resume.docx')