import csv
import string

with open('/Users/JacobElias/Desktop/Projects/SoundProgram/data2.csv') as csvfile:

    readCSV = list(csv.reader(csvfile, delimiter=','))

    songNumber = raw_input("Enter Song ID")
    print("Song number: " + songNumber)
    song_Id = "false"
    songRowIndex = -1

    for counter, row in enumerate(readCSV):

        print(counter)

        if row[0] == songNumber:
            song_Id = "true"
            print("TRUE: In row: ", counter)
            songRowIndex = row


    if song_Id == "false":
        print("Song ID was not in row")

    else:

     print("Counter ", counter)
     print(readCSV[counter])
     lastIndex =  len((readCSV[counter]))
     print(readCSV[counter][lastIndex - 1])
     print (readCSV[0][4])





