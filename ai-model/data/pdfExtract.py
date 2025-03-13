import pdfplumber
import json
import re
import os

# Function to clean extracted text
def clean_text(text):
    """ Removes unwanted symbols and trims extra spaces """
    return re.sub(r"[\uf0b7•]", "", text).strip()

# Function to extract faculty details from a given PDF
def extract_faculty_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        text = clean_text(text)  # Remove unwanted characters

    # Initialize faculty dictionary
    faculty = {}

    # Mapping rules for extracting key details
    mapping = {
        "Name": "name",
        "Designation": "designation",
        "Department": "department",
        "Areas of Research": "research_areas",
        "Email ID": "email",
        "Phone Number": "phone",
        "Professional Experience": "experience"
    }

    # Extract details based on mapping
    for key in mapping:
        match = re.search(rf"{key}\s*[:]\s(.+)", text)
        if match:
            value = clean_text(match.group(1))  # Clean extracted value
            if key == "Areas of Research":
                value = [v.strip() for v in value.split(",")]  # Store as list
            faculty[mapping[key]] = value
        else:
            faculty[mapping[key]] = "Not Available"  # Default value if not found

    # ✅ Fully Fixed Education Extraction (Handles multi-line data)
    def get_education(degree, text):
        """ Extracts education details with university name correctly """
        pattern = rf"{degree} in ([\w\s&]+?)(?:\nfrom|\sfrom|\sat)?\s*([\w\s&]+)"
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            course = clean_text(match.group(1))
            university = clean_text(match.group(2))
            return f"{course} from {university}"
        return "Not Available"

    # Extract education details properly
    faculty["education"] = {
        "phd": get_education("Ph.D", text),
        "mtech": get_education("M[-]?Tech", text),
        "btech": get_education("B[-]?Tech", text)
    }

    # ✅ Extract teaching subjects correctly (Remove Duplicates)
    faculty["teaching_subjects"] = list(set(re.findall(
        r"\b(Database Management Systems|Software Engineering|Software Testing Methodologies|Cloud Computing|Data Structures|Operating Systems|Artificial Intelligence)\b",
        text
    )))

    # ✅ Enhanced regex for extracting publication counts (Handles multi-line)
    def extract_publication_count(label, text):
        """ Extracts publication count for Journals, Conferences, and Patents """
        patterns = [
            rf"{label}[:]\s(\d+)",              # Journals: 6
            rf"{label}\s*-\s*(\d+)",              # Journals - 6
            rf"Published in {label}.*?\((\d+)\)", # Published in Journals (6)
            rf"{label}\s*\n\s*(\d+)"              # Handles cases where the number is on the next line
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return int(match.group(1).strip())
        return 0  # Default to 0 if not found

    faculty["publications"] = {
        "journals": extract_publication_count("Journals", text),
        "conferences": extract_publication_count("Conferences", text),
        "patents": extract_publication_count("Patents", text)
    }

    # ✅ Extract professional memberships correctly
    faculty["professional_memberships"] = re.findall(r"\b(CSI|ISTE|IAENG|ACM)\b", text)

    # ✅ Extract all roles correctly (Handles multi-line)
    all_roles = re.findall(
        r"(Department Budget Coordinator|Department Placement Coordinator|CISCO Lab Incharge|Department Admission Committee Coordinator|Research Advisor)",
        text, re.IGNORECASE | re.MULTILINE
    )
    faculty["roles"] = list(set(all_roles))  # Remove duplicates

    return faculty

# ✅ Function to process multiple PDFs
def process_multiple_pdfs(pdf_paths):
    faculty_list = []  # Store all faculty details

    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):  # Check if file exists
            faculty_data = extract_faculty_details(pdf_path)
            faculty_list.append(faculty_data)
        else:
            print(f"❌ File not found: {pdf_path}")

    # Save to JSON file
    json_path = "faculty_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"faculty": faculty_list}, f, indent=4)

    print(f"✅ All faculty data extracted and saved to {json_path}")

# Example usage: Provide multiple PDFs
pdf_files = [
    r"\T892_SRIKANTH_PROFILE.pdf",
    r"\T841_USHA_PROFILE.pdf"
]

process_multiple_pdfs(pdf_files)  # Process all PDFs