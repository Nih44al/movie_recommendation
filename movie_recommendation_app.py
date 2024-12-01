import streamlit as st
import pandas as pd
import os
from PIL import Image

# Function to generate the correct image filename based on the dataset
def get_image_filename(movie_title):
    # Replace spaces with underscores, convert to lowercase, and remove special characters
    image_filename = movie_title.lower().replace(' ', '_').replace("'", '').replace(':', '').replace('-', '_') + '.jpg'
    return image_filename

# Load the dataset
movies = pd.read_excel('movies_dataset.xlsx')  # Ensure the dataset file is in the same directory

# Set Streamlit page config
st.set_page_config(page_title="Movie Recommendation", layout="wide")

# Function to display recommendations
def show_recommendations(selected_movie):
    try:
        # Load and display the selected movie's poster
        image_title = selected_movie['Title']
        image_filename = get_image_filename(image_title)  # Generate the correct image filename
        image_path = os.path.join('posters', image_filename)
        st.image(Image.open(image_path), caption=selected_movie['Title'], width=200)
    except Exception as e:
        st.write(f"Error loading image for {selected_movie['Title']}: {e}")

    # Display movie description
    st.subheader("Description:")
    st.write(selected_movie['Description'])  # Display the description of the selected movie

    # Display other recommended movies (same language and genre, but different year)
    st.subheader("Recommended Movies:")
    
    # Filter recommendations based on same language and genre, excluding the selected movie
    recommendations = filtered_movies[
        (filtered_movies['Title'] != selected_movie['Title']) & 
        (filtered_movies['Language'] == selected_movie['Language']) &
        (filtered_movies['Genre'] == selected_movie['Genre'])
    ].head(3)  # Limit to 3 recommendations

    if recommendations.empty:
        st.write("No recommendations available based on the current filters.")
    else:
        for _, movie in recommendations.iterrows():
            st.write(f"**{movie['Title']}**")
            st.write(movie['Description'])  # Display description of the recommended movie
            try:
                rec_image_title = movie['Title']
                rec_image_filename = get_image_filename(rec_image_title)  # Generate the correct image filename
                rec_image_path = os.path.join('posters', rec_image_filename)
                st.image(Image.open(rec_image_path), caption=movie['Title'], width=150)
            except Exception as e:
                st.write(f"Poster not available for {movie['Title']}: {e}")

# Sidebar filters
st.sidebar.header("Filter Movies")
language_filter = st.sidebar.selectbox('Select Language', sorted(movies['Language'].unique()))
genre_filter = st.sidebar.selectbox('Select Genre', sorted(movies['Genre'].unique()))
year_filter = st.sidebar.selectbox('Select Year', sorted(movies['Year'].unique()))  # Sorted in ascending order
rating_filter = st.sidebar.slider('Select Maximum Rating', 0.0, 10.0, 10.0)  # Maximum rating filter

# Filter dataset based on selections
filtered_movies = movies[
    (movies['Language'] == language_filter) &
    (movies['Genre'] == genre_filter) &
    (movies['Year'] == year_filter) &  # Year filter is still applied here for the initial movie selection
    (movies['Rating'] <= rating_filter)  # Adjusted to filter for maximum rating
]

# Check if any movies are available after filtering
if filtered_movies.empty:
    st.write("No movies found based on the selected filters. Try adjusting your filters.")

# Dropdown to select a movie from the filtered list
st.subheader("Select a Movie for Recommendations")
selected_movie_title = st.selectbox('Choose a movie:', filtered_movies['Title'].unique())

if selected_movie_title:
    selected_movie = filtered_movies[filtered_movies['Title'] == selected_movie_title].iloc[0]
    show_recommendations(selected_movie)
