# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BliMDRHovdxzEpylScE9kU1E6ghiKQ8Z
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_doctors_info(url):
    # Send a GET request to the URL
    print("Accessing:", url)
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the doctor entries on the page
        doctor_table = soup.find('tbody')
        doctor_entries = doctor_table.find_all('tr')

        doctors_info = []

        # Extract information for each doctor entry
        for doctor_entry in doctor_entries:
            # Extract relevant information like doctor's name, specialty, degree, state, and city
            doctor_name = doctor_entry.find('td', attrs = {'data-title': "Name"}).text.strip()
            doctor_specialty = doctor_entry.find('td', attrs = {'data-title': "Special."}).text.strip()
            doctor_degree = doctor_entry.find('td', attrs = {'data-title': "Degree"}).text.strip()
            doctor_state = doctor_entry.find('td', attrs = {'data-title': "State"}).text.strip()
            doctor_city = doctor_entry.find('td', attrs = {'data-title': "City"}).text.strip()

            # Store the extracted information as a dictionary
            doctor_info = {
                'Name': doctor_name,
                'Specialization': doctor_specialty,
                'Degree': doctor_degree,
                'State': doctor_state,
                'City': doctor_city
            }

            # Append the dictionary to the list of doctors' information
            doctors_info.append(doctor_info)

        return doctors_info
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return []

# URL pattern for all tabs (pages) containing doctors in Uttar Pradesh
base_url = 'https://www.drdata.in/list-doctors.php?state=UTTAR%20PRADESH&page='

# Number of tabs (pages) to scrape (67 tabs based on your information)
num_tabs = 67

# List to store all doctors' information
all_doctors_info = []

# Loop through each tab to scrape doctor information
for page_number in range(1, num_tabs + 1):
    url = f'{base_url}{page_number}'
    doctors_info = scrape_doctors_info(url)
    all_doctors_info.extend(doctors_info)

# Convert the list of dictionaries to a DataFrame
doctors_df = pd.DataFrame(all_doctors_info)

print(doctors_df.head())  # Print the first few rows of the DataFrame

# Define the path to save the CSV file
csv_file_path = '/content/drive/MyDrive/Google_Hackathon/doctors_info.csv'

try:
    doctors_df.to_csv(csv_file_path, index=False)
    print(f"Doctor information scraped and saved to {csv_file_path}")
except Exception as e:
    print(f"Error occurred while saving to CSV: {e}")


# # Save the DataFrame to a CSV file
# doctors_df.to_csv(csv_file_path, index=False)

print(f"Doctor information scraped and saved to {csv_file_path}")