# Pidog

Pidog Python library for Raspberry Pi.

Quick Links:

- [Pidog](#pidog)
  - [Docs](#docs)
  - [Installation](#installation)
  - [AI Integration](#ai-integration)
  - [About SunFounder](#about-sunfounder)
  - [Contact us](#contact-us)
  - [Credit](#credit)

----------------------------------------------

## Docs

- <https://docs.sunfounder.com/projects/pidog/en/latest/>

----------------------------------------------

## Installation

- <https://docs.sunfounder.com/projects/pidog/en/latest/python/python_start/install_all_modules.html>

### install tool

```bash
sudo apt install git python3-pip python3-setuptools python3-smbus
```

### robot-hat library

```bash
cd ~/
git clone -b v2.0 https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install

```

### vilib library

```bash
cd ~/
git clone -b picamera2 https://github.com/sunfounder/vilib.git
cd vilib
sudo python3 install.py
```

### pidog library

```bash
cd ~/
git clone https://github.com/sunfounder/pidog.git
cd pidog
sudo python3 setup.py install
```

### i2samp

```
cd ~/pidog
sudo bash i2samp.sh
```

----------------------------------------------

## AI Integration

Pidog supports AI-powered conversations and interactions through both OpenAI GPT and Google Gemini.

### OpenAI GPT Integration

Located in `gpt_examples/` directory:
- Full conversational AI with voice interaction
- Vision capabilities for image analysis
- OpenAI's Whisper for speech-to-text
- OpenAI's TTS for natural voice responses
- See `gpt_examples/README.md` for setup instructions

### Google Gemini Integration

Located in `gpt_examples/` directory:
- **NEW**: Alternative to OpenAI using Google's Gemini AI
- Free tier available with competitive performance
- Multimodal capabilities (text + vision)
- Google Speech Recognition and Google TTS
- See `gpt_examples/gemini_README.md` for setup instructions

**Quick Start with Gemini:**
```bash
cd gpt_examples
# Edit gemini_keys.py with your API key from https://makersuite.google.com/app/apikey
sudo python3 gemini_dog.py
```

----------------------------------------------

## About SunFounder

SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strives to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project. If you have interest in open source or making something cool, welcome to join us!

----------------------------------------------

## Contact us

website:
    www.sunfounder.com

E-mail:
    service@sunfounder.com, support@sunfounder.com

## Credit

Most sound effect are from [Zapsplat.com](https://www.zapsplat.com)
