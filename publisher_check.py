#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Import argparse and get the command line arguments
import argparse

parser = argparse.ArgumentParser(description='Run the ASCAP search script.')

parser.add_argument('-in', '--input_file', type=str, nargs=1, required=True,
                    help="""The path of the input CSV playlist file.""")
parser.add_argument('-out', '--output_file', type=str, nargs=1, required=True,
                    help="""The path of the output CSV publishers file.""")
parser.add_argument('-so', '--search_options', type=str, nargs=1, default=['song-performer+song-only'],
                    choices=['song-performer+song-only', 'song-performer'],
                    help="""The type of search that is carried out
                            (song-performer-song-only - if the song-performer
                            search doesn't yield results, the song-only search is carried out (can yield false positives);
                            song-performer - only searches song-performer combinations
                            (more accurate but can miss some results)) (default = %(default)s).""")


args = parser.parse_args()

playlist_name = args.input_file[0]
save_name = args.output_file[0]
search_options = args.search_options[0]

# Show the arguments to make sure they are correct
print('Input file:', playlist_name)
print('Output file:', save_name)
print('Chosen options:', search_options)

import requests
import pandas as pd
import os

# Function which runs a request on a give url and get a string of publishers if any have been found
def get_publishers(api_url, search_type):
    r = requests.get(api_url).json()

    # Check if there is a 404 error
    if r['error'] is not None and r['error'] == 'Not Found':
        return None

    # Check if any results have been obtained
    if r['result'] is not None:
        # Depending on the search type determine how to handle the results
        if search_type == 's' and len(r['result']) > 1:
            print('More than 1 result found... skipping.')
            return None
        else:
            interested_parties = r['result'][0]['interestedParties']

            publishers_string = ''

            # Go through each item in the 'interestedParties' list and save any results
            # that have the 'roleCde' set to 'P', which refers to that party being a publisher
            for j in range(len(interested_parties)):
                party = interested_parties[j]

                if party['roleCde'] == 'P':
                    publisher = party['fullName']
                    print('Publisher:', publisher)

                    # Append the publisher to the string
                    if publishers_string == '':
                        publishers_string = publisher
                    else:
                        publishers_string = publishers_string + ' & ' + publisher

            return '"' + publishers_string + '"'
    else:
        return None

# Read the playlist CSV file from the given input argument
df = pd.read_csv(os.path.join(playlist_name))

# print(df)

titles = []
performers = []

# Go through the rows of the file and get the song name and the performer
for index, row in df.iterrows():
    titles.append(row[0])
    performers.append(row[1])

# Open a new CSV file to store the results in
with open(os.path.join(save_name), 'w') as file:
    file.write('Title,Artist,Publishers\n')

    # Go through each song and run the requested queries
    for i in range(len(titles)):
        title = titles[i]
        performer = performers[i]

        # API link that contains both song name and performer
        api_url_song_with_performer = 'https://ace-api.ascap.com/api/wservice/MobileWeb/service/ace/api/v3.0/search/title/' \
                                       + title + '?limit=100&page=1&universe=IncludeATT&socUniverse=SVW&searchType2=perfName&searchValue2=' + performer

        # API link that contains only song name
        api_url_song_only = 'https://ace-api.ascap.com/api/wservice/MobileWeb/service/ace/api/v3.0/works/details?limit=100&page=1&universe=IncludeATT&socUniverse=SVW&workTitle=' + title

        print('Song title:', title)
        print('Performer:', performer)

        write_values_list = ['"' + title + '"', '"' + performer + '"']

        print('Song with performer search...')

        # Run a query with the song + performer link
        publishers_string = get_publishers(api_url_song_with_performer, 'sp')

        # Check if any results have been found
        if publishers_string is not None:
            write_values_list.append(publishers_string)

            if publishers_string == '""':
                print('Song found but no publishers were listed...')
                write_values_list.append('Song found but publisher list was empty')
        else:
            # If the list was empty, also check the song only link
            if search_options == 'song-performer+song-only':
                print('Song only search...')
                publishers_string = get_publishers(api_url_song_only, 's')

            if publishers_string is not None:
                write_values_list.append(publishers_string)

                if publishers_string == '""':
                    print('Song found but no publishers were listed...')
                    write_values_list.append('Song found but publisher list was empty')
            else:
                print('Song not found on ASCAP...')
                write_values_list.append('Song not found')

        print('-------------------')

        # Append the values to the string of the CSV file and write it
        write_string = ','.join(write_values_list)
        file.write(write_string + '\n')
