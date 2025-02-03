# YouTube Comment Song Generator

A Streamlit application that creates songs from YouTube video comments using AI.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/DeVReV27/yt_commentsongs.git
cd yt_commentsongs
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

To get the API keys:
- YouTube API Key: 
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project or select an existing one
  3. Enable the YouTube Data API v3
  4. Create credentials (API key)
  5. Copy the API key to your .env file

- OpenAI API Key:
  1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
  2. Create a new API key
  3. Copy the API key to your .env file

4. Create required directories:
```bash
mkdir assets generated
```

5. Add your logo:
- Place your logo image in the `assets` directory as `logo.png`

## Running the Application

Run the Streamlit app:
```bash
streamlit run main.py
```

## Features

- Scrape comments from any YouTube video
- Generate song lyrics from comments using AI
- Multiple genre options
- Adjustable mood and creativity settings
- Download lyrics as PDF
- Export comments as CSV

## Note

Make sure to keep your API keys confidential and never commit them to version control. The `.env` file is included in `.gitignore` for this reason.
