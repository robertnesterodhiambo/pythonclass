import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("skyscrapers.csv")

# Streamlit app title
st.title("Skyscraper Data Explorer")

# Sidebar for user inputs
st.sidebar.header("Filters")

# Filters for user selection
country = st.sidebar.selectbox("Select a Country", df['location.country'].unique())
year_range = st.sidebar.slider("Select Completion Year Range", int(df['status.completed.year'].min()), int(df['status.completed.year'].max()), (2000, 2020))

# Filter data based on user input
filtered_data = df[(df['location.country'] == country) & (df['status.completed.year'].between(year_range[0], year_range[1]))]

# Visualization 1: Bar Chart - Tallest Skyscrapers
st.subheader("Tallest Skyscrapers in " + country)
top_skyscrapers = filtered_data.nlargest(10, 'statistics.height')
st.bar_chart(top_skyscrapers.set_index('name')['statistics.height'])

# Visualization 2: Line Chart - Completion Over Time
st.subheader("Skyscraper Completions Over Time")

# Ensure 'status.completed.year' is numeric
filtered_data['status.completed.year'] = pd.to_numeric(filtered_data['status.completed.year'], errors='coerce')

# Drop rows where 'status.completed.year' is NaN after conversion
filtered_data = filtered_data.dropna(subset=['status.completed.year'])

# Group the data by year and count the number of skyscrapers completed in each year
completion_count = filtered_data.groupby('status.completed.year').size()

# Check if the series is empty
if completion_count.empty:
    st.write("No skyscrapers completed in the selected year range.")
else:
    # Plot the line chart
    st.line_chart(completion_count)


# Visualization 3: Pie Chart - Purpose Distribution
st.subheader("Skyscraper Purpose Distribution in " + country)
purpose_columns = [col for col in df.columns if col.startswith('purposes.')]
purpose_sums = filtered_data[purpose_columns].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
ax.pie(purpose_sums, labels=purpose_sums.index.str.replace('purposes.', ''), autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
st.pyplot(fig)

# Visualization 4: Map - Skyscraper Locations
st.subheader("Skyscraper Map View")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=filtered_data['location.latitude'].mean(),
        longitude=filtered_data['location.longitude'].mean(),
        zoom=5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_data,
            get_position='[location.longitude, location.latitude]',
            get_fill_color='[200, 30, 0, 160]',
            get_radius=50000,
            pickable=True,
        )
    ]
))

# Visualization 5: Histogram - Building Heights Distribution
st.subheader("Building Heights Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(filtered_data['statistics.height'], bins=20, color='skyblue', edgecolor='black')
ax.set_title("Distribution of Building Heights")
ax.set_xlabel("Height (meters)")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Visualization 6: Scatter Plot - Height vs. Number of Floors
st.subheader("Height vs. Number of Floors")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(filtered_data['statistics.floors above'], filtered_data['statistics.height'], alpha=0.5, color='green')
ax.set_title("Height vs. Number of Floors")
ax.set_xlabel("Number of Floors Above Ground")
ax.set_ylabel("Height (meters)")
st.pyplot(fig)

# Visualization 7: Boxplot of Building Heights by Purpose
st.subheader("Building Heights by Purpose")
# Correct column names for the purposes
valid_purposes = [col for col in purpose_columns if col in filtered_data.columns and filtered_data[col].any()]
# Melt the dataframe to long format for easier plotting
melted_data = filtered_data.melt(id_vars=['statistics.height'], value_vars=valid_purposes, var_name='purpose', value_name='has_purpose')
# Filter out rows where there is no purpose
melted_data = melted_data[melted_data['has_purpose'] == True]

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='purpose', y='statistics.height', data=melted_data)
plt.xticks(rotation=90)
plt.title("Boxplot of Building Heights by Purpose")
st.pyplot(fig)


# Visualization 4: Map - Skyscraper Locations
st.subheader("Skyscraper Map View")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=filtered_data['location.latitude'].mean(),
        longitude=filtered_data['location.longitude'].mean(),
        zoom=5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_data,
            get_position='[location.longitude, location.latitude]',
            get_fill_color='[200, 30, 0, 160]',
            get_radius=50000,
            pickable=True,
        )
    ]
))

# New Visualization: Map Showing Material Count by Location
st.subheader("Materials Count by Location on the Map")

# Group the data by location (city) and material, then count the occurrences
material_count = filtered_data.groupby(['location.city', 'material']).size().reset_index(name='count')

# Create a mapping of locations to latitude and longitude
location_coords = filtered_data[['location.city', 'location.latitude', 'location.longitude']].drop_duplicates()

# Merge the material count data with location coordinates
material_count = pd.merge(material_count, location_coords, on='location.city')

# Create a pydeck map to show the material counts
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=material_count['location.latitude'].mean(),
        longitude=material_count['location.longitude'].mean(),
        zoom=5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=material_count,
            get_position='[location.longitude, location.latitude]',
            get_fill_color='[200, 30, 0, 160]',
            get_radius=50000,
            pickable=True,
            opacity=0.6,
        ),
        pdk.Layer(
            "TextLayer",
            data=material_count,
            get_position='[location.longitude, location.latitude]',
            get_text='count',
            get_size=15,
            get_color=[255, 255, 255],
            get_angle=0,
            get_text_anchor='middle',
            get_alignment_baseline='center',
        ),
    ]
))


# Summary Report
st.subheader("Summary Report")
st.write(f"Total Skyscrapers in {country}: {filtered_data.shape[0]}")
st.write(f"Tallest Skyscraper: {filtered_data.loc[filtered_data['statistics.height'].idxmax(), 'name']} ({filtered_data['statistics.height'].max()} meters)")
st.write(f"Oldest Skyscraper Completed: {filtered_data['status.completed.year'].min()}")
st.write(f"Most Recent Skyscraper Completed: {filtered_data['status.completed.year'].max()}")

st.write("Explore more using the filters on the sidebar!")
