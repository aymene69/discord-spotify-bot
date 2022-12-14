# Discord.py Spotify bot!

This is a simple Discord.py bot with basic commands to play Spotify tracks to a voice channel.
THIS DOESN'T DOWNLOAD SOUNDS FROM YOUTUBE ACCORDING TO THE SPOTIFY SONG! IT PLAYS DIRECTLY FROM SPOTIFY!

THIS NEEDS A PREMIUM SPOTIFY ACCOUNT

THIS IS RAN ON A VPS WITH NO DISPLAYS.

# Installation

## Spotifyd installation
If you are using Ubuntu, you can continue these explanations. If not, please refer to [Spotifyd official wiki](https://spotifyd.github.io/spotifyd/installation/index.html) and do not forget to install with Pulseaudio backend option!

1) First download Rustup. If you have any other Rust installation, please remove it.
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
2) Install Spotifyd requirements
```sh
apt install libasound2-dev libssl-dev pkg-config build-essential
```
3) Clone the repository
```sh
git clone https://github.com/Spotifyd/spotifyd.git
```
4) Compile Spotifyd
```sh
cd spotifyd
cargo build --release --no-default-features --features pulseaudio_backend
```
This will compile Spotifyd and place it in target/release/
5) Configuring Spotifyd
You will need to create two folders:
```sh
mkdir ~/.config ~/.config/spotifyd
```
Copy the content of the config file named spotifyd.conf and paste it:
```sh
nano ~/.config/spotifyd/spotifyd.conf # paste it here and hit ctrl+x and hit y and enter, don't forget to fill the username and password of your spotify account
```
6) Creating service
Copy the spotifyd executable to /usr/bin
```sh
cp target/release/spotifyd /usr/bin
```
Copy the file `spotifyd.service` in /etc/systemd/user/
Execute the following commands
```sh
systemctl enable --user spotifyd.service
systemctl start --user spotifyd.service
systemctly status --user spotifyd.service
```
You are now done for Spotifyd

## Pulseaudio installation
1) First download Pulseaudio
```sh
apt-get install pulseaudio
```
2) Create needed devices
```sh
pulseaudio -D
pactl load-module module-null-sink sink_name=vspeaker sink_properties=device.description=virtual_speaker
pactl load-module module-remap-source master=vspeaker.monitor source_name=vmic source_properties=device.description=virtual_mic
```
3) Relaunch Spotifyd
```
systemctly stop --user spotifyd.service
systemctly start --user spotifyd.service
```
## Python modules installation
1) Install Discord.py voice
```sh
python3 -m pip install -U "discord.py[voice]"
```
2) Install spotipy
```sh
python3 -m pip install spotipy
```
3) Copy .cache file to your server
On your computer, install Python3 and install spotipy. Then, launch a py session and copy paste the next lines in your terminal:
```py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENTID", # Your Spotify Client ID
                                               client_secret="CLIENTSECRET", # Your Spotify Client Secret
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=["user-library-read", "streaming", "user-read-currently-playing", "user-read-playback-state"]))

results = sp.current_user_saved_tracks()
```
This should launch your browser and ask you to connect yo your Spotify account. Connect and close the python terminal. You will normally have a .cache file. Copy its content and paste it in ~/.cache file. If there is a folder named .cache, remove it with `rm -r ~/.cache`

This is needed to make your bot connected to Spotify.

Connect to your Spotify account. Select "Discord" in your listening devices.

You will now simply have to modify the bot variables and token, and launch it with `python3 bot.py`

If you have any problem, feel free to open an issue. I will be glad to help.
