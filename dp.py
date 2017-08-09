import soundcloud
import csv
import time
import sys
from songOBJ import SongOBJ

reload(sys)
sys.setdefaultencoding('utf-8')

client = soundcloud.Client(client_id="rvUzdXNHlC53yQD3OcXOGxUUs3kMniRO")
my_likes = client.get('/resolve', url='http://soundcloud.com/jacob-elias-5/likes')
# Data of music drawn in
data = {}
# Create list of newSong and oldSong
newSongList = []
oldSongList = []


def determine_new_songs():

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


        except AttributeError:
            pass

    ##Compare
    with open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv') as csvfile:

        # readCSV is a list that can be accessed readCSV[row][col]
        read_csv = list(csv.reader(csvfile, delimiter=','))

        # iterate through all of thedef determineNewSongs ():
        for obj in data.keys():
            # bool to determine if the songID is found, resets for each new obj in dict
            _found_in_spreadsheet = "false"

            # iterate throught the CSV
            for row in read_csv:

                # avoid Value error if parsing a string
                try:
                    int(row[0])
                except ValueError:
                    continue

                if int(row[0]) == obj:
                    oldSongList.append(obj)
                    _found_in_spreadsheet = "True"
                    break

            # If the sound if not found in spread sheet at it to new song list
            if _found_in_spreadsheet == "false":
                newSongList.append(obj)


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



def main():
    # determine new data from soundcloud that is not in spreadsheet
    determine_new_songs()

    print "New Song List: ", newSongList
    print "Old Song List: ", oldSongList

    # write the new songs to the spreadsheet
    write_new_songs()


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
