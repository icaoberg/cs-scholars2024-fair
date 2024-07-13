import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

# logo_url = ''
# st.image(logo_url)

title = '# Add Title'
st.write(title)

authors = 'Add authors'
st.write(authors)

today = 'Today''s date'
st.write(today)

intro = '''
The Human BioMolecular Atlas Program (HuBMAP) aims to create an immersive experience of a 3D-map representation of the human body, improving access to data of the human body and developing methods for tissue interrogation applicable to other research areas. To commence its first phase, HuBMAP achieved significant highlights, including standardizing protocols, innovating imaging and sequencing techniques, and establishing reliable data. These efforts led to the creation of high-resolution molecules and of the nine major organ systems. Researchers are working together to expand the map from a 2D to a 3D environment, including factors such as age and ethnicity.
Looking ahead, the main objective of HuBMAP is to provide freely accessible data via its online portal. The program focuses on investigating changes in individual cells and detecting diseases to prevent the harms of healthy aging. Understanding these details will help scientists develop better drugs targeting multiple organs and predict disease outcomes and progression more accurately in clinical settings. The HuBMAP production phase (2022–2026) has several goals. Additionally, it aims to generate reference datasets using new technologies, emphasizing building 3D maps and collecting data from diverse donors representing a range of demographic features (sex, race or ethnicity, and age). Its main purpose is to overcome challenges and gaps. Finally, it aims to improve metadata standards, analytical and visualization tools, and data integration and interpretation to enhance the tissue atlases of the human body through collaborative efforts.
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
'''
st.write(text)
