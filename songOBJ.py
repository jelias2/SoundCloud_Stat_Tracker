import datetime
import os
from datetime import timedelta
import soundcloud
import urllib2
import requests
import cPickle as pickle

song_list = []
client = soundcloud.Client(client_id="rvUzdXNHlC53yQD3OcXOGxUUs3kMniRO")
my_likes = client.get('/resolve', url='http://soundcloud.com/jacob-elias-5/likes')


class songObject:
    # Class to hold information about each song

    def __init__(self, title, song_id, artist):
        self.title = title
        self.id = song_id
        self.artist = artist
        # Format for dictionary:  [Date] : favorites count, play count "
        self.song_data = {}

    def add_information(self):

        # "Method to add soundcloud information from a specific date to a song"
        today = datetime.date.today()
        date = today.strftime('%m-%d-%Y')

        # Check if the date already exits in the dictionary, if not add
        if date in self.song_data:
            # print "Date ", date, " is already in ", self.title
            ' '  # Blank space to avoid python error
        else:
            print "Adding ", date, " to song ", self.title
            try:
                track_info = client.get('/tracks/{}'.format(self.id))
                # favorites = track_info.favoritings_count
                # plays = track_info.playback_count
                self.song_data[date] = [track_info.favoritings_count, track_info.playback_count]

            except (AttributeError, requests.exceptions.HTTPError):
                pass
                print "Could not add info to ", self.title, ": HTTP Request Error:"


    def print_dates(self):
            # Method to show all the dates in a song
            print "Song ", self.title, " contains info from ", self.song_data.keys()

    def get_play_count(self, date):
        #  Method to get the specific play count from a song
        info = self.song_data.get(date)

        return info[1]

    def get_favorite_count(self, date):
        # Method to get the favorites count"
        info = self.song_data.get(date)
        return info[0]


def main():

    stopper = 0

    for item in my_likes:
        if stopper is 3:
            break
        try:
            track_info = client.get('/tracks/{}'.format(item.id))
            username = track_info.user['username']
            song_id = item.id
            song_title = track_info.title

            song = songObject(song.title, song_id, username )

            song.add_information()

            song_list.append(song)
            # favorites = track_info.favoritings_count
            # plays = track_info.playback_count
            stopper += 1
        except AttributeError:
            pass

    today = datetime.date.today()

    # day = datetime.timedelta(days=1)
    # tomorrow = datetime.date.today()
    date = today.strftime('%d-%m-%Y')

    for song in song_list:
        print "Title: ", song.title
        print "Song ID: ", song.id
        print "Artist: ", song.artist
        print "Favorites: ", song.get_favorite_count(date)
        print "Plays: ", song.get_play_count(date)

if __name__ == '__main__':
    print ' '
    print("Starting...")
    print ' '
    print 'Loading pickle file lmaooo'

    f = open("save.p", 'r')   # Pickle file to load a save data

    if(os.stat("save.p")).st_size != 0:  # Check to make sure the file is not empty
        song_list = pickle.load(f)
    f.close()

    main()

    f = open("save.p", 'w')
    pickle.dump(song_list, f)  # Save song_list data to a pickle file
    f.close()

    print ' '
    print("Completed")
