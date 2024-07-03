import os
import discord
import google.generativeai as genai
import asyncio
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# token = os.getenv('Discord_Token')
# api_key = os.getenv('GOOGLE_API_KEY')

token = st.secrets["token"]
api_key = st.secretes["api_key"]


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        try:
            channel = message.channel
            print(f'Message from {message.author}: {message.content}')

            if self.user != message.author:
                if message.content.startswith("!help"):
                    help_text = ("Hi! Here are the commands you can use:\n"
                                 "1. `@bot_name <message>` - Ask me anything and I'll try to help!\n"
                                 "2. `!help` - Display this help message.\n"
                                 "3. `!about` - Learn more about this bot.\n"
                                 "4. `!save <message>` - Save a message to a file.\n"
                                 "5. `!remind <seconds> <message>` - Set a reminder.\n")
                    await channel.send(help_text)

                elif message.content.startswith("!about"):
                    about_text = ("I'm a generative AI bot created to assist with code generation, "
                                  "image description, and general conversational tasks. Feel free to ask me anything!")
                    await channel.send(about_text)

                elif message.content.startswith("!save "):
                    content_to_save = message.content[len("!save "):]
                    with open("users.txt", 'a') as file:
                        file.write(f"{message.author}: {content_to_save}\n")
                    await channel.send("Your message has been saved!")

                elif message.content.startswith("!remind "):
                    try:
                        reminder_time, reminder_message = message.content[len("!remind "):].split(" ", 1)
                        reminder_time = int(reminder_time)
                        await channel.send(f"Reminder set! I will remind you in {reminder_time} seconds.")
                        await asyncio.sleep(reminder_time)
                        await channel.send(f"Reminder: {reminder_message}")
                    except ValueError:
                        await channel.send("Usage: !remind <seconds> <message>")

                elif self.user in message.mentions:
                    if any(message.content.lower().startswith(greeting) for greeting in ["hi", "hello", "hey"]):
                        await channel.send("Hi there!")
                    else:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(message.content)
                        response_text = response.text.replace("#", "").replace("*", "")
                        print(response_text)
                        with open("users.txt", 'a') as file:
                            file.write(f"{message.author}: {message.content}\nexample_bot: {response_text}\n")
                        await channel.send(response_text)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    print("Starting the bot")
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(token)
