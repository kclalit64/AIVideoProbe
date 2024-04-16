from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Function to generate PDF with technical section
def generate_pdf():
    doc = SimpleDocTemplate("interview_sections.pdf", pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50, \
                            title="Interview Sections", showBoundary=1)
    styles = getSampleStyleSheet()

    # Define content for the PDF
    content = []

    # Insert Section 1 title
    section1_title = Paragraph("<b><i>Section 1</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)

    # Add a spacer for gap
    content.append(Spacer(1, 20))

    # Page 1: Technical Section
    content.extend(generate_section("Technical Section", 85, [
        ("1", "Python Programming", "Good understanding", "Official Python Documentation"),
        ("2", "Data Structures", "Needs improvement", "GeeksforGeeks"),
        ("3", "Algorithms", "Excellent", "Introduction to Algorithms."),
        ("4", "Database Management", "Moderate knowledge", "SQL Documentation"),
        ("5", "Web Development", "Basic understanding", "MDN Web Docs")
    ]))

    # Page break
    content.append(PageBreak())

    section1_title = Paragraph("<b><i>Section 2</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)

    content.append(Spacer(1, 20))
    # Page 2: Behavioural Skills Section
    content.extend(generate_section("Behavioural Skills", 75, [
        ("1", "Communication", "Proven effective communication", "Example resource"),
        ("2", "Teamwork", "Collaborative team player", "Example resource"),
        ("3", "Problem Solving", "Strong problem-solving abilities", "Example resource"),
        ("4", "Leadership", "Inspiring natural leadership", "Example resource"),
        ("5", "Adaptability", "Quickly adapts to situations", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())

    section1_title = Paragraph("<b><i>Section 3</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))

    # Page 3: Problem-Solving and Critical Thinking
    content.extend(generate_section("Problem-Solving and Critical Thinking", 90, [
        ("1", "Analytical Thinking", "Analytical problem-solving", "Example resource"),
        ("2", "Creativity", "Ability to think outside the box", "Example resource"),
        ("3", "Decision Making", "Decisive under pressure", "Example resource"),
        ("4", "Critical Thinking", "Strong critical thinking skills", "Example resource"),
        ("5", "Logical Reasoning", "Systematic problem-solving", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())
    section1_title = Paragraph("<b><i>Section 4</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))
    # Page 4: Cultural Fit
    content.extend(generate_section("Cultural Fit", 80, [
        ("1", "Team Collaboration", "Works well in diverse teams", "Example resource"),
        ("2", "Company Values Alignment", "Cultural alignment", "Example resource"),
        ("3", "Adaptability", "Adaptable to company culture", "Example resource"),
        ("4", "Respect for Diversity", "Fosters diversity", "Example resource"),
        ("5", "Open Communication", "Fosters open communication", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())
    section1_title = Paragraph("<b><i>Section 5</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))

    # Page 5: Work Experience and Achievements
    content.extend(generate_section("Work Experience and Achievements", 95, [
        ("1", "Project Management", "Complex project management", "Example resource"),
        ("2", "Technical Skills", "Proven technical expertise", "Example resource"),
        ("3", "Leadership Experience", "Team milestone leadership", "Example resource"),
        ("4", "Industry Recognition", "Award-winning contributions", "Example resource"),
        ("5", "Contributions to Community", "Community initiative involvement", "Example resource")
    ]))

    # Build PDF
    doc.build(content)

# Function to generate section content
def generate_section(title, score, topics):
    styles = getSampleStyleSheet()

    content = []

    # Heading with blue color box
    heading_style = styles["Heading1"]
    heading_style.textColor = colors.white
    heading_style.backColor = colors.blue
    heading_style.alignment = 1  # Center alignment
    content.append(Paragraph(title, heading_style))

    # Score section
    score_paragraph = Paragraph(f"Score: {score}/100", styles["Heading2"])
    content.append(score_paragraph)

    # Add 25px top padding between Score section and table
    content.append(Spacer(1, 25))

    # Side heading for Evaluation Metrics
    evaluation_heading_style = styles["Heading2"]
    evaluation_heading_style.alignment = 0  # Left alignment
    content.append(Paragraph("Evaluation Metrics", evaluation_heading_style))

    # Table data
    table_data = [["Sr. No", "Topic", "Remarks", "Resources"]]
    for sr_no, topic, remarks, resources in topics:
        table_data.append([sr_no, topic, remarks, resources])

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black),
                              ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the entire table
                              ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around each cell
                              ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)])  # Inner grid lines

    # Create table
    section_table = Table(table_data)
    section_table.setStyle(table_style)

    # Set width for all columns
    col_widths = [60, 150, 150, 150]
    section_table._argW = col_widths

    # Set row heights
    section_table.setStyle(TableStyle([('SIZE', (0, 0), (-1, -1), 10)]))

    # Enable word wrapping for all columns
    section_table.setStyle(TableStyle([('WORDWRAP', (0, 0), (-1, -1), True)]))

    # Add table to content
    content.append(section_table)

    # Side heading for Summary
    summary_heading_style = styles["Heading2"]
    summary_heading_style.alignment = 0  # Left alignment
    content.append(Paragraph("Summary", summary_heading_style))

    return content

# Generate PDF
generate_pdf()

print("PDF generated successfully.")
