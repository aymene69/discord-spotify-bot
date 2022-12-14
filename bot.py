from typing import Optional

import discord
from discord import app_commands
from discord.ext import tasks
import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENTID",
                                               client_secret="SECRET",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=["user-library-read", "streaming", "user-read-currently-playing", "user-read-playback-state"])) # Connecting to Spotify

results = sp.current_user_saved_tracks() # Checking if the .cache file is correctly set. If not, will open a link in your browser (if on a VPS, report to the VPS installation)


MY_GUILD = discord.Object(id=GUILDID)  # replace with your guild id


class Dropdown(discord.ui.Select):
    def __init__(self, optionss):
        options = optionss 
        super().__init__(placeholder='Choose a music to listen to:', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        track = sp.track(self.values[0])
        play = sp.start_playback(uris=[track['uri']])
        channel= interaction.user.voice.channel
        vc = await channel.connect()
        source = discord.FFmpegPCMAudio(source="0", executable="ffmpeg", pipe=False, before_options="-f pulse")
        vc.play(source)
        await interaction.response.send_message(f'{interaction.user.mention}, **{track["name"]}** from **{", ".join(elem["name"] for elem in track["artists"])}** listening!')


class DropdownView(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.add_item(Dropdown(options))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    currentCheck.start()

@client.event
async def on_voice_state_update(member, before, after):
    vc = client.get_channel(before.channel.id)
    if len(vc.members) == 1:
        sp.pause_playback()
        vc = client.get_guild(GUILDID).voice_client
        await vc.disconnect()

@client.tree.command()
@app_commands.rename(lien='spotify_link')
@app_commands.describe(lien='Link of the Spotify track that you want to listen to (a track, not an album!)')
async def play(interaction: discord.Interaction, lien: str):
    """Allows to change the music"""
    channel= interaction.user.voice.channel
    vc = await channel.connect()
    source = discord.FFmpegPCMAudio(source="1", executable="ffmpeg", pipe=False, before_options="-f pulse")
    vc.play(source)
    track = sp.track(lien)
    play = sp.start_playback(uris=[track['uri']])
    await interaction.response.send_message(f'{interaction.user.mention}, **{track["name"]}** from **{", ".join(elem["name"] for elem in track["artists"])}** listening!')

@client.tree.command()
async def pause(interaction: discord.Interaction):
    """Pauses the music or resumes it"""
    current = sp.current_playback()
    if(current['is_playing']):
        sp.pause_playback()
        await interaction.response.send_message(f'{interaction.user.mention}, paused!')
    else:
        sp.start_playback()
        await interaction.response.send_message(f'{interaction.user.mention}, resumed!')

@client.tree.command()
async def stop(interaction: discord.Interaction):
    """Stops the music"""
    sp.pause_playback()
    vc = client.get_guild(GUILDID).voice_client
    await vc.disconnect()
    await interaction.response.send_message(f'{interaction.user.mention}, music stopped!')

@client.tree.command()
@app_commands.rename(lien='spotify_link')
@app_commands.describe(lien='Link of the Spotify track that you want to listen to (track, not an album)')
async def queue(interaction: discord.Interaction, lien: str):
    """Adds a track to the listening queue"""
    track = sp.track(lien)
    play = sp.add_to_queue(uri=track['uri'])
    titre = track['name']
    artistes = track['artists'][0]['name']
    await interaction.response.send_message(f'{interaction.user.mention}, **{track["name"]}** from **{", ".join(elem["name"] for elem in track["artists"])}** added to the queue!')

@client.tree.command()
async def next(interaction: discord.Interaction):
    """Skips to the next music"""
    sp.next_track()
    current = sp.current_playback()
    titre = current['item']['name']
    artistes = current['item']['artists'][0]['name']
    await interaction.response.send_message(f'{interaction.user.mention}, **{titre}** from **{artistes}** listening!')

@client.tree.command()
async def en_ecoute(interaction: discord.Interaction):
    """Shows the now listening track"""
    current = sp.current_playback()
    titre = current['item']['name']
    artistes = current['item']['artists'][0]['name']
    await interaction.response.send_message(f'{interaction.user.mention}, en écoute: **{titre}** de **{artistes}** !')


@client.tree.command()
@app_commands.rename(recherche='recherche')
@app_commands.describe(recherche='Your research')
async def search(interaction: discord.Interaction, recherche: str):
    """Searches a track and plays it"""
    result = sp.search(recherche, limit=5)
    resultats = []
    for elem in result['tracks']['items']:
        resultats.append(discord.SelectOption(label=elem['name'], description=elem['name'] + " - " + ", ".join(elem["name"] for elem in elem["artists"]), emoji='▶️', value=elem['uri']))
    view = DropdownView(resultats)

    await interaction.response.send_message(view=view)

@tasks.loop(seconds=5)
async def currentCheck():
    current = sp.current_playback()
    try:
        if(current['is_playing']):
            titre = current['item']['name']
            artistes = current['item']['artists'][0]['name']
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=titre + " - " + artistes))
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your orders"))
    except:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your orders"))



client.run('TOKEN')
