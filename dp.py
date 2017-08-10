import soundcloud
import csv
import cPickle as pickle
import sys
import os
from songOBJ import songObject

reload(sys)
sys.setdefaultencoding('utf-8')

client = soundcloud.Client(client_id="rvUzdXNHlC53yQD3OcXOGxUUs3kMniRO")
my_likes = client.get('/resolve', url='http://soundcloud.com/jacob-elias-5/likes')
# Data of music drawn in
data = {}
# Create list of newSong and oldSong
newSongList = []
oldSongList = []


def determine_new_songs( comparison_list ):

    print "Finding new songs..."
    # Create dictionary of Links
    # The song ID maps to a string of all of the info
    for item in my_likes:
        try:
            track_info = client.get('/tracks/{}'.format(item.id))
            # favorites = track_info.favoritings_count
            # plays = track_info.playback_count
            data[item.id] = [track_info.user['username'],
                             track_info.title,
                             track_info.favoritings_count,
                             track_info.playback_count]

            song = songObject(track_info.title, item.id, track_info.user['username'])  # Create a song object

            # Loop through to see if it already contains the new song before adding it
            found_in_oldSongList = "false"
            for x in comparison_list:
                if x.id == song.id:
                    found_in_oldSongList = "true"
                    break

            # If the song was not found, add it to new songList
            if found_in_oldSongList == "false":
                newSongList.append(song)

        except AttributeError:
            pass

    #  Compare
    # with open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv') as csvfile:
    #
    #     # readCSV is a list that can be accessed readCSV[row][col]
    #     read_csv = list(csv.reader(csvfile, delimiter=','))
    #
    #     # iterate through all of thedef determineNewSongs ():
    #     for obj in data.keys():
    #         # bool to determine if the songID is found, resets for each new obj in dict
    #         _found_in_spreadsheet = "false"
    #
    #         # iterate throught the CSV
    #         for row in read_csv:
    #
    #             # avoid Value error if parsing a string
    #             try:
    #                 int(row[0])
    #             except ValueError:
    #                 continue
    #
    #             if int(row[0]) == obj:
    #                 oldSongList.append(obj)
    #                 _found_in_spreadsheet = "True"
    #                 break
    #
    #         # If the sound if not found in spread sheet at it to new song list
    #         if _found_in_spreadsheet == "false":
    #             newSongList.append(obj)


def write_new_songs():
    print' '
    print "Writing new songs to spreadsheet..."
    print ' '
    with open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv', 'a+') as csvfile:

        #  readCSV is a list that can be accessed readCSV[row][col]
        # read_csv = list(csv.reader(csvfile, delimiter=','))
        # csvWriter is for writing new info to the list
        csv_writer = csv.writer(csvfile)

    # c.writerow(['Song ID', 'Artist', 'Title', 'Favorites', 'Plays','Plays/Likes'])
    # print("entering for loop")
        for key, value in data.items():
            if newSongList.__contains__(key):
                # TO Write
                print "Writing song: ", key, value
                csv_writer.writerow([key] + value)


def read_pickle_file():
    f = open("save.p", 'r')  # Pickle file to load a save data
    if (os.stat("save.p")).st_size != 0:  # Check to make sure the file is not empty
        while 1:
            try:
                oldSongList.extend(pickle.load(f))
            except EOFError:
                break
    f.close()


def write_pickle_file(full_list):

    if newSongList.__len__() == 0:
        print 'No new songs to add'

    for x in newSongList:
        print 'Adding ', x.title, ' to pickle file'

    f = open("save.p", 'w')   # Save song_list data to a pickle file
    pickle.dump(full_list, f)
    f.close()


def main():

    final_song_list = []
    # Read in the stored songs
    read_pickle_file()
    # Determine the new likes from soundCloud, oldSongList is passed in as a comparison
    determine_new_songs(oldSongList)

    print ' '
    print "New Song List: ", newSongList
    print "Old Song List: ", oldSongList
    print ' '
    final_song_list = oldSongList + newSongList
    # Collect new information for all the songs
    for song in final_song_list:
        song.add_information()
    print " "
    write_pickle_file(final_song_list)

    # write the new songs to the spreadsheet
    # write_nw_songs()

if __name__ == '__main__':

    print("Starting...")

    main()

    print ' '
    print("Completed")



# THINGS FOR YOU TO DO
# 1) Figure out how to read in the old spreadsheet
# 2) Figure out how to pull in more than X number of likes at once, all of them
# 3) Figure out how to calculate the "movements" from (1) and the new data (along with it, how to add more columns, etc)
# 4) Get your own clientID and use that instead
