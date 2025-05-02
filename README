# YouTube Channel Video Transcriber

This Python script checks a specified YouTube channel for new videos uploaded after a given date and automatically generates a text transcription for each new video found using Google's Generative AI (Gemini via Vertex AI).

## Features

*   Fetches videos from a specific YouTube channel's upload playlist.
*   Filters videos based on their publication date.
*   Uses the YouTube Data API v3.
*   Leverages Google's Gemini model via Vertex AI for video transcription.
*   Saves transcriptions to individual text files named after the video title.
*   Handles pagination for channels with many videos.
*   Basic error handling for API calls and data processing.

## Prerequisites

1.  **Python 3:** Ensure you have Python 3 installed.
2.  **Google Cloud Project:**
    *   A Google Cloud project with the Vertex AI API enabled.
    *   Authentication configured for Vertex AI. The easiest way is often using Application Default Credentials (ADC) by running:
        ```bash
        gcloud auth application-default login
        ```
3.  **YouTube Data API Key:**
    *   You need an API key from the Google Cloud Console with the YouTube Data API v3 enabled. See [Google's documentation](https://developers.google.com/youtube/v3/getting-started) for instructions.
4.  **Python Libraries:** Install the required libraries:
    ```bash
    pip install google-api-python-client google-cloud-aiplatform google-generativeai google-auth-httplib2 google-auth-oauthlib
    ```
    *(Note: `google-generativeai` might implicitly install some dependencies, but listing them ensures clarity)*

## Setup

1.  **Clone or Download:** Get the `youtubeapi.py` script.
2.  **Configure API Key:** Open `youtubeapi.py` and replace `'YOUR_API_KEY'` with your actual YouTube Data API key:
    ```python
    # Replace with your YouTube Data API key
    API_KEY = 'YOUR_YOUTUBE_DATA_API_KEY'
    ```
3.  **Configure Google Cloud Project:** In the same file, update `PROJECT_ID` and `LOCATION` with your Google Cloud project details:
    ```python
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "your-gcp-region" # e.g., "us-central1"
    ```
4.  **Authentication:** Ensure your environment is authenticated to Google Cloud as mentioned in the Prerequisites (e.g., using `gcloud auth application-default login`).

## Usage

1.  Run the script from your terminal:
    ```bash
    python youtubeapi.py
    ```
2.  The script will prompt you to enter:
    *   **The YouTube Channel ID:** This is usually found in the channel's URL (e.g., `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxx` -> ID is `UCxxxxxxxxxxxxxxxxx`).
    *   **The date (YYYY-MM-DD):** Enter the date after which you want to find videos. The script will look for videos published *after* midnight UTC on this date.

## Output

*   The script will print the title, publication date, and URL of each new video found to the console.
*   For each new video, it will attempt to generate a transcription.
*   A message indicating transcription generation start and completion will be printed.
*   A text file named `<Video Title>.txt` will be created in the same directory as the script, containing the generated transcription for each processed video.

## Configuration Constants

The following constants at the top of `youtubeapi.py` can be adjusted:

*   `API_KEY`: Your YouTube Data API Key.
*   `YOUTUBE_API_SERVICE_NAME`: Should remain `'youtube'`.
*   `YOUTUBE_API_VERSION`: Should remain `'v3'`.
*   `PROJECT_ID`: Your Google Cloud Project ID.
*   `LOCATION`: The Google Cloud region for Vertex AI (e.g., `us-central1`).
*   `model`: The Gemini model used for transcription (defaults to `gemini-2.0-flash-001`).
*   `generate_content_config`: Parameters for the Gemini API call (temperature, safety settings, etc.).

## Notes & Disclaimers

*   **API Quotas:** Both the YouTube Data API and Vertex AI have usage quotas and potential costs associated with them. Monitor your usage in the Google Cloud Console.
*   **Transcription Accuracy:** The quality of the transcription depends on the audio quality of the video and the capabilities of the Gemini model.
*   **Error Handling:** The script includes basic error handling, but complex API issues or network problems might cause it to stop. Check the console output for error messages.
*   **Video Accessibility:** The script currently assumes the video URLs are directly accessible for transcription by the Vertex AI service. This might not work for private videos or videos with certain restrictions. The `generate_transcription` function expects a URI that the Vertex AI service can access. YouTube video URLs (`https://www.youtube.com/watch?v=...`) are *not* direct file URIs and likely **will not work** directly with `types.Part.from_uri`. You might need to download the video first or use a different method compatible with Vertex AI's input requirements.
*   **Safety Settings:** The current configuration disables all content safety filters (`threshold="OFF"`). Be aware of the implications and adjust if necessary based on your use case and content policy requirements.
