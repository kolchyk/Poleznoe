# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:54:31 2024

@author: sereg
"""

import requests
import pandas as pd

# Function to fetch data page by page using cursor
def fetch_data_with_cursor(api_host, headers, start_date, end_date):
    documents = []  # List to hold all documents across pages
    cursor = None  # Initialize cursor

    # Loop until there are no more pages to fetch
    while True:
        # Build the API request URL
        url = f"{api_host}/api/v2/incoming-documents?date_created_from={start_date}&date_created_to={end_date}"
        if cursor:  # Append the cursor to the URL if present
            url += f"&cursor={cursor}"

        # Make the GET request to the API
        response = requests.get(url, headers=headers)

        # Handle unsuccessful response
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break

        # Convert the JSON string to a Python dictionary
        response_data = response.json()  # Using .json() method directly

        # Extend the documents list with the current page of documents
        documents.extend(response_data.get('documents', []))

        # Check for the 'next_cursor' or similar field in the response
        cursor = response_data.get('next_cursor')
        if not cursor:  # Break the loop if there's no next cursor
            break

    return documents

# API configuration
API_HOST = "https://vchasno.ua"
API_TOKEN = "GgPq3irGr2pzbeor1-0bGXnexnSa0OPbHzVi"
headers = {"Authorization": API_TOKEN}
start_date = "2020-01-01"
end_date = "2025-01-31"

# Fetch all documents with pagination support
all_documents = fetch_data_with_cursor(API_HOST, headers, start_date, end_date)

# Convert the list of all documents to a DataFrame
documents_df = pd.DataFrame(all_documents)

filtered_df = documents_df[documents_df['status'] != 7008]

