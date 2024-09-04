import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Streamlit page configuration
st.set_page_config(page_title="Netflix Dashboard", page_icon="📺", layout="centered", initial_sidebar_state="auto")

# Adding custom CSS styles
st.markdown(
    """
    <style>
    /* Background color and text color */
    body { background-color: #121212; color: #e0e0e0; }

    /* Header and sidebar background colors */
    .css-1l02d9a, .css-1rs6osf { background-color: #1e1e1e; }

    /* Sidebar text color */
    .css-1f1d60w { color: #e0e0e0; }

    /* Button and input styles */
    .css-1o4ux7r, .css-1n1v10h { background-color: #333; color: #e0e0e0; }
    .stButton>button { background-color: #333; color: #e0e0e0; border: none; }
    .stTextInput>div>input { background-color: #333; color: #e0e0e0; border: 1px solid #555; }
    .stSelectbox>div>select { background-color: #333; color: #e0e0e0; border: 1px solid #555; }

    /* Adjust layout */
    .css-1y4p8pa { width: 100%; padding: 0px; padding-right: 1rem; padding-left: 2rem; max-width: 100%; }
    .css-1544g2n { padding: 2rem 1rem 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inject CSS to style the sidebar and main page
st.markdown(
    """
    <style>
    /* Sidebar styles */
    .css-1d391kg {
        background: linear-gradient(white 10px, transparent 10px) center/100% 20px;
        border-radius: 0 20px 20px 0; /* Curved right side */
        box-shadow: 4px 0 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
        padding: 20px; /* Padding inside sidebar */
    }
    
    /* Sidebar heading */
    .css-1d391kg .css-1p4fd98 {
        background-color: #333; /* Dark background for heading */
        color: #fff; /* White text color */
        border-radius: 10px; /* Curved corners for heading background */
        padding: 10px; /* Padding around heading */
    }

    /* Main page background */
    .css-1outpf9 {
        background: linear-gradient(
            0deg,
            #ffffff 25%,
            #f0f0f0 25%,
            #f0f0f0 50%,
            #ffffff 50%,
            #ffffff 75%,
            #f0f0f0 75%,
            #f0f0f0
        );
        background-size: 100% 40px; /* Stripe size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up Streamlit app title
st.title(":film_frames::film_projector: Netflix Data Dashboard :tv:")

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# Create new columns for years
df['year'] = pd.to_datetime(df['release_year'], errors='coerce').dt.year


st.markdown(
    """
    <style>
    .custom-box {
        border-radius: 15px; /* Curved corners */
        border: 2px solid #ddd; /* Border color */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
        padding: 20px; /* Padding inside the box */
        background-color: #f9f9f9; /* Light background color */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
		background: linear-gradient(
            0deg,
            #ffffff 25%,
            #f0f0f0 25%,
            #f0f0f0 50%,
            #ffffff 50%,
            #ffffff 75%,
            #f0f0f0 75%,
            #f0f0f0
        );
        background-size: 100% 10px;
    }
    .custom-box h3 {
        margin: 0; /* Remove margin for heading */
        padding: 10px; /* Padding around heading */
        background-color: #333; /* Background color for heading */
        color: #fff; /* Text color for heading */
        text-align: center; /* Center-align the heading */
        border-radius: 10px; /* Curved corners for heading background */
        width: 100%; /* Ensure the background color spans the width */
		background: linear-gradient(#333 10px, #333 10px) center/100% 20px;
        border-radius: 20px 20px 20px 20px; /* Curved right side */
        box-shadow: 4px 0 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
        padding: 20px; /* Padding inside sidebar */
    }
    .custom-box p {
        margin: 10px 0 0; /* Margin for value */
        font-size: 48px; /* Font size for value */
        color: #555; /* Value color */
        font-weight: bold; /* Make value bold */
    }
    .column-wrapper {
        display: flex;
        justify-content: space-between;
    }
    .column-wrapper > div {
        flex: 1;
        margin: 0 20px; /* Spacing between boxes */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create layout columns
col1, col2, col3 = st.columns(3)

# Display basic statistics with custom styling
with col1:
    st.markdown('<div class="custom-box"><h3>Contents</h3><p>{}</p></div>'.format(df['show_id'].count()), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-box"><h3>Movies</h3><p>{}</p></div>'.format(df[df['type'] == "Movie"]['type'].count()), unsafe_allow_html=True)

with col3:
    st.markdown('<div class="custom-box"><h3>TV Shows</h3><p>{}</p></div>'.format(df[df['type'] == "TV Show"]['type'].count()), unsafe_allow_html=True)
st.divider()
# Sidebar filters
st.sidebar.header('Filters')
# st.sidebar.button("Reset")  # Button to reset filters

# Filter options

countries = st.sidebar.multiselect("Country", options=df["country"].dropna().unique())
types = st.sidebar.multiselect("Type", options=df["type"].dropna().unique())
years = st.sidebar.multiselect("Release Year", options=df["year"].dropna().astype(int).unique())
#categories = st.sidebar.multiselect("Category", options=df["listed_in"].dropna().str.split(',', expand=True).stack().unique())

# Filter the dataframe based on selected filters
df_filtered = df.copy()
if years:
    df_filtered = df_filtered[df_filtered["year"].isin(years)]
if countries:
    df_filtered = df_filtered[df_filtered["country"].isin(countries)]
if types:
    df_filtered = df_filtered[df_filtered["type"].isin(types)]
# if categories:
    # df_filtered['categories'] = df_filtered['listed_in'].str.split(',', expand=True).stack()
    # df_filtered = df_filtered[df_filtered['categories'].isin(categories)]

# Drop the temporary 'categories' column
df_filtered.drop(columns=['categories'], inplace=True, errors='ignore')

# Display filtered table
# st.write("Filtered Table")
# st.write(df_filtered.head(10))

# Helper function to check and display no data message
def show_no_data_message():
    st.write("No data available to display.")

# Visualizations
# Categories Treemap
st.header('Categories in Netflix')
if 'listed_in' in df_filtered.columns and not df_filtered['listed_in'].dropna().empty:
    category_data = df_filtered['listed_in'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
    category_counts = category_data.value_counts()
    category_df = pd.DataFrame({'Category': category_counts.index, 'Count': category_counts.values})
    fig = px.treemap(category_df, path=['Category'], values='Count')
    st.plotly_chart(fig, use_container_width=True)
else:
    show_no_data_message()

st.divider()
# Countries of Origin
st.header('Countries of Origin')
if 'country' in df_filtered.columns and not df_filtered['country'].dropna().empty:
    # Process country data
    country_data = df_filtered['country'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
    country_counts = country_data.value_counts()
    country_df = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})

    # Create the scatter geo plot
    fig = px.scatter_geo(
        country_df,
        locations='Country',
        locationmode='country names',
        size='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.Jet,  # Use the Plasma color scale for a more vibrant appearance
        size_max=50,
        title='Distribution of Content by Country of Origin'
    )

    # Update layout for better visual clarity
    fig.update_layout(
        geo=dict(
            showcoastlines=True,
            coastlinecolor="DarkBlue",
            showland=True,
            landcolor="LightGray",  # Changed to LightGray for a softer contrast
            showocean=True,
            oceancolor="teal"
        ),
        coloraxis_colorbar=dict(
            title='Count',
            tickvals=[0, 10, 20, 30, 40, 50],  # Adjust tick values based on your data
            ticktext=['0', '10', '20', '30', '40', '50']
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    show_no_data_message()
	
st.divider()	
# Pie chart for content type
col1, col2 = st.columns(2)
with col1:
    st.header('Content Types')
    table6 = pd.pivot_table(df_filtered, values="show_id", index=['type'], aggfunc=np.size).reset_index()
    if not table6.empty:
        color_map = {    'Movie': 'red',    'TV Show': 'green',    'Other': 'blue'	}
        fig6 = px.pie(table6, values="show_id", names="type", hole=0, color='type' ,  
		color_discrete_sequence=['#0068c9', '#ff2b2b']
		)
        st.plotly_chart(fig6, use_container_width=True)
    else:
        show_no_data_message()

with col2:
    st.header('Content by Rating')
    rating_counts = df_filtered['rating'].value_counts()
    rating_counts_sorted = rating_counts.sort_index()
    if not rating_counts_sorted.empty:
        fig, ax = plt.subplots()
        rating_counts_sorted.plot(kind='bar', ax=ax, color='#0068c9')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Count')
        ax.set_title(f'Content Ratings')
        st.pyplot(fig)
    else:
        show_no_data_message()
st.divider()
# Genre Popularity
st.subheader('Netflix Genre Popularity')
if 'listed_in' in df_filtered.columns:
    genre_series = df_filtered['listed_in'].str.split(',', expand=True).stack()
    genre_counts = genre_series.value_counts().reset_index()
    genre_counts.columns = ['listed_in', 'Count']
    if not genre_counts.empty:
        fig = px.bar(genre_counts, x='listed_in', y='Count', title='Most Frequent Genres and Their Distribution',
                     labels={'listed_in': 'Genre', 'Count': 'Frequency'}, color='Count', color_continuous_scale='Turbo')
        fig.update_layout(xaxis_title='Genre', yaxis_title='Frequency', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        show_no_data_message()
st.divider()
# Multi-line Plot for Release Trends
st.subheader('Content Release Trends Over Time')
if 'release_year' in df_filtered.columns:
    release_counts = df_filtered.groupby('release_year').size().reset_index(name='count')
    if 'type' in df_filtered.columns:
        release_counts = df_filtered.groupby(['release_year', 'type']).size().reset_index(name='count')
        fig = px.line(release_counts, x='release_year', y='count', color='type',
                      title='Trends Over Time: Content Release Patterns',
                      labels={'release_year': 'Year', 'count': 'Number of Releases'})
    else:
        fig = px.line(release_counts, x='release_year', y='count',
                      title='Trends Over Time: Content Release Patterns',
                      labels={'release_year': 'Year', 'count': 'Number of Releases'})
    if len(release_counts) > 0:
        st.plotly_chart(fig, use_container_width=True)
    else:
        show_no_data_message()
st.divider()
# Country Wise Distribution
st.subheader("Country Wise Distribution")
if 'country' in df_filtered.columns:
    country_series = df_filtered['country'].str.split(',', expand=True).stack()
    country_counts = country_series.value_counts().reset_index()
    country_counts.columns = ['country', 'Count']
    if not country_counts.empty:
        fig = px.bar(country_counts, x='country', y='Count', labels={'country': 'Country', 'Count': 'Frequency'},
                     color='Count', color_continuous_scale='Turbo')
        fig.update_layout(xaxis_title='Country', yaxis_title='Frequency', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        show_no_data_message()
st.divider()
# Hierarchical TreeMap
st.subheader("Content Types Distribution")
df.fillna("None", inplace=True)
fig = px.treemap(df_filtered, path=["type", "listed_in"], values='year', color='listed_in', color_continuous_scale='Turbo')
st.plotly_chart(fig, use_container_width=True)
st.divider()


