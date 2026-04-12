import csv
import os
import platform
import subprocess
import webbrowser
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# STEP 1: FILE PATH SETUP
base_path = os.getcwd()
csv_path = os.path.join(base_path, "data.csv")
pdf_path = os.path.join(base_path, "report.pdf")
# STEP 2: CREATE CSV IF MISSING
if not os.path.exists(csv_path):
    try:
        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Marks"])
            writer.writerow(["John", 85])
            writer.writerow(["Alice", 90])
            writer.writerow(["Bob", 78])
            writer.writerow(["David", 88])
            writer.writerow(["Emma", 92])
        print("✅ data.csv created successfully!")
    except:
        print("❌ Unable to create data.csv")
        exit()
# STEP 3: READ DATA SAFELY
students = []
header = ["Name", "Marks"]

try:
    with open(csv_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader, header)

        for row in reader:
            if len(row) >= 2:
                try:
                    name = str(row[0])
                    marks = int(row[1])
                    students.append([name, marks])
                except:
                    pass
except:
    print("❌ Error reading data.csv")
    exit()
# STEP 4: VALIDATE DATA
if len(students) == 0:
    print("❌ No valid data found!")
    exit()
# STEP 5: ANALYZE DATA
total = sum(s[1] for s in students)
average = total / len(students)
highest = max(students, key=lambda x: x[1])
lowest = min(students, key=lambda x: x[1])
# STEP 6: CREATE PDF
try:
    pdf = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Automated Report Generation", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Students: {len(students)}", styles['Normal']))
    elements.append(Paragraph(f"Average Marks: {average:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Highest: {highest[0]} ({highest[1]})", styles['Normal']))
    elements.append(Paragraph(f"Lowest: {lowest[0]} ({lowest[1]})", styles['Normal']))
    elements.append(Spacer(1, 20))

    table_data = [header] + students

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    pdf.build(elements)

    print("✅ Report generated successfully!")
    print("📍 Location:", pdf_path)

except:
    print("❌ Error generating PDF")
    exit()
# STEP 7: AUTO OPEN SAFELY
try:
    system = platform.system()

    if system == "Windows":
        os.startfile(pdf_path)

    elif system == "Darwin":
        subprocess.run(["open", pdf_path])

    elif system == "Linux":
        subprocess.run(["xdg-open", pdf_path])

    else:
        webbrowser.open("file://" + os.path.abspath(pdf_path))

except:
    # Final fallback (works everywhere)
    try:
        webbrowser.open("file://" + os.path.abspath(pdf_path))
        print("🌐 Opened in browser")
    except:
        print("📥 Please open report.pdf manually")
