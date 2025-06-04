import csv
import time
import itertools
import hashlib
import os.path

# function to read hashes in from a file


def read_file(filename):
    # declare list 'file_hashes'
    file_hashes = []

    # check if file exists
    if os.path.isfile(filename):
        # open file
        file = open(filename)

        # create reader
        csv_reader = csv.reader(file)

        # declare list 'row'
        row = []

        for row in csv_reader:
            # check if hash is the correct length
            if len(row[0]) == 64:
                # add each hash from file into list 'file_hashes'
                file_hashes.append(row[0])

        # close file
        file.close()

    else:
        # print error message
        print("Error: File not found")

    # return list 'file_hashes'
    return file_hashes

# function to take in hashes


def hash_input():
    print("Enter a hash, or the name of a file containing a hash: ")
    print("(Please use one line per hash or filename, 'x' to finish)")

    # declare list 'hashes'
    hashes = []

    # check whether each new line is the end of the list
    new_input = input()
    while new_input.lower() != "x":

        # if input contains '.', treat input as filename
        if "." in new_input:
            # if last four chars of input are a csv file extension, read in hashes from file
            if new_input[-4:] == ".csv":
                hashes.extend(read_file(new_input))
            else:
                # print error message
                print("Error: Unrecognised file type (.csv files only)")
        else:
            # check if hash is the correct length
            if len(new_input) == 64:
                # add input to list of hashes
                hashes.append(new_input)
            else:
                print("Error: Hash should be 64 characters")

        # if not the end, add new line into 'hashes'
        new_input = input()

    # return list 'hashes'
    return hashes

# function to compare hash to a list of hashes from a file


def brute_force(hashed_passwd, max_chars):
    # store starting time
    tic = time.perf_counter()

    # declare string 'password' and boolean 'known'
    password = ""
    known = False

    # open file
    file = open("known_passwords.csv", "r+", newline="")

    # create reader
    csv_reader = csv.reader(file)

    # declare list 'row'
    row = []

    print("Comparing values to known passwords...")
    for row in csv_reader:
        # if a match is found
        if hashed_passwd == row[0]:
            # hash was found in file of known passwords
            known = True

            # store password and stop loop
            password = row[1]
            break

    # if password has not yet been found
    if password == "":
        print("No match found")
        print("Comparing values to generated hashes...")

        # declare list 'chars'
        chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z",
                 "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z",
                 " ", "!", chr(34), "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
                 "=", ">", "?", "@", "[", chr(92), "]", "^", "_", "`", "{", "|", "}", "~"]

        # declare integer 'length'
        length = 0

        # while password not found, increase length of combinations generated, up to maximum length specified
        while (length < max_chars) and (password == ""):
            length += 1

            # run through every potential combination of a specified length
            for current_iteration in itertools.product(chars, repeat=length):
                # convert list of characters into string
                string = "".join(map(str, current_iteration))

                # calculate sha256 hash of string
                encoded = string.encode()
                result = hashlib.sha256(encoded)

                # if a match is found, stop loop and store password
                if hashed_passwd == result.hexdigest():
                    password = string

                    # add password and hash to list of known passwords
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([result.hexdigest(), password])

                    break

    # store finishing time
    toc = time.perf_counter()

    # close file
    file.close()

    # return password and time taken to run the function
    return password, (toc - tic)

# starting function


def main():
    # declare string 'passwd_encrypted'
    passwd_encrypted = []

    # add user input to list of hashes
    passwd_encrypted.extend(hash_input())

    # get maximum number of characters from user
    print("Enter the maximum number of characters in the password (default is 5):")
    maximum = input()

    if maximum == "":
        maximum = 5

    # declare integers 'count', 'cracked' and 'total_time'
    count = 0
    cracked = 0
    total_time = 0

    # for each hash given by the user
    for x in passwd_encrypted:
        count += 1
        print("Hash {}: {}\n".format(count, x))

        # decrypt hash
        passwd_decrypted, time_taken = brute_force(x, maximum)

        # print the decrypted password
        if passwd_decrypted == "":
            print("No matches found")
        else:
            print("Password match found:")
            print(passwd_decrypted)

            # add 1 to number of successfully decrypted hashes
            cracked += 1

        # print time taken to decrypt current hash
        print("\nTime taken:")
        print("{}\n".format(time_taken))

        # add time taken to decrypt current hash to the total time taken
        total_time += time_taken

    # print the number of hashes decrypted out of those given
    if cracked == count:
        print("\nAll hashes cracked")
    else:
        print("\n{} out of {} hashes cracked".format(cracked, count))

    # print total time taken
    print("\nTotal time taken:")
    print("{}\n".format(total_time))


main()
