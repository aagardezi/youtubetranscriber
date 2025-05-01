import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone
from google import genai
from google.genai import types
import sys
import base64

# --- Configuration ---
# Replace with your YouTube Data API key
API_KEY = 'YOUR_API_KEY' # Set the API Key
YOUTUBE_API_SERVICE_NAME = 'youtube' # Do not change
YOUTUBE_API_VERSION = 'v3' # Do not change
PROJECT_ID = "PROJECT_ID" # Set the project ID
LOCATION = "us-central1" # Set the region

def get_channel_uploads_playlist_id(youtube, channel_id):
    """
    Fetches the ID of the 'uploads' playlist for a given channel ID.
    """
    try:
        response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        if not response.get('items'):
            print(f"Error: Channel with ID '{channel_id}' not found.")
            return None

        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None
    except KeyError:
        print(f"Could not find 'uploads' playlist ID for channel '{channel_id}'. The channel might not have public uploads or the API response structure changed.")
        return None

def get_new_videos_from_playlist(youtube, playlist_id, after_date_str):
    """
    Retrieves videos from a playlist uploaded after a specific date.
    Prints the URL of each new video.
    """
    try:
        # Convert the input date string to a timezone-aware datetime object (UTC)
        # Assuming the input date is in YYYY-MM-DD format
        after_date = datetime.strptime(after_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    videos_found = False
    next_page_token = None

    print(f"\nChecking for videos uploaded after {after_date_str}...\n")

    while True:
        try:
            playlist_items_response = youtube.playlistItems().list(
                playlistId=playlist_id,
                part='snippet,contentDetails',
                maxResults=50,  # Max 50 per page
                pageToken=next_page_token
            ).execute()

            for item in playlist_items_response.get('items', []):
                video_id = item['contentDetails']['videoId']
                published_at_str = item['snippet']['publishedAt']

                # YouTube API returns publishedAt in ISO 8601 format (e.g., '2023-10-26T14:30:00Z')
                # It needs to be parsed into a datetime object.
                # The 'Z' indicates UTC timezone.
                published_at_dt = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

                if published_at_dt > after_date:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"New Video: {item['snippet']['title']}")
                    print(f"Published: {published_at_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                    print(f"URL: {video_url}\n")
                    videos_found = True
                    print("Generating transcription...")
                    generate_transcription(video_url, item['snippet']['title'])
                    print("Transcription generated.")



            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break  # No more pages

        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred while fetching playlist items: {e.content}")
            return
        except KeyError as e:
            print(f"Error processing video data: {e}. Skipping item.")
            continue


    if not videos_found:
        print(f"No new videos found on the channel after {after_date_str}.")

def generate_transcription(file_uri, video_name):
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location=LOCATION,
  )

  msg1_video1 = types.Part.from_uri(
      file_uri= file_uri,
      mime_type="video/*",
  )

  model = "gemini-2.0-flash-001"
  contents = [
    types.Content(
      role="user",
      parts=[
        msg1_video1,
        types.Part.from_text(text="""Can do full transcription of this video""")
      ]
    ),
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
  )
  f = open(video_name + ".txt",'w')
  response = client.models.generate_content(
    model = model,
    contents = contents,
    config = generate_content_config,
  )
  print(response.text, file=f)
  f.close()

def main():
    if API_KEY == 'YOUR_API_KEY':
        print("Error: Please replace 'YOUR_API_KEY' with your actual YouTube Data API key in the script.")
        return

    channel_id = input("Enter the YouTube Channel ID (e.g., UCxxxxxxxxxxxxxxxxx): ")
    # You can find a channel ID in the URL of the channel page (e.g., https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw -> ID is UC_x5XG1OV2P6uZZ5FSM9Ttw)
    # Or, if you have a channel username, you might need an extra step to get the ID. This script assumes you have the ID.

    date_str = input("Enter the date to check for videos uploaded after (YYYY-MM-DD): ")

    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    except Exception as e:
        print(f"Error building YouTube service: {e}")
        return

    uploads_playlist_id = get_channel_uploads_playlist_id(youtube, channel_id)

    if uploads_playlist_id:
        get_new_videos_from_playlist(youtube, uploads_playlist_id, date_str)

if __name__ == '__main__':
    main()