import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load data
df = pd.read_csv("skyscrapers.csv")

# Simplify column names
df.columns = df.columns.str.replace('location.', '', regex=False)
df.columns = df.columns.str.replace('purposes.', '', regex=False)
df.columns = df.columns.str.replace('statistics.', '', regex=False)
df.columns = df.columns.str.replace('status.', '', regex=False)

# Handle missing or zero values
df['completed.year'] = df['completed.year'].replace(0, None)
df['started.year'] = df['started.year'].replace(0, None)

# Streamlit app
st.set_page_config(page_title="Skyscraper Data Visualizations", layout="wide")

st.title("Skyscraper Data Visualizations")

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Select Countries", options=df['country'].unique(), default=df['country'].unique())
selected_cities = st.sidebar.multiselect("Select Cities", options=df['city'].unique(), default=df['city'].unique())
selected_materials = st.sidebar.multiselect("Select Materials", options=df['material'].unique(), default=df['material'].unique())
height_range = st.sidebar.slider("Select Height Range (meters)", int(df['height'].min()), int(df['height'].max()), (int(df['height'].min()), int(df['height'].max())))

# Apply filters
filtered_df = df[
    (df['country'].isin(selected_countries)) &
    (df['city'].isin(selected_cities)) &
    (df['material'].isin(selected_materials)) &
    (df['height'].between(height_range[0], height_range[1]))
]

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_df)

# Visualizations
st.subheader("Visualizations")

# Bar chart: Count of skyscrapers by city
st.markdown("### Count of Skyscrapers by City")
city_counts = filtered_df['city'].value_counts().reset_index()
city_counts.columns = ['city', 'count']
city_bar_chart = alt.Chart(city_counts).mark_bar().encode(
    x=alt.X('count', title='Count'),
    y=alt.Y('city', sort='-x', title='City')
)
st.altair_chart(city_bar_chart, use_container_width=True)

# Histogram: Distribution of heights
st.markdown("### Distribution of Heights")
height_histogram = px.histogram(filtered_df, x='height', nbins=30, title="Height Distribution")
st.plotly_chart(height_histogram, use_container_width=True)

# Pie chart: Distribution of materials
st.markdown("### Distribution of Materials")
material_pie_chart = px.pie(filtered_df, names='material', title="Material Distribution")
st.plotly_chart(material_pie_chart, use_container_width=True)

# Map: Plot skyscrapers
st.markdown("### Map of Skyscrapers")
map_fig = px.scatter_mapbox(
    filtered_df,
    lat='latitude',
    lon='longitude',
    hover_name='name',
    color='height',
    size='height',
    zoom=1,
    mapbox_style="carto-positron",
    title="Skyscraper Locations"
)
st.plotly_chart(map_fig, use_container_width=True)

# Time-series: Trend of completed skyscrapers
st.markdown("### Trend of Completed Skyscrapers")
completion_trend = filtered_df.groupby('completed.year').size().reset_index(name='count')
time_series_chart = px.line(completion_trend, x='completed.year', y='count', title="Completion Trend")
st.plotly_chart(time_series_chart, use_container_width=True)

st.markdown("### Explore Further")
st.markdown("Use the filters in the sidebar to refine the data and visualizations!")
