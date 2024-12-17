import streamlit as st
from utils.youtube_scraper import scrape_youtube_comments
from utils.csv_generator import generate_csv
from utils.song_generator import generate_song_lyrics
from utils.pdf_generator import generate_pdf
import os

# Load environment variables (API keys)
from dotenv import load_dotenv
load_dotenv()

# Main Streamlit app
st.set_page_config(layout="wide", page_title="MacieraiMusic")

# Sidebar logo and variables
st.sidebar.image("assets/logo.png", use_column_width=True)

st.sidebar.title("Song Creation Settings")

# Song creation settings
genre = st.sidebar.selectbox("Genre", ["Rap", "Country", "Pop", "Rock", "K-Pop", "Opera", "Contemporary"])
mood = st.sidebar.selectbox("Mood", ["Normal", "Serious", "Fun", "Light-hearted", "Poppy", "Melancholy", "Intense"])
creativity = st.sidebar.slider("Creativity (formatting refinement)", 0.0, 1.0, 0.7)
song_length = st.sidebar.selectbox("Song Length (minutes)", ["2:15", "2:30", "2:45", "3:00", "3:15", "3:30", "3:45", "4:00", "4:15", "4:30", "4:45", "5:00"])
additional_info = st.sidebar.text_area("Additional Info", placeholder="Add any extra details for the song...")

# Main page content
st.title("YouTube Comment Song Creator")

youtube_url = st.text_input("Enter YouTube URL:")

if st.button("Scrape Comments"):
    if youtube_url:
        with st.spinner("Scraping comments..."):
            try:
                comments, video_title, channel_name = scrape_youtube_comments(youtube_url)
                if comments:
                    csv_file = generate_csv(comments, video_title, channel_name)
                    st.success(f"Comments successfully scraped from '{video_title}' by {channel_name}!")
                    st.download_button(label="Download CSV", data=csv_file, file_name="comments.csv", mime="text/csv")
                    st.session_state['comments'] = comments
                    st.session_state['video_title'] = video_title
                    st.session_state['channel_name'] = channel_name
                else:
                    st.warning("No comments found for this video.")
            except Exception as e:
                st.error(f"An error occurred while fetching comments: {str(e)}")

if st.button("Create Song"):
    if 'comments' in st.session_state:
        with st.spinner("Creating song lyrics..."):
            lyrics = generate_song_lyrics(
                st.session_state['comments'], 
                "gpt-4o",
                genre, 
                mood, 
                creativity, 
                song_length, 
                additional_info
            )
            st.write(lyrics)
            try:
                pdf_bytes = generate_pdf(lyrics)
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="song_lyrics.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                st.write("Unable to generate PDF. You can copy the lyrics from above.")
    else:
        st.error("Please scrape comments first before creating a song.")

# Display video title and channel name if available
if 'video_title' in st.session_state and 'channel_name' in st.session_state:
    st.sidebar.markdown(f"**Video:** {st.session_state['video_title']}")
    st.sidebar.markdown(f"**Channel:** {st.session_state['channel_name']}")

# Add some spacing
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

# Add a footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 MacieraiMusic. All rights reserved.")