from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class ReportService:
    @staticmethod
    def generate_pdf(filename: str, title: str, sections: list):
        """
        sections: list of dict {'title': str, 'body': str}
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 12))

        # Sections
        for section in sections:
            if section.get('title'):
                story.append(Paragraph(section['title'], styles['Heading2']))
                story.append(Spacer(1, 6))
            
            # Helper to handle newlines in body
            body_text = section['body'].replace('\n', '<br/>')
            story.append(Paragraph(body_text, styles['Normal']))
            story.append(Spacer(1, 12))

        doc.build(story)
        return filename
