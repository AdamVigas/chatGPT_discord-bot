# bot.py

import discord
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the Discord client
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Event listener for when the bot has connected to Discord
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event listener for when a message is sent in the server
@client.event
async def on_message(message):
    # Avoid responding to the bot's own messages
    if message.author == client.user:
        return

    # Process the message content
    user_message = message.content

    try:
        # Use OpenAI's ChatCompletion API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        # Get the response text
        response_text = response.choices[0].message['content'].strip()

        # Send the response back to the Discord channel
        await message.channel.send(response_text)

    except openai.error.RateLimitError:
        await message.channel.send("I'm currently experiencing high usage. Please try again later.")

    except openai.error.OpenAIError as e:
        await message.channel.send(f"An error occurred: {str(e)}")

# Run the bot
client.run(DISCORD_TOKEN)
