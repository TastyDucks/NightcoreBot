# NightcoreBot
Automated creation and uploading of "nightcore" remixes of various songs in Python.

## Installation

### Core installation requirements

You will need to install the following dependencies:

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/#Download)
- [FFmpeg](https://www.ffmpeg.org/download.html)
- [FFmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [pydub](https://github.com/jiaaro/pydub)
- [pytube](https://github.com/nficano/pytube)

You can easially install four of these libraries with pip:

```bash
pip install beautifulsoup4
pip install ffmpeg-python
pip install pydub
pip install pytube
```

Finally, install FFmpeg.

### Additional installation requirements

**IMPORTANT*: You will need to do these additional steps if you plan to automatically upload your videos to Youtube.*

Install the following dependencies:

- [Google API Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)

Again, pip is your friend:

```bash
pip install google-api-python-client
```

## Usage

Use `python3 NightcoreBot.py --help` to view the command syntax.

### Miscellaneous I/O information

- Sources for nightcore songs may be either local files or Youtube videos. NightcoreBot supports *only* mp3 files.
- Files output locally will share the same title as their source file or Youtube video.
- In order to automatically upload Nightcore remixes to Youtube, the file `client_secrets.json` must be filled in with the required information from the [Youtube Developers Console](https://accounts.google.com/signin/v2/identifier?service=cloudconsole&passive=1209600&osid=1&continue=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fdevelopers.google.com%2Fyoutube%2Fv3%2Fguides%2Fuploading_a_video&followup=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fdevelopers.google.com%2Fyoutube%2Fv3%2Fguides%2Fuploading_a_video&flowName=GlifWebSignIn&flowEntry=ServiceLogin).
- Backgrounds for any created videos must be specified in `NightcoreBot.cfg` under `BackgroundSource`.
- The maximum and minimum pitch shifting rates must be specified in `Nightcorebot.cfg` under ``. The pitch shift applied to a song will be a random number within the range.
- NightcoreBot is **not** multithreaded, it creates one mix at a time.