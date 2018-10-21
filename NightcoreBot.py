#!/usr/bin/env python3
"""The main script for NightcoreBot."""

#
# Imports
#

# Python imports

import argparse
import atexit
import json
import os
import random
import sys
import time

# Library imports

try:
    import bs4
except ImportError:
    Log("Required dependency \"Beautiful Soup 4\" is not installed.", 4)
    sys.exit()
try:
    import ffmpy
except ImportError:
    Log("Required dependency \"ffmpy\" is not installed.", 4)
    sys.exit()
try:
    import pydub
except ImportError:
    Log("Required dependency \"pydub\" is not installed.", 4)
    sys.exit()
try:
    import pytube
except ImportError:
    Log("Required dependency \"pytube\" is not installed.", 4)
    sys.exit()

#
# Important variables
#

NightcoreBotVersion = "1.0"
DefaultConfigFile = "{\n    \"VideoDimensions\":\n    {\n        \"Height\": 720,\n        \"Width\": 1280\n    },\n    \"SpeedupPercentage\":\n    {\n        \"LowerBound\": 20,\n        \"UpperBound\": 20\n    },\n    \"BackgroundSource\": \"Backgrounds\",\n    \"UploadTitlePrefix\": \"▶️ 🎵 \",\n    \"UploadTitleSuffix\": \" 🎶\"\n}"
DefaultSecretsFile = "{\n    \"web\": {\n      \"client_id\": \"[[INSERT CLIENT ID HERE]]\",\n      \"client_secret\": \"[[INSERT CLIENT SECRET HERE]]\",\n      \"redirect_uris\": [],\n      \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n      \"token_uri\": \"https://accounts.google.com/o/oauth2/token\"\n    }\n  }"

#
# Functions
#

def CheckCoreFiles(Overwrite = False):
    """
    Check to see if the important data files exist. Set Overwrite to True to create a new configuration file.
    """
    if not os.path.isfile("NightcoreBot.cfg"):
        Log("The configuration file does not exist, creating...", 2)
        try:
            with open("NightcoreBot.cfg", "w", encoding="utf-8") as File:
                File.write(DefaultConfigFile)
        except IOError:
            Log("IOError: unable to create configuration file.", 4)
            sys.exit()
    if not os.path.isfile("client_secrets.json"):
        Log("The client secrets file does not exist, creating...", 2)
        try:
            with open("client_secrets.json", "w") as File:
                File.write(DefaultSecretsFile)
        except IOError:
            Log("IOError: unable to create client secrets file.", 4)
            sys.exit()
    if Overwrite:
        try:
            with open("NightcoreBot.cfg", "w", encoding="utf-8") as File:
                File.write(DefaultConfigFile)
        except IOError:
            Log("IOError: unable to create configuration file.", 4)
            sys.exit()

def Download(Type, Query):
    """
    Download a youtube video from a URL or from the first video returned for the specified query.
    Type must be boolean False or True, URL or search query. Query is a string, the URL or search query itself.
    """
    return None, None # TODO: Return audio and title.

def Exit():
    """
    Graceful halt.
    """
    Log("NightcoreBot stopped.", 2)

def Log(Message=None, LogLevel=1):
    """
    Logs a specific message according to its LogLevel.
    Logged messages are printed in the console, and are saved to the file as defined in the configuration file "Pathfinding.cfg".
    LogLevels are:
    0 / "DEBUG"; 1 / "INFO"; 2 / "WARNING"; 3 / "ERROR"; 4 / "CRITICAL".
    If no LogLevel is specified, 1 / "INFO" will be used.
    """
    if Message is None:
        raise ValueError("Message has no value.")
    Time = time.strftime("%Y-%m-%d %H:%M:%S")
    Date = time.strftime("%Y-%m-%d")
    LogLevel = str(LogLevel).lower()
    if LogLevel in ("0", "debug"):
        Message = "DEBUG:    {0}".format(Message)
    elif LogLevel in ("1", "info"):
        Message = "INFO:     {0}".format(Message)
    elif LogLevel in ("2", "warning"):
        Message = "WARNING:  {0}".format(Message)
    elif LogLevel in ("3", "error"):
        Message = "ERROR:    {0}".format(Message)
    elif LogLevel in ("4", "critical"):
        Message = "CRITICAL: {0}".format(Message)
    else:
        raise ValueError("Improper value passed for log level.")
    Message = "{0} > {1}".format(Time, Message)
    print(str(Message))
    try:
        with open("{0}.log".format(Date), "a", encoding="utf8") as File:
            File.write(Message + "\n")
    except IOError:
        print("IOError: unable to write to log file.", 3)

def MakeVideo(SourceType, Source):
    """
    Combine the input audio with the BackgroundSource image defined in the configuration, and returns the source of the output video.
    """

    if SourceType == "Y":
        Audio, Title = Download(False, Source)
        FileName = "NightcoreBot Mix № {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))
        raise Exception("WIP") # TODO: Finish this.
    if SourceType == "Q":
        Audio, Title = Download(False, Source)
        FileName = Source
        raise Exception("WIP") # TODO: Finish this too.
    if SourceType == "F":
        FileName, FileExtension = os.path.splitext(Source)
        try:
            Audio = pydub.AudioSegment.from_file(Source, format="mp3")
        except Exception as E:
            Log("Unable to decode audio file:\n{0}".format(E), 3)
    NewAudio = ProcessAudio(Audio)
    NewAudio.export("temp.mp3", format="mp3") # Create temporary audio file for ffmpy to work with.
    try:
        with open("NightcoreBot.cfg", "r", encoding="utf-8") as File: # Load various settings from config
            Config = json.load(File)
            BackgroundImageSource = Config["BackgroundSource"]
            VideoWidth = Config["VideoDimensions"]["Width"]
            VideoHeight = Config["VideoDimensions"]["Height"]
    except IOError:
        Log("IOError: unable to read configuration file.", 3)
    except Exception as E:
        Log("Unable to parse contents of configuration file:\n{0}".format(E))
    if os.path.isfile(BackgroundImageSource):
        BackgroundImage = BackgroundImageSource
    else:
        BackgroundImage = "{0}/{1}".format(BackgroundImageSource, random.choice(os.listdir(BackgroundImageSource)))
    FF = ffmpy.FFmpeg(inputs={"{0}".format(BackgroundImage): ["-r", "1", "-loop", "1"], "temp.mp3": None}, outputs={"{0}.mp4".format(FileName): ["-acodec", "copy", "-r", "1", "-shortest", "-vf", "scale={0}:{1}".format(VideoWidth, VideoHeight)]})
    try:
        FF.run()
    except Exception as E:
        Log("Unable to encode video:\n{0}".format(E), 3)
        return None
    os.remove("temp.mp3") # Delete temporary audio file.
    return "{0}.mp4".format(FileName)

def ProcessAudio(Audio):
    """
    Pitch-shift and speed up ("nightcoreify") the input audio; returns new audio.
    """
    try:
        with open("NightcoreBot.cfg", "r", encoding="utf-8") as File:
            Config = json.load(File)
        Lower = Config["SpeedupPercentage"]["LowerBound"]
        Upper = Config["SpeedupPercentage"]["UpperBound"]
    except Exception as E:
        Log("Unable to parse contents of configuration file:\n{0}".format(E), 3)
        sys.exit()
    if Lower > Upper:
        Log("LowerBound in SpeedupPercentage is greater than UpperBound. Check configuration file.", 4)
        sys.exit()
    ShiftPercentage = 1 + 0.01 * random.randint(Lower, Upper)
    try:
        NewAudio = Audio._spawn(Audio.raw_data, overrides={"frame_rate": int(Audio.frame_rate * ShiftPercentage)})
        NewAudio = NewAudio.set_frame_rate(Audio.frame_rate)
        return NewAudio
    except Exception as E:
        Log("Error processing audio:\n{0}".format(E), 3)

def Save(Video):
    """
    Save the input video locally.
    """
    pass

def Upload(Video):
    """
    Upload the input video to Youtube and returns the URL. Returns False if video failed to upload.
    """
    return None

#
# Mainline code
#

Parser = argparse.ArgumentParser(description="NightcoreBot: Automatically create Nightcore, and (optionally) upload it to Youtube.", epilog="NightcoreBot version: {0}. Visit http://pkre.co/Projects/NightcoreBot/ for more information.".format(NightcoreBotVersion))
SourceTypeGroup = Parser.add_mutually_exclusive_group(required=True)
SourceTypeGroup.add_argument("-y", dest="SourceType", action="store_const", const="Y", help="specifies source type \"Youtube URL\"")
SourceTypeGroup.add_argument("-q", dest="SourceType", action="store_const", const="Q", help="specifies source type \"Youtube query\"")
SourceTypeGroup.add_argument("-f", dest="SourceType", action="store_const", const="F", help="specifies source type \"local file\" (must be either a single file or a directory of files)")
Parser.add_argument("-s", "--save", dest="Save", action="store_true", help="whether to save the mixes locally")
Parser.add_argument("-u", "--upload", dest="Upload", action="store_true", help="whether to upload the mixes to Youtube")
Parser.add_argument("Source", nargs="+", type=str, help="the source of the audio, or the location of the file containing a list of songs to download and process (if using a file, seperate song entries with a newline)")
Arguments = Parser.parse_args(sys.argv[1:])

Arguments.Source = " ".join(Arguments.Source)

Actions = 0
if Arguments.Save and not Arguments.Upload:
    Actions = 1
elif not Arguments.Save and Arguments.Upload:
    Actions = 2
elif Arguments.Save and Arguments.Upload:
    Actions = 3
else:
    Parser.error("This program won't do anything if you don't choose an option for what to do with the nightcore remix... Use either \"-s\" to save locally, \"-u\" to upload to Youtube, or both.")
    sys.exit()

atexit.register(Exit)

Log("NightcoreBot started.")

CheckCoreFiles()

SourceList = []

StartTime = time.time()

if Arguments.SourceType == "Y": # TODO: COMPLETE THIS
    Log("Videos can not currently be downloaded from Youtube. Sorry!", 2)

if Arguments.SourceType == "Q": # TODO: COMPLETE THIS
    Log("Videos can not currently be downloaded from Youtube. Sorry!", 2)

if Arguments.SourceType == "F":
    if os.path.isfile(Arguments.Source):
        Log("Mixing local file \"{0}\"...".format(Arguments.Source))
        SourceList.append(Arguments.Source)
    elif os.path.isdir(Arguments.Source):
        SourceList = [Arguments.Source + "/" + File for File in os.listdir(Arguments.Source) if os.path.isfile(os.path.join(Arguments.Source, File))]
        if not SourceList:
            Log("No files exist within the specified directory.", 3)
            sys.exit()
        Log("Mixing {0} local files contained in directory \"{1}\"...".format(len(SourceList), Arguments.Source))
    else:
        Log("The specified file or directory can not be located.", 3)
        sys.exit()

VideosMixed = 0
VideosUploaded = 0

if not SourceList:
    Log("No sources were found.", 3)
    sys.exit()

for Source in SourceList:
    try:
        Video = MakeVideo(Arguments.SourceType, Source)
        VideosMixed += 1
        Log("√ \"{0}\"".format(Source))
        if Actions == 1 or Actions == 3:
            Save(Video)
        if Actions == 2 or Actions == 3:
            URL = Upload(Video)
            if URL:
                VideosUploaded += 1
                Log("^ \"{0}\"".format(URL))
            else:
                Log("* \"{0}\"".format(Source), 3)
    except Exception as E:
        Log("X {0}:\n{1}".format(Source, E), 2)

RunTime = round(time.time() - StartTime, 2)
UploadMessage = ""
if VideosUploaded > 0:
    UploadMessage = "Uploaded {0}/{1} videos.".format(VideosUploaded, len(SourceList))
Log("Done in {0} seconds. Successfully mixed {1}/{2} requests. {3}".format(RunTime, VideosMixed, len(SourceList), UploadMessage))
