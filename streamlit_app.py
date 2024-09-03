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
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="auto"
)

# Apply custom CSS for dark theme


# Set up Streamlit app title
st.title(":film_frames::film_projector: Netflix Data Dashboard :tv:")

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# Create new columns for years
df['year'] = pd.to_datetime(df['release_year']).dt.year

# Display basic statistics
col1, col2, col3 = st.columns(3)

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
    st.markdown('<div class="custom-box"><h3>All Contents</h3><p>{}</p></div>'.format(df['show_id'].count()), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-box"><h3>Movies</h3><p>{}</p></div>'.format(df[df['type'] == "Movie"]['type'].count()), unsafe_allow_html=True)

with col3:
    st.markdown('<div class="custom-box"><h3>TV Shows</h3><p>{}</p></div>'.format(df[df['type'] == "TV Show"]['type'].count()), unsafe_allow_html=True)

st.divider()

# Sidebar filters
st.sidebar.header('Filters')
years = st.sidebar.multiselect("Year", df["release_year"].unique())
region = st.sidebar.multiselect("Country", df["country"].unique())
type_select_filter = st.sidebar.multiselect("Type", df["type"].unique())
min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
selected_years = st.sidebar.slider('Select release year range:', min_year, max_year, (min_year, max_year))

# Apply filters
df_filtered = df
if years:
    df_filtered = df_filtered[df_filtered["release_year"].isin(years)]
if region:
    df_filtered = df_filtered[df_filtered["country"].isin(region)]
if type_select_filter:
    df_filtered = df_filtered[df_filtered["type"].isin(type_select_filter)]

# Categories Listed
st.header('Categories Listed in Netflix')
if 'listed_in' in df_filtered.columns and not df_filtered['listed_in'].dropna().empty:
    category_data = df_filtered['listed_in'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
    category_counts = category_data.value_counts()
    category_df = pd.DataFrame({'Category': category_counts.index, 'Count': category_counts.values})
    fig = px.treemap(category_df, path=['Category'], values='Count')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No category data available to display.")

# Countries of Origin
st.header('Countries of Origin')
if 'country' in df_filtered.columns and not df_filtered['country'].dropna().empty:
    country_data = df_filtered['country'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
    country_counts = country_data.value_counts()
    country_df = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})
    fig = px.scatter_geo(
        country_df,
        locations='Country',
        locationmode='country names',
        size='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.Sunset,
        size_max=50,
        title='Distribution of Content by Country of Origin'
    )
    fig.update_layout(
        geo=dict(
            coastlinecolor="DarkBlue",
            showland=True,
            landcolor="Black",
            showocean=True,
            oceancolor="LightBlue",
        ),
        coloraxis_colorbar=dict(
            title='Count',
            tickvals=[0, 50, 100, 200],
            ticktext=['0', '50', '100', '200']
        )
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No country data available to display.")

# Type-wise and Rating content
col1, col2 = st.columns(2)

with col1:
    st.header('Type Wise Distribution')
    table6 = pd.pivot_table(df, values="show_id", index=['type'], aggfunc=np.size).reset_index()
    fig6 = px.pie(table6, values="show_id", names="type", hole=0)
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.header('Content by Rating')
    rating_counts = df_filtered['rating'].value_counts().sort_index()
    if rating_counts.empty:
        st.write("No shows")
    else:
        fig, ax = plt.subplots()
        rating_counts.plot(kind='bar', ax=ax, color='coral')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Count')
        ax.set_title('Content Ratings')
        st.pyplot(fig, use_container_width=True)

st.divider()

# Genre Popularity
st.subheader('Netflix Genre Popularity')
if 'listed_in' in df_filtered.columns:
    genre_series = df_filtered['listed_in'].str.split(',', expand=True).stack()
    genre_counts = genre_series.value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig = px.bar(
        genre_counts,
        x='Genre',
        y='Count',
        title='Most Frequent Genres and Their Distribution',
        labels={'Genre': 'Genre', 'Count': 'Frequency'},
        color='Count',
        color_continuous_scale='Turbo'
    )
    fig.update_layout(xaxis_title='Genre', yaxis_title='Frequency', xaxis_tickangle=-45)
    st.plotly_chart(fig)
else:
    st.write("The 'genres' column is not found in the dataset.")

# Multi-line Plot for Content Trends
st.subheader('Trends Over Time')
if 'release_year' in df_filtered.columns:
    release_counts = df_filtered.groupby('release_year').size().reset_index(name='count')
    if 'type' in df_filtered.columns:
        release_counts = df_filtered.groupby(['release_year', 'type']).size().reset_index(name='count')
        fig = px.line(
            release_counts,
            x='release_year',
            y='count',
            color='type',
            title='Trends Over Time: Content Release Patterns',
            labels={'release_year': 'Year', 'count': 'Number of Releases'}
        )
    else:
        fig = px.line(
            release_counts,
            x='release_year',
            y='count',
            title='Trends Over Time: Content Release Patterns',
            labels={'release_year': 'Year', 'count': 'Number of Releases'}
        )
    st.plotly_chart(fig)
else:
    st.write("The 'release_year' column is not found in the dataset.")

# Country-wise Distribution
st.subheader("Country-wise Distribution")
genre_series = df_filtered['country'].str.split(',', expand=True).stack()
genre_counts = genre_series.value_counts().reset_index()
genre_counts.columns = ['Country', 'Count']
fig = px.bar(
    genre_counts,
    x='Country',
    y='Count',
    labels={'Country': 'Country', 'Count': 'Frequency'},
    color='Count',
    color_continuous_scale='Turbo'
)
fig.update_layout(xaxis_title='Country', yaxis_title='Frequency', xaxis_tickangle=-45)
st.plotly_chart(fig)

# Hierarchical view using TreeMap
st.subheader("Hierarchical View using TreeMap")
df_filtered.fillna("None", inplace=True)
fig = px.treemap(df_filtered, path=["type", "listed_in"], values='release_year')
st.plotly_chart(fig)

# Content Release by Decade
st.header('Content Release by Decade')
years_with_gap = list(range(selected_years[0], selected_years[1] + 1, 10))
filtered_by_gap = df_filtered[df_filtered['release_year'].isin(years_with_gap)]
fig, ax = plt.subplots()
filtered_by_gap['release_year'].value_counts().reindex(years_with_gap).plot(kind='line', ax=ax, color='green')
ax.set_xlabel('Release Year')
ax.set_ylabel('Count')
ax.set_title('Content Distribution by Decade')
st.pyplot(fig)
