import openai
import os
from typing import Dict, List
from openai import OpenAI
class LLMHandler:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client =  OpenAI(
        organization='org-Qf0ZgkD7gMaJ8A44ouvmZkvt',
        )
    def generate_tailored_content(self, cv_data: Dict, job_description: str) -> Dict:
        """Generate resume content tailored to job description"""
        
        # Static sections - minimal modification needed
        static_sections = ['education', 'skills']
        
        # Dynamic sections - need STAR method application
        dynamic_sections = ['experience', 'projects', 'research_papers']
        
        system_prompt = """
        You are an expert resume writer who specializes in the STAR method. 
        For dynamic sections (experience, projects, research), create impactful bullet points that:
        1. Start with strong action verbs
        2. Incorporate specific technologies and tools
        3. Include measurable results (%, metrics, improvements)
        4. Condense STAR (Situation, Task, Action, Result) into single, impactful statements
        5. Align with the job description requirements
        """
        
        tailored_content = {}
        
        # Handle static sections
        for section in static_sections:
            if section in cv_data:
                tailored_content[section] = self._format_static_section(
                    section, 
                    cv_data[section], 
                    job_description
                )
        
        # Handle dynamic sections with STAR method
        for section in dynamic_sections:
            if section in cv_data:
                tailored_content[section] = self._format_star_section(
                    section, 
                    cv_data[section], 
                    job_description
                )
        
        return tailored_content
    
    def _format_star_section(self, section: str, content: str, job_description: str) -> str:
        """Format dynamic sections using STAR method"""
        client =  OpenAI(
        organization='org-Qf0ZgkD7gMaJ8A44ouvmZkvt',
        )
        prompts = {
            'experience': f"""
                Transform these experiences into STAR-method bullet points:
                {content}
                
                Job Description:
                {job_description}
                
                Requirements:
                - Start each bullet with a strong action verb
                - Include specific technologies used
                - Highlight measurable results
                - Limit to 3-4 bullet points per role
                - Focus on achievements relevant to the job description
                """,
            
            'projects': f"""
                Transform these projects into STAR-method bullet points:
                {content}
                
                Job Description:
                {job_description}
                
                Requirements:
                - Emphasize technical implementation details
                - Include specific technologies and methodologies
                - Highlight measurable outcomes
                - Focus on projects most relevant to the job
                - Limit to 2-3 most relevant projects
                """,
            
            'research_papers': f"""
                Transform these research papers into impactful bullet points:
                {content}
                
                Job Description:
                {job_description}
                
                Requirements:
                - Emphasize technical contributions
                - Highlight impact and innovations
                - Include relevant technologies and methodologies
                - Focus on research relevant to the job
                - Limit to most significant papers
                """
        }
        
        try:
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {"role": "system", "content": "You are an expert resume writer specializing in STAR method."},
            #         {"role": "user", "content": prompts.get(section, "")}
            #     ],
            #     temperature=0.7
            # )
            response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in STAR method."},
                    {"role": "user", "content":  prompts.get(section, "")}
                ],
                temperature=0.7
            )
            print(response)
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def _format_static_section(self, section: str, content: str, job_description: str) -> str:
        """Format static sections with minimal modification"""
        try:
            response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "Format this section clearly and concisely."},
                    {"role": "user", "content": f"Organize this {section} content, keeping relevant items for the job:\n{content}\n\nJob Description:\n{job_description}"}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating content: {str(e)}"