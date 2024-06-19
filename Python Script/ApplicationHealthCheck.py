""" Application Health Checker :- 
Problem Statement - 
    Please write a script that can check the uptime of an application and
    determine if it is functioning correctly or not. The script must accurately
    assess the application's status by checking HTTP status codes. It should be
    able to detect if the application is 'up', meaning it is functioning correctly, or
    'down', indicating that it is unavailable or not responding.
"""

import http.client
import logging
from datetime import datetime
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(filename='uptime_report.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Configuration
APP_URL = "http://yourapplication.com/healthcheck"  # URL to check application status

def check_application_status(url):
    try:
        parsed_url = urlparse(url)
        connection = http.client.HTTPConnection(parsed_url.netloc)
        connection.request("GET", parsed_url.path)
        response = connection.getresponse()

        if 200 <= response.status < 300:
            message = f"Application is UP. Status code: {response.status}"
            log_and_alert(message)
        else:
            message = f"Application is DOWN. Status code: {response.status}"
            log_and_alert(message)

        connection.close()
    except Exception as e:
        message = f"Application is DOWN. Error: {e}"
        log_and_alert(message)

def log_and_alert(message):
    print(message)
    logging.info(message)

if __name__ == "__main__":
    check_application_status(APP_URL)
