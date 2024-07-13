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

today = datetime.now().strftime('%Y-%m-%d')
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

#print table
st.write(df)

# --------------------------------------------------------------------
# Calculate value counts and get the top 10 research group names
value_counts = df['group_name'].value_counts()
top_10_value_counts = value_counts.nlargest(10)
# Calculate "Others" category
others_count = value_counts.iloc[10:].sum()
if others_count > 0:
    top_10_value_counts['Others'] = others_count

# Plotting in Streamlit
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(top_10_value_counts,
                                  autopct='%1.1f%%',  # Add percentages
                                  explode=[0.1 if value == max(top_10_value_counts) else 0 for value in top_10_value_counts],  # Explode largest slice
                                  colors=plt.cm.tab20.colors[:len(top_10_value_counts)],  # Use tab20 colormap for colors
                                  shadow=True,  # Add shadow
                                  startangle=90,  # Rotate start angle
                                  textprops=dict(color="w"))  # Text color for percentages

ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Group names')  # Add title to the pie chart
# Display plot using Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Count how many times each boolean appears in the data
data_counts = df['has_data'].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts,
                                  labels=data_counts.index.map({True: 'Yes', False: 'No'}),
                                  autopct='%1.1f%%',
                                  startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Has data')

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Count how many times each boolean appears in the data
data_counts = df['has_contributors'].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts,
                                  labels=data_counts.index.map({True: 'Yes', False: 'No'}),
                                  autopct='%1.1f%%',
                                  startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Has Contributors')

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

text = '### Data access level'
st.write(text)

# --------------------------------------------------------------------
# Count how many times each access level appears in the data
data_counts = df['data_access_level'].value_counts()


# Count how many times each access level appears in the data
data_counts = df['data_access_level'].value_counts()

# Display text using st.write()
# Plot pie chart using matplotlib and display with st.pyplot()
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(data_counts,
                                  labels=data_counts.index,
                                  autopct='%1.1f%%',
                                  startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Distribution of Data Access Levels')

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

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
