# Libraries Used
import tempfile
from pydub.playback import play
import speech_recognition as sr
import wikipedia
import webbrowser
import pyautogui
import pygame
import random
from gtts import gTTS
import os
import json
import pyaudio
import datetime
import requests
from bs4 import BeautifulSoup
import time
import googleapiclient.discovery
from groq import Groq
from pydub import AudioSegment
import re

# Load the JSON file with API Keys
with open('key.json', 'r') as file:
    config = json.load(file)

# Access the API key
API_KEY_YT = config.get("API_KEY_YT")
API_KEY_GROQ = config.get("API_KEY_GROQ")

# Use APIs
API_KEY = API_KEY_YT
client = Groq(api_key=API_KEY_GROQ)

def get_joke(query):
    # Check if the message contains the word "joke"
    if "joke" in query.lower():
        # Request a joke using Groq
        joke_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Tell me a joke",
                }
            ],
            model="mixtral-8x7b-32768",
        )
        # Extract the joke from the completion response
        joke = joke_completion.choices[0].message.content
        say(joke)
    else:
        return "Sorry, I couldn't generate a joke right now."

def get_solution(query):
    if "what is" in query.lower() or "who is" in query.lower():
        solution = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{query}",
                }
            ],
            model="mixtral-8x7b-32768",
        )
        ans = solution.choices[0].message.content
        # Extract the first sentence
        first_sentence = re.split(r'(?<=[.!?])\s+', ans.strip())[0]
        say(first_sentence)
        say("Want to ask more?")
        # Create a filename based on the query
        filename = f"{query.replace(' ', '_')}.md"
        with open(filename, 'w') as f:
            f.write(ans)
        say(f"Result will be saved to file after the program will end.")
    else:
        return "Sorry, I couldn't fetch the solution right now."

def get_short_story():
    url = "https://americanliterature.com/short-stories-for-children"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-successful status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        story_elements = soup.find_all('a', class_='story-title')
        if not story_elements:
            raise Exception("No short stories found on the webpage.")
        stories = [story.get_text().strip() for story in story_elements]
        if not stories:
            raise Exception("Extracted stories list is empty.")
        return random.choice(stories)
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

def say(text):
    speech = gTTS(text=text, lang="hi")

    # Save the speech audio into a temporary file
    output_file = os.path.join(tempfile.gettempdir(), "output.mp3")
    speech.save(output_file)

    # Load the speech audio
    audio = AudioSegment.from_file(output_file)

    # Apply noise reduction (low-pass filter)
    audio = audio.low_pass_filter(3000)  # Adjust cutoff frequency as needed

    # Play the audio
    play(audio)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise before listening
            audio = r.listen(source, timeout=5)  # Set a timeout for listening (5 seconds in this case)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You Said: {query}")
            return query
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return "Request Error. Please check your internet connection."
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return "Sorry, I couldn't understand what you said."
        except sr.WaitTimeoutError:
            print("Timeout listening for speech")
            return "Sorry, I didn't hear anything. Please try again."

def play_specific_song(song_name):
    try:
        # Initialize the YouTube Data API client
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

        # Search for the song on YouTube
        search_response = youtube.search().list(
            q=f"{song_name} song",
            part='id',
            type='video',
            maxResults=1
        ).execute()

        # Extract the video ID of the top search result
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Now playing {song_name} on YouTube.")
        say(f"Now playing {song_name} on YouTube.")

        # Open the specific video URL in the web browser to play automatically
        webbrowser.open(video_url)

    except Exception as e:
        print(f"Error in play_specific_song function: {e}")
        say("Sorry, I encountered an error while trying to play the song.")

def play_folder_music():
    pygame.init()  # Initialize pygame
    pygame.mixer.init()  # Initialize mixer
    pygame.display.init()  # Initialize display (to avoid video system not initialized error)

    folder_path = "D:/Musics/"

    try:
        while True:
            # Get a list of all files in the folder
            audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

            if not audio_files:
                print("No MP3 files found in the folder.")
                return

            # Select a random audio file from the list
            random_audio_file = random.choice(audio_files)

            # Construct the full path to the selected audio file
            music_path = os.path.join(folder_path, random_audio_file)

            # Load and play the selected audio file
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            print(f"Now playing: {music_path}")

            # Set an event for the end of the music
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

            # Wait for the music to finish playing or for a command
            while True:
                # Check for music end event or voice command
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:  # Music end event
                        print("Music ended.")
                        break  # Exit the inner loop to play the next song

                # Listen for voice commands
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening for commands...")
                    audio = r.listen(source)

                try:
                    command = r.recognize_google(audio).lower()
                    print(f"Recognized command: {command}")

                    if "stop" in command or "quit" in command:
                        pygame.mixer.music.stop()
                        print("Music stopped.")
                        return

                    if "volume up" in command:
                        pygame.mixer.music.set_volume(min(1.0, pygame.mixer.music.get_volume() + 0.1))
                        print("Volume increased.")

                    if "volume down" in command:
                        pygame.mixer.music.set_volume(max(0.0, pygame.mixer.music.get_volume() - 0.1))
                        print("Volume decreased.")

                    if "max volume" in command:
                        pygame.mixer.music.set_volume(1.0)
                        print("Maximum volume set.")

                    if "minimum volume" in command:
                        pygame.mixer.music.set_volume(0.0)
                        print("Minimum volume set.")

                    if "next song" in command or "next" in command or "next one" in command:
                        pygame.mixer.music.stop()
                        break  # Exit the inner loop to go to the next song

                    if "pause" in command:
                        pygame.mixer.music.pause()
                        print("Music paused.")
                    elif "play" in command:
                        pygame.mixer.music.unpause()
                        print("Music resumed.")

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results: {e}")

    except Exception as e:
        print(f"Error while playing music: {e}")

    finally:
        pygame.quit()

def search_wikipedia(topic):
    try:
        # Search Wikipedia for the query
        results = wikipedia.search(query)

        if not results:
            return "No relevant information found on Wikipedia."

        # Fetch the summary of the page
        page_summary = wikipedia.summary(topic, sentences=2)

        return page_summary
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation errors (when multiple pages match the query)
        return f"Please specify your query. Multiple results found: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return "No information found on Wikipedia for this query."
    except Exception as e:
        return f"Error occurred while fetching information: {str(e)}"

def openSite():
    say(f"I am opening {site[0]}")
    webbrowser.open(site[1])

def openApp():
    say(f"Opening {app[0]} for you.")
    os.system(f"start {app[1]}")

def get_greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 0 <= hour < 12:
        time_greeting = "Good morning!"
    elif 12 <= hour < 17:
        time_greeting = "Good afternoon!"
    elif 17 <= hour < 21:
        time_greeting = "Good evening!"
    else:
        time_greeting = "Hello! Late night coding, eh?"

    greetings = [
        "I'm elly, at your service.",
        "This is elly, ready to help.",
        "I'm elly, your friendly assistant.",
        "Hi there! I’m elly, ready to brighten your day!",
        "I’m elly, your virtual buddy. Let’s get started!",
        "I'm elly, at your command.",
        "This is elly, how can I assist you today?",
        "I'm elly, always here to lend a hand.",
    ]

    random_greeting = random.choice(greetings)

    combined_greeting = f"{time_greeting} {random_greeting}"

    return combined_greeting

def greet():
    greeting = get_greeting()
    say(greeting)

def maps(location):
    google_maps_url = f"https://www.google.com/maps/search/?q={location}"
    webbrowser.open(google_maps_url)
    say(f"Opening {location} in Google Maps. Is there anything else I can assist you with?")

def texttospeech():
    textInput = input("Enter Your Text: ")
    say(textInput)


if __name__ == '__main__':
    greet()
    say("listening to you.")

    sites = [["youtube", "https://www.youtube.com/"],
             ["google", "https://www.google.com/"],
             ["portfolio", "https://Aditya-Vishwa.github.io/My-Portfolio"],
             ["instagram", "https://www.instagram.com/"],
             ["canva", "https://www.canva.com/"],
             ["meet", "https://meet.google.com/"],
             ["classroom", "https://classroom.google.com/"],
             ["mail", "https://mail.google.com/"],
             ["twitter", "https://www.twitter.com/"],
             ["GitHub", "https://www.github.com/"],
             ["Wikipedia", "https://www.wikipedia.com"]]

    apps = [["chrome", "chrome.exe"],
            ["file", "explorer.exe"],
            ["notepad", "notepad.exe"],
            ["code", "code"],
            ["discord", "C:/Users/vishw/AppData/Local/Discord/Update.exe --processStart Discord.exe"],
            ["calculator", "calc.exe"],
            ["cmd", "cmd.exe"]]

    bye = ["done", "exit", "end", "break", "you are free", "bye", "bye-bye", "free", "no", "stop", "nothing"]

    elly = ["are you", "hu r u", "what r u", "hu"]

    ai = ["What", "Where", "When", "Which", "Who", "Whom", "Whose", "Why", "How", "How many", "How much",
          "How often", "How long", "How far", "How old", "Write me"]

    compliments = ["great", "nice", "you are the best", "thank", "thank you", "thanks"]

    while True:
        query = takeCommand()
        print("Recognized query:", query)  # Added this line for debugging

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                openSite()

        for app in apps:
            if f"Open {app[0]}".lower() in query.lower():
                openApp()


        if "play music" in query.lower() or "play songs" in query.lower():
            play_folder_music()

        # Check if the command contains "play" and "song" keywords
        if "play" in query and "song" in query:
            # Extract the song name from the command
            song_name = query.replace("play", "").replace("song", "").strip()
            play_specific_song(song_name)

        elif "shutdown" in query.lower():
            # Say goodbye message
            say("Goodbye! Initiating system shutdown.")

            # Countdown timer before shutdown
            countdown_time = 3  # Set the countdown time to 5 seconds
            while countdown_time > 0:
                # Convert countdown number to spoken words
                countdown_text = str(countdown_time)
                say(countdown_text)  # Speak the countdown number
                time.sleep(0.5)  # Pause for 1 second
                countdown_time -= 1
            # Initiate system shutdown with a delay of 5 seconds
            os.system("shutdown /s /t 1")  # Shutdown the system

        elif "search" in query.lower():
            # Extract the search query from the user's command
            search_query = query.lower().replace("search", "").replace("what is", "").replace("who is", "").strip()

            # Search Wikipedia based on the query
            wikipedia_response = search_wikipedia(search_query)

            # Speak out the Wikipedia summary
            say(wikipedia_response)
            say("Want to ask more?")
            continue

        elif "tell me a joke" in query.lower():
            user_message = query
            joke_response = get_joke(user_message)
            if joke_response:
                print("Here's a joke:")
                print(joke_response)
            else:
                print("No joke requested.")

        elif "what is" in query.lower() or "who is" in query.lower():
            user_message = query
            response = get_solution(user_message)
            if response:
                print("Here's your solution:")
                print(response)
            else:
                print("Sorry, I couldn't help you, right now")

        elif "tell me a short story" in query.lower():
            story = get_short_story()
            say(story)

        elif "where is" in query.lower():
            location = query
            place = location.split()
            if place:
                last_word = place[-1]
            else:
                last_word = None
            maps(last_word)

        elif "time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Aadi, it's {strfTime}. Is there anything else you'd like to know?")
        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")  # Format current date
            say(f"Today, The date is {current_date}. How else can I help you?")

        elif f"{query}".lower() in elly:
            say("""
                        I am elly a dedicated Virtual assistant, 
                        designed and developed by Aadi, to enhance your daily life. 
                        With a blend of intelligence and personality, 
                        I am your reliable companion for a wide range of tasks and interactions. 
                        Whether you need assistance with organizing your schedule, answering questions, or simply engaging in friendly conversations, 
                        I am always at your service. With my intuitive understanding and adaptability, 
                        I am here to make your life easier and more enjoyable. 
                        """)

        elif any(compliment in query.lower() for compliment in compliments):
            say("Feel free to ask anything.")

        elif "olama" in query.lower():
            say("Running Ollama")
            os.system("start cmd.exe /c ollama run llama2")

        elif f"{query}".lower() in ai:
            get_solution(query)

        elif "text input" in query.lower():
            texttospeech()

        elif "input" in query.lower():
            query = input("Text: ")
            get_solution(query)

        elif "morning" in query.lower():
            greet()
            takeCommand()
        elif "afternoon" in query.lower():
            greet()
            takeCommand()
        elif "evening" in query.lower():
            greet()
            takeCommand()

        elif "close" in query.lower():
            # Simulate pressing Alt + F4
            pyautogui.hotkey('alt', 'f4')

        elif "delete" in query.lower():
            pyautogui.hotkey('delete')

        elif "enter" in query.lower():
            pyautogui.hotkey('enter')

        elif "change tab" in query.lower():
            pyautogui.hotkey('alt', 'tab')

        elif "minimize" in query.lower() or "minimise" in query.lower():
            pyautogui.hotkey('win', 'd')

        # Functions for Chrome
        elif "change chrome tab" in query.lower():
            pyautogui.hotkey('ctrl', 'tab')

        # For mainly Chrome
        elif "change to tab 1" in query.lower():
            pyautogui.hotkey('ctrl', '1')
        elif "change to tab 2" in query.lower() or "change to tab to" in query.lower():
            pyautogui.hotkey('ctrl', '2')
        elif "change to tab 3" in query.lower():
            pyautogui.hotkey('ctrl', '3')
        elif "downloads" in query.lower():
            pyautogui.hotkey('ctrl', 'j')
        elif "history" in query.lower():
            pyautogui.hotkey('ctrl', 'h')
        elif "wait" in query.lower() or "pause" in query.lower():
            pyautogui.hotkey('space')
        elif "continue" in query.lower() or "play" in query.lower():
            pyautogui.hotkey('k')
        elif "mute" in query.lower():
            pyautogui.hotkey('m')

        elif f"{query}".lower() in bye:
            say("Take Care Aadi, I am always here to help you.")
            break
# End
