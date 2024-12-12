import discord
from discord.ext import commands
import torch
from TTS.api import TTS
import soundfile as sf
import numpy as np
import json
import os
import re
import asyncio

# Discord bot initialization
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Configuration
MAX_TEXT_LENGTH = 300  # Character limit for input text
MAX_AUDIO_SIZE = 8_000_000  # 8 MB file size limit
TARGET_CHANNEL_ID = 123456789  # Replace with the actual channel ID
speakers = {}

# Load speakers from JSON file
def load_speakers():
    global speakers
    with open("speakers.json", "r") as f:
        speakers = json.load(f)

@bot.event
async def on_ready():
    load_speakers()
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        speaker_list = "\n".join([f"Number {num}: {info['name']}" for num, info in speakers.items()])
        await channel.send(f"Bot is online! Use !go to start. Available speakers:\n\n{speaker_list}")

user_sessions = {}

@bot.command(name="go")
async def go_command(ctx):
    user_sessions[ctx.author.id] = {"step": "awaiting_number"}
    await ctx.send("Enter the speaker number.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id in user_sessions:
        session = user_sessions[message.author.id]
        if session["step"] == "awaiting_number":
            if message.content.isdigit() and message.content in speakers:
                session["speaker_id"] = message.content
                session["step"] = "awaiting_text"
                await message.channel.send("Enter the text (max 300 characters).")
            else:
                await message.channel.send("Invalid number. Try again.")
        elif session["step"] == "awaiting_text":
            if len(message.content) <= MAX_TEXT_LENGTH:
                session["text"] = message.content
                await save_text_to_file(message.content, message.author.id)
                await clear_conversation(message.channel, message.author)
                await message.channel.send("Text received! Generating audio...")
                await generate_and_send_audio(message.channel, session)
                user_sessions.pop(message.author.id)
            else:
                await message.channel.send(f"Text exceeds {MAX_TEXT_LENGTH} characters. Please try again.")
# optional 
async def save_text_to_file(text, user_id):
    with open(f"text_{user_id}.txt", "a", encoding="utf-8") as file:
        file.write("\n" + text)

async def clear_conversation(channel, user):
    async for msg in channel.history(limit=50):
        if msg.author == user or msg.author == bot.user:
            await msg.delete()

# Generate and send audio file
async def generate_and_send_audio(channel, session):
    speaker_wav = speakers[session["speaker_id"]]["file"]
    text = session["text"]
    output_file = await asyncio.to_thread(create_audio, text, speaker_wav)
    if output_file and os.path.getsize(output_file) <= MAX_AUDIO_SIZE:
        await channel.send(file=discord.File(output_file))
        os.remove(output_file)
    else:
        await channel.send("Audio generation failed or file is too large.")
    await channel.send("Bot is ready for new commands.")

# Generate audio using TTS
def create_audio(text, speaker_wav, language="en"): 
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    segments = split_text(text)
    audio_data = []
    for i, segment in enumerate(segments):
        temp_output_path = f"temp_segment_{i}.wav"
        tts.tts_to_file(text=segment, speaker_wav=speaker_wav, language=language, file_path=temp_output_path)
        segment_data, samplerate = sf.read(temp_output_path)
        audio_data.append(segment_data)
        os.remove(temp_output_path)
    final_audio = np.concatenate(audio_data)
    output_path = "output_audio.wav"
    sf.write(output_path, final_audio, samplerate)
    return output_path if os.path.getsize(output_path) <= MAX_AUDIO_SIZE else None

# Split text into smaller segments
def split_text(text, max_length=50):
    sentences = re.split(r'(?<=[.!?]) +', text)
    segments, current_segment = [], []
    current_length = 0
    for sentence in sentences:
        words = sentence.split()
        if current_length + len(words) > max_length:
            segments.append(" ".join(current_segment))
            current_segment, current_length = [], 0
        current_segment.extend(words)
        current_length += len(words)
    if current_segment:
        segments.append(" ".join(current_segment))
    return segments

bot.run(DISCORD_TOKEN)
