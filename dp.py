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


def menu():

    runMenu = "false"

    while runMenu == 'false':
        menu_option = ['c', 'd', 'r', 'q']
        print " "
        print '-------------------------------'
        print '[C]ompare two dates'
        print '[D]isplay stats from single day'
        print '[R]emove a song from saved list'
        print '[Q]uit   '
        print '-------------------------------'
        print ' '
        user_in = raw_input("What would you like to do ?   ")

        if user_in.lower() in menu_option:
            runMenu = 'true'
            return user_in


def determine_new_songs(comparison_list):
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


def write_songs(songlist, date):
    print' '
    print "Writing new songs to spreadsheet..."
    csvfile = open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv', 'w')

    #  readCSV is a list that can be accessed readCSV[row][col]
    # read_csv = list(csv.reader(csvfile, delimiter=','))
    # csvWriter is for writing new info to the list
    csv_writer = csv.writer(csvfile)
    title = "Displaying stats from" + date
    csv_writer.writerow([' ', ' ', title])
    csv_writer.writerow(['Song ID', 'Artist', 'Title', 'Favorites', 'Plays','Plays/Likes'])

    for song in songlist:
        csv_writer.writerow([song.id, song.artist, song.title, song.get_favorite_count(date), song.get_play_count(date)] )


def compare_songs(songlist, date1, date2):
        print' '
        print "Writing new songs to spreadsheet..."
        csvfile = open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv', 'w')

        #  readCSV is a list that can be accessed readCSV[row][col]
        # read_csv = list(csv.reader(csvfile, delimiter=','))
        # csvWriter is for writing new info to the list
        csv_writer = csv.writer(csvfile)
        #Format a string for the "title" for the spread sheet
        title = "Comparison between " + date1 + " and " + date2
        csv_writer.writerow([' ', ' ', title])
        csv_writer.writerow(['Song ID', 'Artist', 'Title', 'Favorites growth', 'Play growth', 'Plays/Likes'])

        for song in songlist:
            fav_growth = calculate_percent_growth( song.get_favorite_count(date1), song.get_favorite_count(date2))
            play_growth = calculate_percent_growth( song.get_play_count(date1), song.get_play_count(date2))

            csv_writer.writerow([song.id,
                                 song.artist,
                                 song.title,
                                 fav_growth + '%'
                                 , play_growth + '%'])


def calculate_percent_growth(past_number, future_number):
    diff = float(future_number) - float(past_number)
    percent = diff / past_number
    format_percent = format(percent, '.2f')
    return format_percent


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


def print_all_dates(listofsongs):

    dates = []
    # Loop to add all keys to a list without duplicates
    for song in listofsongs:
        for x in song.song_data.keys():
            if x not in dates:
                dates.append(x)
    print ' '
    print "Dates to choose from", dates

    return dates

def main():
    final_song_list = []
    # Read in the stored songs
    read_pickle_file()
    # Determine the new likes from soundCloud, oldSongList is passed in as a comparison
    determine_new_songs(oldSongList)

    final_song_list = oldSongList + newSongList
    # Collect new information for all the songs
    for song in final_song_list:
        song.add_information()
    print "Finding new songs..."
    write_pickle_file(final_song_list)

    user_choice = menu()

    if user_choice.lower().strip() == 'd':
        valid_date_list = print_all_dates(final_song_list)

        valid_date_1 = 'false'
        while valid_date_1 == 'false':
            date1 = raw_input("Enter a date to view:  DD-MM-YYYY ")

            if date1 in valid_date_list:
                valid_date_1 = 'true'
            else:
                print 'Date was not valid'

        # write the new songs to the spreadsheet
        write_songs(final_song_list, date1)

    if user_choice.lower().strip() == 'q':
        print 'Quiting...peace'

    if user_choice.lower().strip() == 'c':

        valid_date_list = print_all_dates(final_song_list)

        valid_date_1 = 'false'
        while valid_date_1 == 'false':
            date1 = raw_input("Enter first date:  DD-MM-YYYY ")
            if date1 in valid_date_list:
                valid_date_1 = 'true'
            else:
                print 'Date was not valid'

        valid_date_2 = 'false'
        while valid_date_2 == 'false':
                date2 = raw_input("Enter second date: DD-MM-YYYY ")
                if date2 in valid_date_list:
                    valid_date_2 = 'true'
                if date2 == date1:
                    print 'Date 1 and date 2 were the same. Please enter another second date'
                    valid_date_2 = 'false'
                elif valid_date_2 == 'false':
                    print 'Date 2 was not valid'

        compare_songs(final_song_list, date1, date2)


if __name__ == '__main__':

    print("Starting...")
    print "Updating Information... "

    main()

    print ' '
    print("Completed")
