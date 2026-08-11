from selenium import webdriver
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

EMS_URL = "https://krmu.icloudems.com/corecampus/index.php/"

def collect_ems_logs():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    try:
        driver = webdriver.Chrome()
        driver.get(EMS_URL)

        print("Please login to EMS using Mobile + Authenticator...")
        print("You have 60 seconds to complete login...")

        # Wait for manual login
        time.sleep(60)

        print("Login time over, collecting EMS logs...")

        # After login, collect dashboard
        dashboard = driver.page_source

        # Try opening other pages after login
        try:
            driver.get(EMS_URL + "/fee")
            time.sleep(5)
            fee_page = driver.page_source
        except:
            fee_page = "Fee page not accessible"

        try:
            driver.get(EMS_URL + "/timetable")
            time.sleep(5)
            timetable_page = driver.page_source
        except:
            timetable_page = "Timetable page not accessible"

        # Save logs
        filename = "logs/ems_logs_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("===== EMS DASHBOARD =====\n")
            f.write(BeautifulSoup(dashboard, "html.parser").get_text())

            f.write("\n\n===== EMS FEE PAGE =====\n")
            f.write(BeautifulSoup(fee_page, "html.parser").get_text())

            f.write("\n\n===== EMS TIMETABLE =====\n")
            f.write(BeautifulSoup(timetable_page, "html.parser").get_text())

        print("EMS internal logs collected successfully")

        driver.quit()
        return filename

    except Exception as e:
        print("EMS collection failed:", e)
        return None