# Discord TTS Bot

## Overview
This bot is a Discord-based Text-to-Speech (TTS) application that allows users to generate and share audio files using pre-defined speaker profiles. Users can select a speaker, input text, and receive an audio file generated using the selected speaker's voice.

## Features
- Select from a list of predefined speakers.
- Input text and receive a generated audio file.
- Automatically manages file size to stay within Discord's upload limits.
- Clears previous conversation messages for a clean user experience.

---

## Setup and Requirements

### Prerequisites
1. **Python**: Ensure Python 3.8 or later is installed on your system.
2. **Libraries**: Install the required Python libraries:
    ```bash
    pip install discord.py torch TTS soundfile numpy
    ```
3. **Discord Bot Token**: Obtain a bot token from the [Discord Developer Portal](https://discord.com/developers/applications) and replace `YOUR_DISCORD_TOKEN` in the code with your bot token.
4. **Speaker Profiles**: Create a `speakers.json` file to define available speakers.
   Example structure:
   ```json
   {
       "1": {"name": "Tom Holland", "file": "audios/holland.wav"},
       "2": {"name": "Olivia Rodrigo", "file": "audios/olivia.wav"}
   }
   ```
   Ensure the corresponding `.wav` files are stored in the `audios` directory.

5. **TTS Model Files**: The bot uses the `TTS` library. Ensure the model `tts_models/multilingual/multi-dataset/xtts_v2` is available and accessible.

---

## How It Works

### Bot Workflow
1. **Startup**:
   - The bot loads speaker profiles from `speakers.json`.
   - Sends a welcome message in the target Discord channel with a list of available speakers.

2. **User Interaction**:
   - Use the `!go` command to start an interaction.
   - Select a speaker by entering its number.
   - Provide the text (max 300 characters) to be converted into audio.
   - The bot generates the audio file and uploads it to the channel.

3. **Audio Generation**:
   - Text is split into manageable segments for TTS processing.
   - The segments are synthesized using the TTS model and combined into a single audio file.
   - The bot checks file size before uploading to Discord.

---

## Steps to Run
1. Clone or download the project files.
2. Ensure the prerequisites are met (see above).
3. Replace `YOUR_DISCORD_TOKEN` with your bot token.
4. Place the `speakers.json` file and `.wav` files in the appropriate directories.
5. Run the bot:
   ```bash
   python bot.py
   ```
6. Invite the bot to your server using the OAuth2 URL from the Discord Developer Portal.

---

## Extending the Bot

### Adding More Voices
1. Add a new entry to the `speakers.json` file:
   ```json
   "3": {"name": "New Speaker", "file": "audios/new_speaker.wav"}
   ```
2. Place the corresponding `.wav` file (`new_speaker.wav`) in the `audios` directory.
3. Restart the bot to load the updated `speakers.json`.

### Customizing Limits
- **Text Length**: Modify `MAX_TEXT_LENGTH` in the code to increase or decrease the text input limit.
- **File Size**: Adjust `MAX_AUDIO_SIZE` to fit your Discord server's upload limits.

### Changing the TTS Model
- Replace `tts_models/multilingual/multi-dataset/xtts_v2` with another compatible model path supported by the `TTS` library.

---

## Important Notes on Voice Usage
Using voices of real individuals without their consent may violate their privacy and intellectual property rights. Before adding new voices, ensure that:
- You have explicit permission from the person whose voice is being used.
- The voice files comply with local laws and regulations.
- The use of the voice adheres to Discord's and other applicable terms of service.

Failure to follow these guidelines can result in legal consequences or account bans.

---

## Troubleshooting
1. **Bot Not Responding**:
   - Verify the bot token and intents configuration.
   - Check if the bot is properly invited to the server.

2. **Audio Generation Fails**:
   - Ensure the `.wav` files are valid and accessible.
   - Confirm the TTS model is correctly installed.

3. **File Size Exceeds Limit**:
   - Reduce input text length.
   - Optimize audio settings or split the output into smaller files.

---

## License
This project is open-source and available for modification. Ensure compliance with Discord's and TTS library's terms of use when deploying the bot.

