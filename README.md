# NightcoreBot
Automated creation and uploading of "nightcore" remixes of various songs in Python.
This program uses way too many libraries. Half of these are redundant! Oh well.

## Installation

### Core installation requirements

You will need to install the following dependencies:

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/#Download)
- [FFmpeg](https://www.ffmpeg.org/download.html)
- [ffmpy](https://github.com/Ch00k/ffmpy)
- [pydub](https://github.com/jiaaro/pydub)
- [pytube](https://github.com/nficano/pytube)

You can easially install four of these libraries with pip:

```bash
pip install beautifulsoup4
pip install ffmpy
pip install pydub
pip install pytube
```

Finally, install FFmpeg.

### Additional installation requirements

**IMPORTANT*: You will need to do these additional steps if you plan to automatically upload your videos to Youtube.*

Install the following dependencies:

- [Google API Client Library for Python and related libraries](https://developers.google.com/youtube/v3/quickstart/python)
- [FLASK](http://flask.pocoo.org/)
- [Requests](http://docs.python-requests.org/en/master/)

Again, pip is your friend:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
pip install --upgrade flask
pip install --upgrade requests
```

## Usage

Use `python3 NightcoreBot.py --help` to view the command syntax.

### Configuration

The configuration file for NightcoreBot is `NightcoreBot.cfg`. NightcoreBot uses the ever-ubiquitous [JSON](https://www.json.org/) syntax as it is supported natively by Python.
Here is an explaination of each of the options in the file:

- A background image or directory containing multiple images must be specified under `BackgroundSource`. If a directory is listed, each video will have a randomly selected image as its background for the duration of the video.
- The speed-up rate of the processed songs is a random integer within the ranges specified under `SpeedupPercentage`, including both the lower and upper bounds.

### Miscellaneous I/O information

- Sources for nightcore songs may be either local files or Youtube videos. NightcoreBot supports *only* files encoded with mp3 audio, regardless of their container.
- Files output locally will share the same title as their source file or Youtube video.
- In order to automatically upload Nightcore remixes to Youtube, the file `client_secrets.json` must be filled in with the required information from the [Youtube Developers Console](https://accounts.google.com/signin/v2/identifier?service=cloudconsole&passive=1209600&osid=1&continue=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fdevelopers.google.com%2Fyoutube%2Fv3%2Fguides%2Fuploading_a_video&followup=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fdevelopers.google.com%2Fyoutube%2Fv3%2Fguides%2Fuploading_a_video&flowName=GlifWebSignIn&flowEntry=ServiceLogin).
- NightcoreBot is **not** multithreaded, it creates one mix at a time.
- When uploading to Youtube, NightcoreBot titles the video differently depending on the source type. (It should be noted that all of these types support the prefix and suffix described in the configuration file.)
  - If the source type is `Youtube URL`, the video will be titled `NightcoreBot Mix № D`, where `D` is the current date and time.
  - If the source type is `Youtube query`, the video will be titled the same as the query.
  - If the source type is `Local file`, the video will be titled with the name of the source file, without the file extension.