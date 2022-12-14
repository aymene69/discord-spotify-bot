# Discord.py Spotify bot!

This is a simple Discord.py bot with basic commands to play Spotify tracks to a voice channel.
THIS DOESN'T DOWNLOAD SOUNDS FROM YOUTUBE ACCORDING TO THE SPOTIFY SONG! IT PLAYS DIRECTLY FROM SPOTIFY!

THIS NEEDS A PREMIUM SPOTIFY ACCOUNT

# Installation

## Spotifyd installation
If you are using Ubuntu, you can continue these explanations. If not, please refer to [Spotifyd official wiki](https://spotifyd.github.io/spotifyd/installation/index.html) and do not forget to install with Pulseaudio backend option!

1) First download Rustup. If you have any other Rust installation, please remove it.
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
2) Install Spotifyd requirements
```sh
sudo apt install libasound2-dev libssl-dev pkg-config build-essential
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
This will compile Spotifyd and place it in spotifyd/target/release/

You are now done!

NEXT TBD.
