import requests
import time
import sys
from xml.etree import ElementTree as ET

# Configuration
API_URL = "https://qualysapi.qualys.com/api/2.0/fo/report/"  # Replace with your Qualys platform URL
USERNAME = "your_username"  # Replace with your Qualys username
PASSWORD = "your_password"  # Replace with your Qualys password
TEMPLATE_ID = "123456"  # Replace with your report template ID
OUTPUT_FILE = "vulnerability_report.csv"

# Headers for API requests
headers = {
    "X-Requested-With": "Python Script",
    "Content-Type": "text/xml",
}

# Step 1: Launch a report
def launch_report():
    payload = {
        "action": "launch",
        "template_id": TEMPLATE_ID,
        "output_format": "csv",
        "report_title": "Automated Vulnerability Report",
    }
    try:
        response = requests.post(
            API_URL,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            params=payload
        )
        response.raise_for_status()
        # Parse XML response to get report ID
        root = ET.fromstring(response.text)
        report_id = root.find(".//VALUE").text
        print(f"Report launched successfully. Report ID: {report_id}")
        return report_id
    except requests.exceptions.RequestException as e:
        print(f"Error launching report: {e}")
        sys.exit(1)
    except AttributeError:
        print("Error parsing report ID from response")
        sys.exit(1)

# Step 2: Check report status
def check_report_status(report_id):
    payload = {
        "action": "list",
        "id": report_id,
    }
    while True:
        try:
            response = requests.get(
                API_URL,
                auth=(USERNAME, PASSWORD),
                headers=headers,
                params=payload
            )
            response.raise_for_status()
            root = ET.fromstring(response.text)
            status = root.find(".//STATUS/STATE").text
            print(f"Report status: {status}")
            if status == "Finished":
                return True
            elif status in ["Error", "Cancelled"]:
                print("Report generation failed or was cancelled")
                sys.exit(1)
            time.sleep(30)  # Wait before polling again
        except requests.exceptions.RequestException as e:
            print(f"Error checking report status: {e}")
            sys.exit(1)

# Step 3: Download the report
def download_report(report_id):
    payload = {
        "action": "fetch",
        "id": report_id,
    }
    try:
        response = requests.get(
            API_URL,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            params=payload
        )
        response.raise_for_status()
        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)
        print(f"Report downloaded successfully to {OUTPUT_FILE}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading report: {e}")
        sys.exit(1)

def main():
    # Launch the report
    report_id = launch_report()
    
    # Check status until finished
    if check_report_status(report_id):
        # Download the report
        download_report(report_id)

if __name__ == "__main__":
    main()