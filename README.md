# SpotiSearch (Currently still a WIP)

Website that allows a user to see the top 10 songs from a query search of an artist's name. Links to songs will be hyperlinked. Will redirect to Spotify.

## Local Installation Guide

### Requirements
- Python (preferably the latest version)
- Spotify Developer Account
- Application through Spotify Developer Portal

1. `git clone` this repository.
2. `cd SpotiSearch`
3. `pip install -r requirements.txt`
4. `touch .env`
5. `vim .env`
6. Enter `CLIENT_ID` and `CLIENT_SECRET` tokens into the `.env` file. These should be from the application you created through the SDP.
7. `python3 main.py`
8. The terminal should have generated an IP address at which your localhost is live. Enter that IP address in your browser search bar.
9. `Ctrl+C` in Terminal when finished.

## To Do
1. Add basic/advanced CSS.
2. Show images for album covers of songs.
3. Make images hyperlinks.
4. Deploy somewhere on internet.
5. Add a showing of how many streams the song has in place of popularity indicator.
6. Dropdown list of artists after search.
7. Select from a list of countries and then show the top 10 songs in that country.
    - Across languages.
    - For a specific language.
