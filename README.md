# YouTube Playlist Video Extractor

This project allows you to extract video information from a YouTube playlist using the YouTube Data API.

## Prerequisites

Before running this project, you need to set up the following:

1. YouTube API Key:
   - Go to the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project or select an existing one.
   - Enable the YouTube Data API v3 for your project.
   - Create credentials (API Key) for accessing the API.

2. Environment Variables:
   - Create a `.env` file in the root directory of the project.
   - Add your YouTube API Key to the `.env` file as follows:

     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

   Replace `your_api_key_here` with the actual API key you obtained from the Google Developers Console.

## Installation

1. Clone this repository.
2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the `retrieve.py` script and follow the prompts to enter a YouTube playlist URL or ID.
The script will retrieve video links from the playlist and save it to a CSV file with a name 
`playlist_{PLAYLIST_ID}.csv`.

2. Run the `extract.py` script to extract data from the links and save it
into `info_playlist_{PLAYLIST_ID}.csv`.

## Note

Make sure to keep your `.env` file secure and do not share it publicly, as it contains sensitive information (your API key).
