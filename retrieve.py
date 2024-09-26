import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

# Set up YouTube client
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
MAX_VIDEOS_PER_PLAYLIST = 1000

youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


def get_playlist_videos(playlist_id: str) -> list[str]:
    print("Starting parsing...")
    request = youtube.playlistItems().list(
        part="snippet", playlistId=playlist_id, maxResults=50
    )
    response = request.execute()

    videos = []
    i = 0
    while request is not None:
        response = request.execute()
        items = [
            f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
            for item in response.get("items", [])
        ]
        print(f"items #{i}:", len(items))
        videos += items
        request = youtube.playlistItems().list_next(request, response)
        if i > MAX_VIDEOS_PER_PLAYLIST / 50:
            print("Reached max amount of videos per playlist!")
            break
        i += 1

    return videos


if __name__ == "__main__":
    # Function to format the playlist ID
    def format_playlist_id(playlist_id: str) -> str:
        # Remove any leading/trailing whitespace
        playlist_id = playlist_id.strip()

        # If the ID is a full URL, extract just the ID part
        if playlist_id.startswith(
            ("https://www.youtube.com/", "http://www.youtube.com/")
        ):
            playlist_id = playlist_id.split("list=")[-1]
            playlist_id = playlist_id.split("&")[0]  # Remove any additional parameters

        return playlist_id

    playlist_link: str = (
        str(input("Enter playlist Link: ")) or "PLtVdS8z6F1MkY-pffA-gVYwaCQzVREj8G"
    )
    playlist_id = format_playlist_id(playlist_link)
    print("Your playlist's ID:", playlist_id)

    videos = get_playlist_videos(playlist_id)

    print("Videos in playlist:", len(set(videos)))

    # Write links to CSV file
    output_file = Path(f"playlist_{playlist_id}.csv")

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Video URL"])  # Write header
        for video in videos:
            writer.writerow([video])

    print(f"Video links have been written to {output_file}")
