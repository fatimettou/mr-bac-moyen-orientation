import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Streamlit input
st.title('Extract Information from Website')
matricule = st.text_input('Enter your matricule:')
url = f"https://dec.education.gov.mr/bac-21/{matricule}/info"

if matricule:
    # Path to your ChromeDriver
    service = Service('C:/Users/Fatimetou Zeine/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service)

    # Open the webpage
    driver.get(url)

    try:
        # Wait for the table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the table containing the information
        table = soup.find("table")

        # Find the span containing the result value
        result_span = soup.find("span", class_="result")

        if table:
            # Extract the table headers
            headers = [header.text.strip() for header in table.find_all("th")]

            # Extract the table rows
            rows = []
            for row in table.find_all("tr"):
                cols = [col.text.strip() for col in row.find_all("td")]
                if cols:
                    rows.append(cols)

            # Create a DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Extract the value from the span and convert it to float
            moyenne = float(result_span.text.strip()) if result_span else 0.0

            # Calculate moyenne_orientation
            if len(df) >= 3:
                moyenne_orientation = (
                    (float(df['النتيجة'][0]) * 3) +
                    (float(df['النتيجة'][1]) * 2) +
                    (float(df['النتيجة'][2]) * 1) +
                    moyenne
                ) / 7
            else:
                moyenne_orientation = None  # Handle the case with fewer than 3 rows differently

            # Add moyenne_orientation to the DataFrame
            df['moyenne_orientation'] = moyenne_orientation

            # Display the DataFrame
            st.write(df)
            st.write(f'Moyenne Orientation: {moyenne_orientation}')
        else:
            st.write("Table not found on the webpage.")
    finally:
        # Close the browser
        driver.quit()
