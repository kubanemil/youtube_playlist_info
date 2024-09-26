import csv
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from isodate import parse_duration
from datetime import datetime

load_dotenv()

# Set up YouTube API client
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def extract_video_info(video_id):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails", id=video_id
    )
    response = request.execute()

    # Check if the response contains any items
    if not response["items"]:
        print(f"No data found for video ID: {video_id}")
        return None, None, None, None, None, None

    video = response["items"][0]
    title = video["snippet"]["title"]
    views = video["statistics"]["viewCount"]
    duration = parse_duration(video["contentDetails"]["duration"]).total_seconds()
    published_at = video["snippet"]["publishedAt"]
    published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
    channel_name = video["snippet"]["channelTitle"]
    description = video["snippet"]["description"]

    return title, views, duration, published_date, channel_name, description


def process_csv(input_file, output_file):
    with open(input_file, "r") as infile, open(
        output_file, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        writer.writerow(
            [
                "Video URL",
                "Title",
                "Views",
                "Duration (seconds)",
                "Publication Date",
                "Channel Name",
                "Description",
            ]
        )

        # Skip header
        next(reader)

        for row in reader:
            video_url = row[0]
            video_id = video_url.split("v=")[1]
            title, views, duration, published_date, description, channel_name = (
                extract_video_info(video_id)
            )
            if title:
                writer.writerow(
                    [
                        video_url,
                        title,
                        views,
                        duration,
                        published_date,
                        description,
                        channel_name,
                    ]
                )


# Usage
input_csv = "playlist_PLtVdS8z6F1MkY-pffA-gVYwaCQzVREj8G.csv"
output_csv = "info_" + input_csv
process_csv(input_csv, output_csv)
