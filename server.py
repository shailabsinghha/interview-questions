#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import json
import io
import urllib.parse
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

PORT = 8000
os.chdir('/Users/shailabsingh/Desktop/interviewQues')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/download':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                params = urllib.parse.parse_qs(post_data)
                question_ids_str = params.get('questions', [''])[0]
                question_ids = [int(x) for x in question_ids_str.split(',') if x]
                candidate_name = params.get('candidate', [''])[0]
                view_type = params.get('viewType', ['interview'])[0]
                
                doc = self.generate_docx(question_ids, candidate_name, view_type)
                
                output = io.BytesIO()
                doc.save(output)
                output.seek(0)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                filename = f"Interview_Questions_{candidate_name.replace(' ', '_')}.docx"
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.send_header('Content-Length', str(len(output.getvalue())))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(output.getvalue())
                
            except Exception as e:
                import traceback
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write((str(e) + '\n' + traceback.format_exc()).encode())
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
    
    def generate_docx(self, question_ids, candidate_name, view_type):
        questions = []
        
        with open('questions.json', 'r') as f:
            all_questions = json.load(f)
        
        for q in all_questions:
            if q['id'] in question_ids:
                questions.append(q)
        
        doc = Document()
        
        # Header with candidate name
        title = doc.add_heading('Interview Questions', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        subtitle = doc.add_paragraph(f'Candidate: {candidate_name}')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph(f'Total Questions: {len(questions)}')
        doc.add_paragraph('')
        
        if view_type == 'candidate':
            # CANDIDATE VIEW - Only questions
            doc.add_heading('Questions for Candidate', level=1)
            doc.add_paragraph('Solve these questions. No answers provided.')
            doc.add_paragraph('')
            
            for i, q in enumerate(questions, 1):
                p = doc.add_paragraph()
                p.add_run(f'{i}. ').bold = True
                p.add_run(q['question'])
                doc.add_paragraph('')
            
            # Add master copy section
            doc.add_page_break()
            doc.add_heading('Master Copy - For Reference', level=1)
            doc.add_paragraph(f'Candidate: {candidate_name}')
            doc.add_paragraph('')
            
            for i, q in enumerate(questions, 1):
                doc.add_heading(f'{i}. {q["topic"]} - {q["difficulty"]}', level=2)
                
                p = doc.add_paragraph()
                p.add_run('Question: ').bold = True
                p.add_run(q['question'])
                
                p = doc.add_paragraph()
                p.add_run('Answer: ').bold = True
                p.add_run(q['answer'])
                
                doc.add_paragraph('')
        
        else:
            # INTERVIEW VIEW - Full format
            doc.add_heading('Interview Questions - Full Details', level=1)
            doc.add_paragraph('')
            
            for i, q in enumerate(questions, 1):
                doc.add_heading(f'{i}. {q["topic"]} - {q["difficulty"]}', level=2)
                
                p = doc.add_paragraph()
                p.add_run('Topic: ').bold = True
                p.add_run(q['topic'])
                
                p = doc.add_paragraph()
                p.add_run('Difficulty: ').bold = True
                p.add_run(q['difficulty'])
                
                p = doc.add_paragraph()
                p.add_run('Question: ').bold = True
                p.add_run(q['question'])
                
                p = doc.add_paragraph()
                p.add_run('Answer: ').bold = True
                p.add_run(q['answer'])
                
                doc.add_paragraph('')
        
        return doc

print(f"Starting server at http://localhost:{PORT}")
print("Open http://localhost:8000 in your browser")
print("Select questions and click 'Download DOCX' to export")
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    httpd.serve_forever()