import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def make_pdf(path="backend/data/knowledge.pdf"):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Initialize the PDF canvas
    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica-Bold", 14)
    lines = [
        "Insurance Agency Customer Care Knowledge Base",
        "",
        "Q: How do I file a claim?",
        "A: Call our claims line or submit through the portal. Keep photos and receipts.",
        "",
        "Q: What is a deductible?",
        "A: The amount you pay out of pocket before insurance starts paying.",
        "",
        "Q: How do I add a driver to my auto policy?",
        "A: Provide name, DOB, license number, and effective date. We'll send a quote.",
        "",
        "Q: What documents do you need for a new policy?",
        "A: ID proof, address proof, vehicle/home details, and prior insurance history.",
        "",
        "Q: Can I cancel my policy at any time?",
        "A: Yes, but some policies carry a short-rate cancellation fee if ended early.",
        "",
        "Q: When is my premium payment due?",
        "A: Payments are typically due on the 1st of every month via autopay or portal."

]
        
# Write the lines to the PDF
    for line in lines:
        if "Q:" in line:
            text.setFont("Helvetica-Bold", 12)
        else:
            text.setFont("Helvetica", 12)
        text.textLine(line)
        
    c.drawText(text)
    c.save()
    print(f"Successfully generated: {path}")

if __name__ == "__main__":
    make_pdf()
    
