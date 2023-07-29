import cv2
import webbrowser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import io
import speech_recognition as sr

# Set up the YouTube API client
api_key = 'AIzaSyDWcHSDLEyB3a2S_qbXhzbXfJnyyYb1NgI'
youtube = build('youtube', 'v3', developerKey=api_key)

# Dictionary of moods and corresponding search queries
mood_query = {
    'happy': 'happy music',
    'sad': 'sad music',
    'calm': 'relaxing music',
    'energetic': 'upbeat music',
    'romantic': 'romantic music'
}

# Function to capture user's face and get the mood
def get_user_mood():
    # Load the face detection cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and destroy the window
    cap.release()
    cv2.destroyAllWindows()

    # Use speech recognition to get the user's mood
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say your mood!')
        audio = r.listen(source)
    try:
        mood = r.recognize_google(audio)
        print('You said:', mood)
    except:
        print('Sorry, could not recognize your voice. Please try again.')
        mood = None

    return mood

# Function to search for videos on YouTube
def search_youtube(query):
    try:
        request = youtube.search().list(
            part='id',
            q=query,
            type='video',
            maxResults=5
        )
        response = request.execute()
        return response['items']
    except HttpError as e:
        print('An error occurred:', e)
        return None

# Function to recommend a playlist based on user's mood
def recommend_playlist(mood):
    query = mood_query.get(mood)
    if query:
        results = search_youtube(query)
        if results:
            video_ids = [result['id']['videoId'] for result in results]
            print('Recommended video IDs:', video_ids)
            # Open a web browser and play the first video from the recommended playlist
            webbrowser.open('https://www.youtube.com/watch?v=' + video_ids[0])
        else:
            print('Sorry, no results found for your mood.')
    else:
        print('Sorry, could not recognize your mood. Please try again.')

# Main function
def main():
    mood = get_user_mood()
    if mood:
        recommend_playlist(mood)

if __name__ == '__main__':
    main()
