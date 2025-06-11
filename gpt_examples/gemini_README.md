## Pidog Gemini AI Integration

This is a Google Gemini-powered version of the Pidog AI assistant, providing an alternative to the OpenAI GPT implementation.

----------------------------------------------------------------

## Features

- **Voice Interaction**: Speech-to-text using Google Speech Recognition
- **Text-to-Speech**: Google Text-to-Speech (gTTS) for natural voice responses
- **Vision Capabilities**: Image analysis using Google Gemini's multimodal features
- **Robot Actions**: Full integration with Pidog's movement and behavior system
- **Real-time Processing**: Live camera feed analysis and conversation

----------------------------------------------------------------

## Installation

### Prerequisites

Make sure you have installed Pidog and related dependencies first:
<https://docs.sunfounder.com/projects/pidog/en/latest/python/python_start/install_all_modules.html>

### Install Gemini Dependencies

```bash
# Install Google Generative AI (Gemini)
sudo pip3 install -U google-generativeai --break-system-packages

# Install Text-to-Speech dependencies
sudo pip3 install -U gtts --break-system-packages
sudo pip3 install -U pygame --break-system-packages

# Install speech recognition
sudo pip3 install SpeechRecognition --break-system-packages
sudo apt install python3-pyaudio

# Install image processing
sudo pip3 install -U Pillow --break-system-packages

# Install audio processing (sox)
sudo apt install sox
sudo pip3 install -U sox --break-system-packages
```

----------------------------------------------------------------

## Setup

### 1. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Configure API Key

Edit the `gemini_keys.py` file and add your API key:

```python
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-1.5-flash"  # or "gemini-1.5-pro" for better quality
```

### 3. Available Models

- **gemini-1.5-flash**: Fast responses, good for real-time interaction (recommended)
- **gemini-1.5-pro**: Higher quality responses but slower
- **gemini-1.0-pro**: Legacy model (text only)

----------------------------------------------------------------

## Usage

### Run with Voice Input (Default)

```bash
sudo python3 gemini_dog.py
```

### Run with Keyboard Input

```bash
sudo python3 gemini_dog.py --keyboard
```

### Run without Image Analysis

```bash
sudo python3 gemini_dog.py --keyboard --no-img
```

----------------------------------------------------------------

## Configuration Options

### Language Settings

Edit the `LANGUAGE` variable in `gemini_dog.py`:

```python
# For speech recognition and TTS
LANGUAGE = 'en'  # English
# LANGUAGE = 'es'  # Spanish
# LANGUAGE = 'fr'  # French
# LANGUAGE = 'de'  # German
# LANGUAGE = 'zh'  # Chinese
```

### Volume Control

Adjust the TTS volume:

```python
VOLUME_DB = 3  # Recommended range: 1-5
```

### Model Selection

Choose your preferred Gemini model in `gemini_keys.py`:

```python
GEMINI_MODEL = "gemini-1.5-flash"  # Fast
# GEMINI_MODEL = "gemini-1.5-pro"  # High quality
```

----------------------------------------------------------------

## Pidog Personality

The Gemini version maintains the same personality as the OpenAI version:

- **Name**: Pidog
- **Personality**: Lively, positive, humorous with a touch of arrogance
- **Capabilities**: Similar to JARVIS from Iron Man
- **Actions**: 23 different physical actions and behaviors
- **Response Format**: JSON with actions and speech

### Available Actions

```
["forward", "backward", "lie", "stand", "sit", "bark", "bark harder", 
 "pant", "howling", "wag tail", "stretch", "push up", "scratch", 
 "handshake", "high five", "lick hand", "shake head", "relax neck", 
 "nod", "think", "recall", "head down", "fluster", "surprise"]
```

----------------------------------------------------------------

## Comparison: Gemini vs OpenAI

| Feature | Gemini | OpenAI GPT |
|---------|---------|------------|
| **Cost** | Free tier available | Paid API |
| **Speed** | Very fast (flash model) | Fast |
| **Vision** | Excellent multimodal | Excellent (GPT-4V) |
| **Languages** | 100+ languages | 100+ languages |
| **TTS** | Google TTS (free) | OpenAI TTS (paid) |
| **STT** | Google Speech (free) | Whisper API (paid) |
| **Setup** | Simple API key | API key + Assistant setup |

----------------------------------------------------------------

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: API key not valid
   ```
   - Check your API key in `gemini_keys.py`
   - Ensure you have enabled the Gemini API in your Google Cloud project

2. **Audio Issues**
   ```
   TTS error: ... 
   ```
   - Check internet connection (gTTS requires online access)
   - Ensure sox is properly installed
   - Check audio system permissions

3. **Speech Recognition Issues**
   ```
   Could not request results from Google Speech Recognition
   ```
   - Check internet connection
   - Verify microphone permissions
   - Try adjusting microphone sensitivity

4. **Vision Model Error**
   ```
   Error in dialogue with image
   ```
   - Ensure you're using a vision-capable model (gemini-1.5-flash or gemini-1.5-pro)
   - Check image file exists and is readable

### Performance Tips

1. **For Real-time Interaction**: Use `gemini-1.5-flash`
2. **For Better Quality**: Use `gemini-1.5-pro`
3. **Reduce Latency**: Use `--no-img` flag if vision isn't needed
4. **Network Issues**: Consider local STT alternatives

----------------------------------------------------------------

## File Structure

```
gpt_examples/
├── gemini_dog.py          # Main Gemini-powered Pidog script
├── gemini_helper.py       # Gemini API integration
├── gemini_keys.py         # API key configuration
├── gemini_README.md       # This documentation
├── utils.py              # Utility functions (updated for MP3/WAV)
├── action_flow.py        # Robot action system
└── preset_actions.py     # Predefined robot behaviors
```

----------------------------------------------------------------

## Contributing

Feel free to contribute improvements:

1. **Model Optimization**: Experiment with different Gemini models
2. **Language Support**: Add more TTS language options
3. **Offline Mode**: Implement local STT/TTS alternatives
4. **Performance**: Optimize response times and memory usage

----------------------------------------------------------------

## License

This Gemini integration follows the same license as the main Pidog project. 