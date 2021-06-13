# Song Publisher Search Tool

This is a prototype Python script which searches the [ASCAP Repertory](https://www.ascap.com/repertory#/) API to get a list of publishers.

## Motivation

I wrote this script in a few hours to see if it would be possible to have some sort of tool for content creators, which searches the publishers of the music they want to use in videos/on stream.

## Installation

Before running this tool, it is important to have **Python** installed on your device. This can be done through any method of your choice. Personally I prefer to use [Anaconda](https://www.anaconda.com/) (or maybe [Miniconda](https://docs.conda.io/en/latest/miniconda.html)) when working on Windows, and the standard apt command-line package tool when working on Ubuntu.

The tool uses a few packages, most of them already included in the [Python 3 Standard Library](https://docs.python.org/3/library/). The packages that need to be installed are **pandas** and **requests**, with the following commands.

```
pip install requests
pip install pandas
```

## Step-by-step usage

### Step 1 - Get the CSV file for the playlist

1. Go to the [TuneMyMusic](https://www.tunemymusic.com/) website, and click on the **Let's Start** button.
2. Choose the the source where your music is coming from, for this example I chose **Spotify**.
3. On your Spotify playlist click the three dots and click **Share > Copy link to playlist**.
4. Paste the link into the text box and click the **Load playlist** button.
5. Once the playlist is loaded click the **Next: Select Destination** button.
6. To select the destination, scroll down and click **Export to file**, this will give you an option to select format, it is important to choose **CSV**, and then click **Select**.
7. Once this has been done, a summary page will be shown, with the chosen playlist and the text **Spotify >> CSV** below the summary heading. On this page, click the **Start Moving My Music >>** button.
8. A download will start and the file **My Spotify Playlist.csv** should be saved on your device.

### Step 2 - Run the script

This tool is run via the command-line and includes an option to choose how to search for the songs and publishers.

```
usage: publisher_check.py [-h] -in INPUT_FILE -out OUTPUT_FILE
                          [-so {song-performer+song-only,song-performer}]

Run the ASCAP search script.

optional arguments:
  -h, --help            show this help message and exit
  -in INPUT_FILE, --input_file INPUT_FILE
                        The path of the input CSV playlist file.
  -out OUTPUT_FILE, --output_file OUTPUT_FILE
                        The path of the output CSV publishers file.
  -so {song-performer+song-only,song-performer}, --serarch_options {song-performer+song-only,song-performer}
                        The type of search that is carried out (song-
                        performer-song-only - if the song-performer search
                        doesn't yield results, the song-only search is carried
                        out (can yield false positives); song-performer - only
                        searches song-performer combinations (more accurate
                        but can miss some results)) (default = ['song-
                        performer+song-only']).
```

#### Option 1 - Search the song name with the performer first, then search only the song name

For this option, the script first runs a query with song title and performer. This is the best way to make sure that the right song is found, but it can have some issues with certain characters in the song name (so far mainly the / character was found to be problematic).

If this search does not find any results, another search is carried out with only the song title. This tends to give a lot of results, so at the moment if more than one result is found, the script ignores the output. **The song name only search can sometimes lead to false positives, so at the moment it might be best to not use it.**

```
python publisher_check.py -in Playlist.csv -out PlaylistPublishers.csv -so song-performer+song-only
```

#### Option 2 - Search the song name with the performer only

This option is very similar to the previous, but this only queries the song title and the performer. As mentioned, this tends to give fewer results but is somewhat more reliable.

```
python publisher_check.py -in Playlist.csv -out PlaylistPublishers.csv -so song-performer
```

### Step 3 - Review the results

After the script has run, make sure to open the output CSV file and go through the publishers that have been found. At this moment, it is important to **manually go through the publishers and double check that these match with the ASCAP results** (or any other repertory), I know this is a little counterintuitive, but as stated, this is only a prototype.

## Disclaimer

It has been stated clearly that the script is a basic prototype and is not always accurate, thus, you should take its results with a level of discretion.

If you would fully like to know the rights of a certain song and have not obtained results from this script, I advise you to manually check through the [ASCAP](https://www.ascap.com/repertory#/), [BMI](https://repertoire.bmi.com/) and [SESAC](https://www.sesac.com/repertory/search) repertories, and see if any results come up on there. Keeping this in mind, these sources might still have issues with finding the song you are looking, so there is always a level of risk involved.

This project is not affiliated with any of the aforementioned repertories, and only makes use of available API links to gather information without having to type it manually.

## Possible ideas for Improvements

At this moment, I cannot really afford to spend much time on this project, so I am leaving a list of ideas for anyone who would like to make a fork/pull-request and improve on this project.

- Adding a Graphical User Interface (GUI) to improve accessability.
- Transforming the script into a browser-based application (probably requires migration from Python to JavaScript).
- Improving the way the songs are searched, this might include:
  - searching song name only then trying to match the performer;
  - searching for the performer only then trying to match the song (should require less processing).
- Increasing the number of repertories that are searched. This might be difficult if the APIs are not easily available, but this should make the results more accurate.
- Adding some sort of multiprocessing to query multiple songs at once and speed-up the script.
- Most of these repertoires have their data publicly available for download It might be interesting to experiment with searching through a repertory file instead of sending requests over the internet. This method would require the repertory to be re-downloaded regularly, to keep up-to-date with any newly added songs.
- Adding a more fluid way to get songs from a playlist by only asking the user to input their Spotify (or any other platform) credentials, and choose the playlist from there. This might require quite a bit of time to work out how to information from such apps and is probably a very late stage addition.
