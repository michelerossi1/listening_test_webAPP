# Listening Test Web Application

This project is a web application designed to conduct listening tests, where participants evaluate songs based on emotional reactions. Users rate various emotional states such as "Aggressive," "Relaxed," "Happy," and "Sad" while listening to different audio tracks. The collected data helps analyze the relationship between music and emotional response.

## Features

- **Emotion-Based Song Evaluation**: Allows users to rate songs on emotional scales from -3 (Strongly Opposed) to +3 (Strongly Present).
- **Customizable Song Progression**: Users move through a sequence of songs and evaluate each one independently.
- **Break Intervals**: The app provides "Take a Break" prompts to help participants pause, creating a balanced experience during longer listening sessions.
- **Progress Tracking**: Visual progress bar updates as users advance through the list of songs.

## Technology Stack

- **Backend**: Python (Flask) for routing and managing session data.
- **Frontend**: HTML, CSS (Bootstrap) for responsive and visually appealing forms and controls.
- **Audio**: Supports audio playback and custom sliders for rating emotions.

## Getting Started

### Prerequisites

Ensure you have Python installed, along with Flask for web development:

```bash
pip install Flask
