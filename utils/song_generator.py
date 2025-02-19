import openai
import os
import streamlit as st
import random

# Load OpenAI API key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_song_structure(genre, song_length):
    """Generate a basic song structure based on genre and length."""
    structures = {
        "Rap": ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus", "Outro"],
        "Country": ["Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus", "Outro"],
        "Pop": ["Intro", "Verse", "Pre-Chorus", "Chorus", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Chorus", "Outro"],
        "Rock": ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Guitar Solo", "Bridge", "Chorus", "Outro"],
        "K-Pop": ["Intro", "Verse", "Pre-Chorus", "Chorus", "Verse", "Pre-Chorus", "Chorus", "Rap Break", "Bridge", "Chorus", "Outro"],
        "Opera": ["Overture", "Aria", "Recitative", "Chorus", "Aria", "Recitative", "Chorus", "Finale"],
        "Contemporary": ["Intro", "Verse", "Chorus", "Verse", "Chorus", "Bridge", "Chorus", "Outro"]
    }
    
    base_structure = structures.get(genre, structures["Pop"])
    
    # Adjust structure based on song length
    length_minutes = int(song_length.split(":")[0])
    if length_minutes <= 2:
        return base_structure[:4]
    elif length_minutes <= 3:
        return base_structure[:6]
    elif length_minutes <= 4:
        return base_structure
    else:
        return base_structure + ["Extended Outro"]

def select_unique_comments(comments, num_comments):
    """Select a specified number of unique comments."""
    unique_comments = list(set(comment['content-text'] for comment in comments))
    return random.sample(unique_comments, min(num_comments, len(unique_comments)))

def generate_song_lyrics(comments, model, genre, mood, creativity, song_length, additional_info):
    # Generate song structure
    structure = generate_song_structure(genre, song_length)
    
    # Estimate words per minute based on genre
    words_per_minute = {
        "Rap": 150, "Country": 100, "Pop": 120, "Rock": 110,
        "K-Pop": 130, "Opera": 80, "Contemporary": 100
    }
    wpm = words_per_minute.get(genre, 100)
    
    # Calculate total words based on song length
    minutes, seconds = map(int, song_length.split(":"))
    total_words = int((minutes + seconds/60) * wpm)
    
    # Estimate number of unique comments needed
    estimated_comments = total_words // 10  # Assuming average comment length of 10 words
    
    # Select unique comments
    unique_comments = select_unique_comments(comments, estimated_comments)
    
    # Generate lyrics by assigning unique comments to each section
    lyrics = []
    comment_index = 0
    for section in structure:
        section_lyrics = [f"{section}:"]
        words_in_section = 0
        while words_in_section < (total_words // len(structure)) and comment_index < len(unique_comments):
            comment = unique_comments[comment_index]
            section_lyrics.append(comment)
            words_in_section += len(comment.split())
            comment_index += 1
        lyrics.append("\n".join(section_lyrics) + "\n")
    
    # Join all sections
    full_lyrics = "\n".join(lyrics)
    
    # Use OpenAI to refine and format the lyrics
    prompt = f"""
    Create a complete, well-structured song from the following lyrics. The genre is {genre}, and the mood should be {mood}.

    Requirements:
    1. Create a COMPLETE song - do not truncate or end with "to be continued"
    2. Maintain clear section headers: [Intro], [Verse 1], [Chorus], etc.
    3. Each section should be properly spaced and formatted
    4. Use the provided comments as the core content, but you can:
       - Adjust line breaks for better flow
       - Add repetition where appropriate (especially for chorus)
       - Add minimal connecting words or phrases between lines
    5. Ensure all sections from the song structure are filled with content
    6. If more content is needed, creatively reuse and adapt existing comments

    Additional info: {additional_info}

    Lyrics to structure:
    {full_lyrics}
    
    Important: Generate the complete song with all sections. Do not truncate or leave any sections incomplete.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that formats and refines song lyrics without changing the core content."},
                {"role": "user", "content": prompt}
            ],
            temperature=creativity,
            max_tokens=4000
        )
        
        refined_lyrics = response.choices[0].message.content.strip()
        return refined_lyrics

    except openai.APIError as e:
        st.error(f"Error with OpenAI API: {str(e)}")
        st.warning("Falling back to unrefined lyrics due to API error.")
        return full_lyrics
    except Exception as e:
        st.error(f"Unexpected error in generating lyrics: {str(e)}")
        return full_lyrics
