import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, parse_qs

# Load API key from environment variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def extract_video_id(url):
    """Extract the video ID from various forms of YouTube URLs."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    # If we get here, it's not a valid YouTube URL
    raise ValueError(f"Invalid YouTube URL: {url}")

def scrape_youtube_comments(youtube_url):
    try:
        # Extract video ID from URL
        video_id = extract_video_id(youtube_url)

        # Fetch video title and channel name by scraping HTML
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        html_response = requests.get(youtube_url, headers=headers)
        html_response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(html_response.content, 'html.parser')

        # Extract the video title and channel name from the HTML page
        video_title = soup.find("meta", property="og:title")['content']
        channel_name = soup.find("link", itemprop="name")['content']

        # Fetch comments using the YouTube Data API
        comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults=100"
        comments_response = requests.get(comments_url)
        comments_response.raise_for_status()  # Raise an exception for bad status codes
        comments_data = comments_response.json()

        comments = []
        for item in comments_data.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author-text': comment['authorDisplayName'],  # Changed back to 'author-text'
                'content-text': comment['textDisplay']
            })

        return comments, video_title, channel_name

    except requests.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except ValueError as e:
        raise Exception(f"URL parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Data extraction error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")