# Elly - A Virtual AI Assistant

This repository contains the source code for a Virtual AI Assistant named **Elly**. Elly can perform various tasks like telling jokes, playing music, searching for information, controlling applications, and more. The assistant leverages APIs like Groq and Google Cloud YouTube Data API to provide interactive and personalized experiences.

---

## Features

### 🎵 Music and Entertainment
- **Play Music from Folder**: Plays random MP3 files from a specified folder.
- **Play Songs on YouTube**: Searches and plays specific songs on YouTube using the Google Cloud YouTube API.
- **Tell Jokes**: Uses the Groq API to deliver a random joke.
- **Short Stories**: Fetches and narrates random short stories for children.

### 🌐 Information and Search
- **Wikipedia Search**: Retrieves summaries from Wikipedia.
- **General Questions**: Answers questions using the Groq API.
- **Search the Web**: Opens and searches popular websites like YouTube, Google, and Wikipedia.

### 💻 System and App Control
- **Open Applications**: Launches applications like Chrome, Notepad, Discord, and more.
- **Open Websites**: Quickly opens pre-defined websites like Google, YouTube, and GitHub.
- **Shutdown System**: Automates system shutdown with a countdown timer.

### 🗺 Maps and Navigation
- **Search Locations**: Opens specified locations in Google Maps.

### 🗣 Voice Interaction
- **Voice Recognition**: Listens to user commands using a microphone.
- **Text-to-Speech**: Converts responses to audio using Google Text-to-Speech (gTTS).

---

## Technologies and Libraries Used

### APIs
- **Groq API**: For joke generation and question answering.
- **Google Cloud YouTube Data API**: For searching and playing songs on YouTube.

### Python Libraries
- `speech_recognition`: For capturing and recognizing user voice commands.
- `wikipedia`: For fetching summaries from Wikipedia.
- `webbrowser`: To open websites in the default browser.
- `pygame`: For playing local MP3 files.
- `gTTS`: For converting text to speech.
- `pydub`: For audio manipulation and playback.
- `requests` & `BeautifulSoup`: For web scraping short stories.
- `json`: For loading API keys.

---

## Installation and Setup

### Prerequisites
- Python 3.7 or later
- Install required libraries using `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### Configure API Keys
1. Create a `key.json` file in the root directory.
2. Add your API keys in the following format:
   ```json
   {
     "API_KEY_YT": "YOUR_YOUTUBE_API_KEY",
     "API_KEY_GROQ": "YOUR_GROQ_API_KEY"
   }
   ```

### Usage
1. Run the `main.py` script:
   ```bash
   python main.py
   ```
2. Use voice commands to interact with Elly. Examples:
   - "Play music."
   - "Search for Python programming."
   - "Open Google."
   - "Tell me a joke."
   - "Where is New York?"

---

## File Structure
```
.
├── key.json            # API keys
├── main.py             # Main script
├── requirements.txt    # Requirements
└── README.md           # Documentation
```

---

## Future Improvements
- Integrate more APIs for advanced functionalities.
- Add support for multi-language voice recognition and responses.
- Enhance error handling for seamless user experience.
- Add machine learning for personalized interactions.

---

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests.
