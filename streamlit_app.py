import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from datetime import datetime

logo_url = (
    "https://hubmapconsortium.org/wp-content/uploads/2019/01/HuBMAP-Logo-Color.png"
)
st.image(logo_url)

title = "# Self-assessment of HuBMAP published resources"
st.write(title)

authors = "Prince, A. Tinajero, A. Perez, L. Ku, J. Lin, X. Ricano, J. Fisher, M. Edmond, J. Mitchell, A. McLeod, A. Wong, A. Cao-Berg, I."
st.write(authors)

today = datetime.now().strftime("%Y-%m-%d")
st.write(today)

abstract = """
## Abstract
The Human BioMolecular Atlas Program (HuBMAP) aims to create a comprehensive, open, and accurate map of the human body at the cellular level. This initiative addresses the critical need for high-resolution, multi-dimensional data that can enhance our understanding of human biology and disease. To see if HuBMAP data follows the FAIR (Findable, Accessible, Interoperable, Reusable) principles, we analyzed how the data is managed and shared. We looked at the standards used for metadata, how easy it is to access the data, how well the data works with other datasets, and how reusable the data is. Our review showed that HuBMAP data is fairly straightforward to find thanks to metadata and strong search tools. The data can be accessed through user-friendly platforms and APIs, making it easy for anyone to use. The data is also designed to work well with other datasets due to standardized formats. Plus, the data is highly reusable, supported by clear licensing and thorough documentation. By making data findable, accessible, interoperable, and reusable, HuBMAP helps scientific discovery and sets a high standard for other big biological data projects.
"""
st.write(abstract)

intro = """
## Introduction
The Human BioMolecular Atlas Program (HuBMAP) aims to create an immersive experience of a 3D-map representation of the human body, improving access to data of the human body and developing methods for tissue interrogation applicable to other research areas. To commence its first phase, HuBMAP achieved significant highlights, including standardizing protocols, innovating imaging and sequencing techniques, and establishing reliable data. These efforts led to the creation of high-resolution molecules and of the nine major organ systems. Researchers are working together to expand the map from a 2D to a 3D environment, including factors such as age and ethnicity.
Looking ahead, the main objective of HuBMAP is to provide freely accessible data via its online portal. The program focuses on investigating changes in individual cells and detecting diseases to prevent the harms of healthy aging. Understanding these details will help scientists develop better drugs targeting multiple organs and predict disease outcomes and progression more accurately in clinical settings. The HuBMAP production phase (2022–2026) has several goals. Additionally, it aims to generate reference datasets using new technologies, emphasizing building 3D maps and collecting data from diverse donors representing a range of demographic features (sex, race or ethnicity, and age). Its main purpose is to overcome challenges and gaps. Finally, it aims to improve metadata standards, analytical and visualization tools, and data integration and interpretation to enhance the tissue atlases of the human body through collaborative efforts.
"""
st.write(intro)


## DO NOT MODIFY THIS BLOCK
# Function to determine the type
def determine_type(dataset_type: str) -> str:
    if "[" in dataset_type and "]" in dataset_type:
        return "Derived"
    else:
        return "Primary"


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
        if "data" in json_data:  # Check if the JSON contains the key 'data'
            df = pd.DataFrame(
                json_data["data"]
            )  # Create a DataFrame using the data under 'data' key
            df = df[df["status"] == "Published"]
            df["dataset_status"] = df["dataset_type"].apply(determine_type)
            print("Data successfully loaded.")  # Print a message indicating success
        else:
            raise KeyError(
                "'data' key not found in the JSON response"
            )  # Raise an error if 'data' key is missing

        return df  # Return the DataFrame with the data
    except (ValueError, KeyError) as e:  # Catch errors related to value or missing keys
        print(f"Error loading data: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if there is an error
    except requests.RequestException as e:  # Catch errors related to the request itself
        print(f"Request failed: {e}")  # Print the error message
        return pd.DataFrame()  # Return an empty DataFrame if the request fails


df = get_data()
## DO NOT MODIFY THIS BLOCK

text = "## Assessment of published data"
st.write(text)

text = "### At a Glance"
st.write(text)

number_of_datasets = None
text = f"There are {number_of_datasets} published datasets"
st.write(text)


number_of_organs = None
text = f"There are {number_of_organs} organs"
st.write(text)

text = "### Datasets"
st.write(text)

# print table
st.write(df)

# --------------------------------------------------------------------
# Calculate value counts and get the top 10 research group names
value_counts = df["group_name"].value_counts()
top_10_value_counts = value_counts.nlargest(7)

# Calculate "Others" category
others_count = value_counts.iloc[7:].sum()
if others_count > 0:
    top_10_value_counts["Others"] = others_count

# Plotting in Streamlit
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    top_10_value_counts,
    autopct="%1.1f%%",  # Add percentages
    explode=[
        0.1 if value == max(top_10_value_counts) else 0 for value in top_10_value_counts
    ],  # Explode largest slice
    colors=plt.cm.tab20.colors[
        : len(top_10_value_counts)
    ],  # Use tab20 colormap for colors
    shadow=True,  # Add shadow
    startangle=90,  # Rotate start angle
    textprops=dict(color="w"),
)  # Text color for percentages

ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
# Create custom legend
legend_labels = top_10_value_counts.index.tolist()
ax.legend(
    wedges,
    legend_labels,
    title="Groups",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

ax.set_title("Group names")  # Add title to the pie chart
# Display plot using Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
from wordcloud import WordCloud

text = " ".join(df["group_name"].str.replace(" ", "_").tolist())

# Create the Word Cloud
wordcloud = WordCloud(
    width=200,
    height=200,
    background_color="white",
    collocations=False,
).generate(text)


def grey_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    return "hsl(230,100%%, %d%%)" % np.random.randint(49, 51)


# change the color setting
wordcloud.recolor(color_func=grey_color_func)

# Create a figure
fig, ax = plt.subplots(
    figsize=(25, 25)
)  # Create a figure of size 10 inches by 5 inches

# Display the Word Cloud
ax.imshow(wordcloud, interpolation="bilinear")  # Display the word cloud image
ax.axis("off")  # Turn off the axis because we don't need it for the word cloud
# Display plot using Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Count how many times each boolean appears in the column: Has data
data_counts = df["has_data"].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    data_counts, labels=data_counts.index, autopct="%1.1f%%", startangle=90
)
ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title("Has data")

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Count how many times each boolean appears in the data: Has contributors

data_counts = df['has_contributors'].value_counts()

# Plot pie chart using Streamlit
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    data_counts,  # This is the data we're using — the counts of each boolean
    labels=data_counts.index,  # These are the labels for each piece of the pie
    autopct='%1.1f%%',  # This makes sure that each piece of the pie shows its percentage like "25.0%"
    startangle=90,  # This starts the first piece of the pie at the top of the circle
    colors=plt.cm.tab20.colors[:len(data_counts)],  # Use tab20 colormap for colors
    explode=[0.1 if value == max(data_counts) else 0 for value in data_counts],  # Explode largest slice
    shadow=True,  # Add shadow
)


ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title('Percentage of Datasets That Has Contributors')

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

text = "### Data access level"
st.write(text)

# --------------------------------------------------------------------
# Count how many times each access level appears in the data
data_counts = df["data_access_level"].value_counts()


# Count how many times each access level appears in the data
data_counts = df["data_access_level"].value_counts()

# Display text using st.write()
# Plot pie chart using matplotlib and display with st.pyplot()
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    data_counts, labels=data_counts.index, autopct="%1.1f%%", startangle=90
)
ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title("Distribution of Data Access Levels")

# Display the plot in Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------

text = "### Dataset types"
st.write(text)

text = "### Dataset types"
st.write(text)

text = """
## Assessment of public tool - Organ VR
### Method
### Setup
### Assessment
---
References: \n

* Jain, S., Pei, L., Spraggins, J.M. et al. Advances and prospects for the Human BioMolecular Atlas Program (HuBMAP). Nat Cell Biol 25, 1089–1100 (2023). https://doi.org/10.1038/s41556-023-01194-w \n
* Wilkinson, M., Dumontier, M., Aalbersberg, I. et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3, 160018 (2016). https://doi.org/10.1038/sdata.2016.18 \n
* Bueckle A, Qing C, Luley S, Kumar Y, Pandey N and Börner K (2023) The HRA Organ Gallery affords immersive superpowers for building and exploring the Human Reference Atlas with virtual reality. Front. Bioinform. 3:1162723. doi: 10.3389/fbinf.2023.1162723 \n
* HuBMAP Consortium. The human body at cellular resolution: the NIH Human Biomolecular Atlas Program. Nature 574, 187–192 (2019). https://doi.org/10.1038/s41586-019-1629-x \n

---
Copyright © 2024 Carnegie Mellon University. All Rights Reserved.

The [Biomedical Applications Group](https://www.psc.edu/biomedical-applications/) at the [Pittsburgh Supercomputing Center](http://www.psc.edu) in the [Mellon College of Science](https://www.cmu.edu/mcs/) at [Carnegie Mellon University](http://www.cmu.edu) and the Data Science Group at CS Scholars 2024.
"""
st.write(text)
