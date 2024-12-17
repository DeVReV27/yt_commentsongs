# YouTube Comments Song Generator

This application creates unique songs by extracting random comments from YouTube videos. It combines the power of YouTube data extraction with creative text-to-song generation.

## Features

- Extracts comments from any YouTube video
- Generates creative songs from the extracted comments
- Exports results in multiple formats (CSV, PDF)
- Easy-to-use command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DeVReV27/yt_commentsongs.git
cd yt_commentsongs
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:
```
YOUTUBE_API_KEY=your_api_key_here
```

## Usage

Run the main application:
```bash
python main.py
```

The application will:
1. Prompt for a YouTube video URL
2. Extract random comments from the video
3. Generate a song using the extracted comments
4. Save the results in both CSV and PDF formats

## Project Structure

- `main.py`: Main application entry point
- `utils/`:
  - `youtube_scraper.py`: Handles YouTube comment extraction
  - `song_generator.py`: Converts comments into song lyrics
  - `pdf_generator.py`: Generates PDF output
  - `csv_generator.py`: Generates CSV output

## Requirements

See `requirements.txt` for a full list of dependencies.

## License

This project is open source and available under the MIT License.
