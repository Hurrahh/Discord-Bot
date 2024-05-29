import discord
import google.generativeai as genai

token = "Your Token"
api_key = "Your gemini api key"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message):

        try:
            channel = message.channel
            print(f'Message from {message.author}: {message.content}')
            if self.user != message.author:
                if self.user in message.mentions:
                    if any(message.content.lower().startswith(greeting) for greeting in ["hi", "hello", "hey"]):
                        await channel.send("Hi there!")
                    else:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(message.content)
                        response_text = response.text.replace("#", "").replace("*", "")
                        print(response_text)
                        with open("users.txt",'a') as file:
                            x = file.write(f"1. {message.author}:  {message.content} \n  HurrahGPT:  {response_text}")
                        await channel.send(response_text)
        except Exception as e:
            print(e)




if __name__ == "__main__":
    print("Starting the bot")
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(token)