import random
import discord
import feedparser
import asyncio
import json
import os

def load_config():
    with open('config.json') as f:
        return json.load(f)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

posted_videos = []

async def handle_uploads():
    config = load_config()
    channel_id = config["channel"]
    channel = client.get_channel(channel_id)
    
    if channel is None:
        print("Didn't found the YT channel")
        return
    
    while True:
        feed = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={config["channel_id"]}')
        if feed.entries:
            video_link = feed.entries[0].link
            if video_link not in posted_videos:
                posted_videos.append(video_link)
                message = config["messageTemplate"].format(
                    author=feed.entries[0].author,
                    title=feed.entries[0].title,
                    url=video_link
                )
                await channel.send(message)
        await asyncio.sleep(config["watchInterval"] / 1000)  

@client.event
async def on_ready():
    print("Lets goo")
    await handle_uploads()

# Load configuration
if __name__ == "__main__":
    client.run(load_config()["token"])
