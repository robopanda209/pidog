#!/bin/bash

# Pidog Gemini Dependencies Installation Script
# This script installs all required dependencies for running Pidog with Google Gemini

echo "=================================="
echo "Pidog Gemini Dependencies Installer"
echo "=================================="

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y python3-pyaudio sox flac libsox-fmt-all

# Install Python packages
echo "Installing Python packages..."

# Core Gemini package
echo "Installing Google Generative AI (Gemini)..."
sudo pip3 install -U google-generativeai --break-system-packages

# Text-to-Speech dependencies
echo "Installing Text-to-Speech dependencies..."
sudo pip3 install -U gtts --break-system-packages
sudo pip3 install -U pygame --break-system-packages

# Speech recognition
echo "Installing speech recognition..."
sudo pip3 install SpeechRecognition --break-system-packages

# Image processing
echo "Installing image processing..."
sudo pip3 install -U Pillow --break-system-packages

# Audio processing
echo "Installing audio processing..."
sudo pip3 install -U sox --break-system-packages

# Create tts directory if it doesn't exist
echo "Creating tts directory..."
mkdir -p ./tts

echo "=================================="
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get your Google Gemini API key from: https://makersuite.google.com/app/apikey"
echo "2. Edit gemini_keys.py and add your API key"
echo "3. Run: sudo python3 gemini_dog.py"
echo "==================================" 