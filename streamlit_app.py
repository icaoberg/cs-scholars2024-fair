import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

logo_url = 'https://hubmapconsortium.org/wp-content/uploads/2019/01/HuBMAP-Logo-Color.png'
st.image(logo_url)

title = 'FAIR Assessment of HuBMAP Data'
st.write(title)

authors = 'Prince, A. Tinajero, A. Perez, L. Ku, J. Li, X. Ricano, J. Fisher, M. Edmond, J. Mitchell, A. McLeod, A. Wong, A. Cao-Berg, I.'
st.write(authors)

today = 'Today''s date'
st.write(today)

intro = '''
This is some text
'''
st.write(intro)

## DO NOT MODIFY THIS BLOCK
# Function to determine the type
def determine_type(dataset_type: str) -> str:
    if '[' in dataset_type and ']' in dataset_type:
        return 'Derived'
    else:
        return 'Primary'

@st.cache_data
def get_data() -> pd.DataFrame:
    """
    Fetch data from a predefined URL, extract the 'data' key,
    and return it as a DataFrame.

    Returns:
    pd.DataFrame: The data extracted from the 'data' key loaded into a DataFrame.
    """
    url = "https://ingest.api.hubmapconsortium.org/datasets/data-status"  # The URL to get the data from
    try:
        response = requests.get(url)  # Send a request to the URL to get the data
        response.raise_for_status()  # Check if the request was successful (no errors)
        json_data = response.json()  # Convert the response to JSON format

        # Ensure 'data' key exists in the JSON
        if 'data' in json_data:  # Check if the JSON contains the key 'data'
            df = pd.DataFrame(json_data['data'])  # Create a DataFrame using the data under 'data' key
            df = df[df['status']=='Published']
            df['dataset_status'] = df['dataset_type'].apply(determine_type)
            print("Data successfully loaded.")  # Print a message indicating success
        else:
            raise KeyError("'data' key not found in the JSON response")  # Raise an error if 'data' key is missing

        return df  # Return the DataFrame with the data
    except (ValueError, KeyError) as e:  # Catch errors related to value or missing keys
        print(f"Error loading data: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if there is an error
    except requests.RequestException as e:  # Catch errors related to the request itself
        print(f"Request failed: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if the request fails

df = get_data()
## DO NOT MODIFY THIS BLOCK

text = '## Assessment of published data'
st.write(text)

text = '### At a Glance'
st.write(text)

number_of_datasets = None
text = f'There are {number_of_datasets} published datasets'
st.write(text)

number_of_organs = None
text = f'There are {number_of_organs} organs'
st.write(text)

text = '### Datasets'
st.write(text)

#Has_contributor plot----------------------------------------------
# Count how many times each boolean appears in the data
data_counts = df['has_contributors'].value_counts()

# Start making a pie chart
# We plot a pie chart using the counts we just calculated
plt.pie(
    data_counts,  # The data to plot, which are the counts of each access level
    labels=data_counts.index,  # Labels for each pie slice, taken from the data (each type of access level)
    autopct='%1.1f%%',  # Shows percentages on the pie chart, formatted to one decimal place
    startangle=90  # Starts the first slice of the pie at the top (90 degrees on the circle)
)

# Make sure the pie chart is a perfect circle
plt.axis('equal')  # This command ensures the pie chart is not oval but a perfect circle

# Give the pie chart a title
plt.title('Whether or Not the Dataset Has a Contributor')

# Display the pie chart on the screen
plt.show()  # This command actually shows the pie chart we just created in a window
#-----------------------------------------------------------

text = '### Data access level'
st.write(text)

text = '### Dataset types'
st.write(text)

text = '### Dataset types'
st.write(text)

text = '''
## Assessment of public tool - Organ VR
### Method
### Setup
### Assessment
---
Copyright © 2024 Carnegie Mellon University. All Rights Reserved.

The [Biomedical Applications Group](https://www.psc.edu/biomedical-applications/) at the [Pittsburgh Supercomputing Center](http://www.psc.edu) in the [Mellon College of Science](https://www.cmu.edu/mcs/) at [Carnegie Mellon University](http://www.cmu.edu) and the Data Science Group at CS Scholars 2024.
'''
st.write(text)

