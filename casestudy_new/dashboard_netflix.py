import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import warnings
import plotly.express as px
import datetime
from datetime import time
from datetime import datetime
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Netflix Dashboard", page_icon = "📺", layout = "centered", initial_sidebar_state="auto", menu_items=None)

st.logo("netflix_logo.png")
#=================== ADD CSS file ============================
# theme_folder = 'themes/blank'
# css_files=['styles.css', 'sidebar.css', 'button.css', 'inputs.css']
# for css_file in css_files:
	# st.markdown('<style>' + open(theme_folder + '/css/' + css_file).read() + '</style>', unsafe_allow_html=True)
# =========================TESTING=====================================
# theme_folder = 'themes/testing'
# css_files=['styles.css', 'sidebar.css', 'button.css', 'inputs.css']
# css_files.append('material-dashboard.css')

# for css_file in css_files:
	# st.markdown('<style>' + open(theme_folder + '/css/' + css_file).read() + '</style>', unsafe_allow_html=True)
#==============================================================
# #09f  # blue color
#rgba(255, 255, 255, 0.05) /* slightly transparent  */

st.markdown('<style type="text/css">body {     background-color: #121212;     color: #e0e0e0; }  /* Header and sidebar background colors */ .css-1l02d9a, .css-1rs6osf {     background-color: #1e1e1e; }  /* Sidebar text color */ .css-1f1d60w {     color: #e0e0e0; }  /* Change button and input styles to match dark theme */ .css-1o4ux7r, .css-1n1v10h {     background-color: #333;     color: #e0e0e0; }  /* Adjust chart colors */ .css-1i64wgt {     background-color: #121212; }  .stButton>button {     background-color: #333;     color: #e0e0e0;     border: none; }  .stTextInput>div>input {     background-color: #333;     color: #e0e0e0;     border: 1px solid #555; }  .stSelectbox>div>select {     background-color: #333;     color: #e0e0e0;     border: 1px solid #555; } </style>', unsafe_allow_html=True)
st.markdown('<style type="text/css">.css-1y4p8pa {    width: 100%;    padding: 0px;        padding-right: 1rem;        padding-left: 2rem;     max-width: 100%;</style>', unsafe_allow_html=True)
	
st.markdown('<style type="text/css">.css-1544g2n {    padding: 2rem 1rem 1.5rem;}</style>', unsafe_allow_html=True)
	
st.markdown(
    """
    <link rel="stylesheet" type="text/css" href="styles.css">
    """,
    unsafe_allow_html=True
)

#======================== CSS ENDS ======================================




# Set up Streamlit app title
st.title(":film_frames::film_projector: Netflix Data Dashboard :tv:")

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# Display basic information about the dataset
# st.header('Dataset Overview')
# st.write('Number of rows and columns:', df.shape)
# st.write('First few rows of the dataset:')
# st.write(df.head())








ct1,ct2=st.columns(2)
# ct1.image("netflix.jpg")
#ct2.title("NetFlix Dashboard")
df = pd.read_csv('netflix_titles.csv')


# create new columns for years and months
df['year'] = pd.to_datetime(df['release_year']).dt.year
#df['Months'] = pd.to_datetime(df['InvoiceDate']).dt.month
#st.write(df)
#st.write(df.head(10))


col1,col2,col3=st.columns(3)

col1.subheader("Total Movies and TV shows")
col1.subheader(df['show_id'].count())

col2.subheader("Total Movies")
col2.subheader(df[df['type'].isin(["Movie"])]['type'].count())

col3.subheader("Total TV Shows")
col3.subheader(df[df['type'].isin(["TV Show"])]['type'].count())

st.divider()

# ===== Side bar filters starts here =========================
st.sidebar.header('Filters')
#st.sidebar.button(label = "Reset") # testing button theme



years = st.sidebar.multiselect("Year",df["release_year"].unique())
region  = st.sidebar.multiselect("Country",df["country"].unique())
# Filter by content type
type_select_filter   = st.sidebar.multiselect("Type",df["type"].unique())
#st.write(type_select_filter)
# content_type = st.sidebar.selectbox('Select content type:', ['All'] + df['type'].unique().tolist())
# st.write(content_type)
# Filter by year
min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
selected_years = st.sidebar.slider('Select release year range:', min_year, max_year, (min_year, max_year))


df_filtered = df
#========== left col filters ==========
if not years or region or type_select_filter:
    pass
elif years and region and type_select_filter:
    df1=df[df["release_year"].isin(years)]
    df2=df1[df1["country"].isin(region)]
    df3=df2[df2["type"].isin(type_select_filter)]    
    df_filtered = df3

elif years and region:
    df1=df[df["release_year"].isin(years)]
    df2=df1[df1["country"].isin(region)]
    df_filtered = df2 
    
elif years and type_select_filter:
    df1=df[df["release_year"].isin(years)]
    df2=df1[df1["type"].isin(type_select_filter)]    
    df_filtered = df2 
elif region and type_select_filter:
    df1=df[df["country"].isin(region)]
    df2=df1[df1["type"].isin(type_select_filter)]    
    df_filtered = df2 

    
elif years:
    df1=df[df["release_year"].isin(years)]
    df_filtered = df1   
elif region:
    df1=df[df["country"].isin(region)]
    df_filtered = df1       
elif type_select_filter:
    df1=df[df["type"].isin(type_select_filter)]    
    df_filtered = df1       

else:
    pass

#=============================
#df = df_filtered
#=============================
# st.write("Filtered Table")
# st.write(df.head(10))














	

#===========++++++++++++++++++++++++     =======	
# Treemap for 'listed_in' column
st.header('Categories Listed in Netflix')

# Ensure that the 'listed_in' column exists and is non-empty
if 'listed_in' in df_filtered.columns and not df_filtered['listed_in'].dropna().empty:
	# Split the 'listed_in' column to handle multiple categories per row
	category_data = df_filtered['listed_in'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
	category_counts = category_data.value_counts()

	# Create a dataframe for plotting
	category_df = pd.DataFrame({'Category': category_counts.index, 'Count': category_counts.values})

	# Create a treemap
	fig = px.treemap(
		category_df,
		path=['Category'],
		values='Count',
		#title='Treemap of Categories Listed in Netflix'
	)

	st.plotly_chart(fig, use_container_width=True)
else:
	st.write("No category data available to display.")	








# Show a geomap with bright markers for countries of origin
st.header('Countries of Origin')

# Ensure that the 'country' column exists and is non-empty
if 'country' in df_filtered.columns and not df_filtered['country'].dropna().empty:
	# Extracting the country data
	country_data = df_filtered['country'].dropna().str.split(',', expand=True).stack().reset_index(drop=True)
	country_counts = country_data.value_counts()

	# Create a dataframe for plotting
	country_df = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})

	# Create a bright marker geomap
	fig = px.scatter_geo(
		country_df,
		locations='Country',
		locationmode='country names',
		size='Count',
		color='Count',
		
		#color_continuous_scale=px.colors.sequential.Plasma,
		#color_continuous_scale=px.colors.sequential.Viridis,
		#color_continuous_scale=px.colors.sequential.Cividis,
		#color_continuous_scale=px.colors.sequential.Turbo,
		color_continuous_scale=px.colors.sequential.Sunset,
		
		size_max=50,  # Adjust size of markers
		title='Distribution of Content by Country of Origin'
	)

	fig.update_layout(
		geo=dict(
			# showcoastlines=True,
			 coastlinecolor="DarkBlue",
			 showland=True,
			 landcolor="Black",
			 showocean=True,
			 oceancolor="LightBlue",
			# showcountries=True,
			# countrycolor="Black",
			# showrivers=True,
			# rivercolor="Blue",
			# showlakes=True,
			# lakecolor="LightBlue",
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


#=======================================


col1, col2 = st.columns(2)

with col1:
	# Pie chart for movie and TV shows
	st.header('Type wise')
	table6 = pd.pivot_table(df, values="show_id", index=['type'], aggfunc=np.size).reset_index()
	fig6=px.pie(table6,values="show_id",names="type",hole=0)
	st.plotly_chart(fig6,use_container_width=True)
	
with col2:
	# Show content by rating
	st.header('Content by Rating')
	rating_counts = df_filtered['rating'].value_counts()
	rating_counts_sorted = rating_counts.sort_index()
	if(rating_counts_sorted.empty):
		st.write("No shows")
	else:
		fig, ax = plt.subplots()
		rating_counts_sorted.plot(kind='bar', ax=ax, color='coral')
		ax.set_xlabel('Rating')
		ax.set_ylabel('Count')
		ax.set_title(f'Content Ratings')
		st.pyplot(fig, use_container_width=True)

st.divider()

#==================== BAR CHART FOR GENRES =========================		
st.subheader('Netflix Genre Popularity')

# Ensure the 'genres' column exists
if 'listed_in' in df_filtered.columns:
    # Process genres
    genre_series = df_filtered['listed_in'].str.split(',', expand=True).stack()
    genre_counts = genre_series.value_counts().reset_index()
    genre_counts.columns = ['listed_in', 'Count']
    
    # Plot genre popularity using Plotly
    fig = px.bar(
        genre_counts,
        x='listed_in',
        y='Count',
        title='Most Frequent Genres and Their Distribution',
        labels={'listed_in': 'Genre', 'Count': 'Frequency'},
        color='Count',
        color_continuous_scale='Turbo'
    )
    fig.update_layout(xaxis_title='Genre', yaxis_title='Frequency', xaxis_tickangle=-45)
    
    # Display the plot
    st.plotly_chart(fig)
else:
    st.write("The 'genres' column is not found in the dataset.")
	
#============== MULTI LINE PLOT ========================
# Ensure the 'release_year' column exists
if 'release_year' in df_filtered.columns:
    # Process data
    # Count the number of movies/TV shows per year
    release_counts = df_filtered.groupby('release_year').size().reset_index(name='count')
    
    # Optionally, if you have a column for content type (e.g., 'type' with 'Movie' and 'TV Show'),
    # you can differentiate the trends for movies and TV shows
    if 'type' in df_filtered.columns:
        # Group by year and type
        release_counts = df_filtered.groupby(['release_year', 'type']).size().reset_index(name='count')

        # Create a multiline plot
        fig = px.line(
            release_counts,
            x='release_year',
            y='count',
            color='type',
            title='Trends Over Time: Content Release Patterns',
            labels={'release_year': 'Year', 'count': 'Number of Releases'}
        )
    else:
        # Create a single line plot
        fig = px.line(
            release_counts,
            x='release_year',
            y='count',
            title='Trends Over Time: Content Release Patterns',
            labels={'release_year': 'Year', 'count': 'Number of Releases'}
        )

    # Display the plot
    st.plotly_chart(fig)
else:
    st.write("The 'release_year' column is not found in the dataset.")


#=================================

st.subheader("Country wise Distribution")
# table5 = pd.pivot_table(df_filtered, values="show_id", index=['country'], aggfunc=np.size).reset_index()
# fig12=px.pie(table5,values="show_id",names="country",hole=0)
# fig12.update_layout(
    # autosize=False,
    # width=500,
    # height=500
# )
# st.plotly_chart(fig12,use_container_width=True)


genre_series = df_filtered['country'].str.split(',', expand=True).stack()
genre_counts = genre_series.value_counts().reset_index()
genre_counts.columns = ['country', 'Count']

# Plot genre popularity using Plotly
fig = px.bar(
    genre_counts,
    x='country',
    y='Count',
    #title='Country wise Distribution',
    labels={'country': 'Country', 'Count': 'Frequency'},
    color='Count',
    color_continuous_scale='Turbo'
)
fig.update_layout(xaxis_title='Country', yaxis_title='Frequency', xaxis_tickangle=-45)

# Display the plot
st.plotly_chart(fig)

#====================================




#===============
# (f) Hierarchical view of Sale using any chart, path=[”Region”,”Category”,”Sub-Category”] and values = ”Sales”
st.subheader("Hierarchical view using TreeMap")
df_filtered.fillna("None")
fig = px.treemap(df_filtered, path=["type","listed_in"], values='release_year')
st.plotly_chart(fig)

st.divider()
#===============

    
    

#===============
	




# Create a bar chart with a 10-year gap
st.header('Content Release by Decade')
# Select years with a 10-year gap
years_with_gap = list(range(selected_years[0], selected_years[1] + 1, 10))
filtered_by_gap = df_filtered[df_filtered['release_year'].isin(years_with_gap)]

# Create a bar plot
fig, ax = plt.subplots()
filtered_by_gap['release_year'].value_counts().reindex(years_with_gap).plot(kind='line', ax=ax, color='green')
ax.set_xlabel('Release Year')
ax.set_ylabel('Count')
ax.set_title('Content Distribution by Decade')
st.pyplot(fig)

    