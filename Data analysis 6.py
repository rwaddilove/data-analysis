# Data analysis
# By Roland Waddilove
# This is a Python learning exercise - I just wanted to practise analysing data.
# What data? I am using data from the UK National Lottery. Go to:
# https://www.national-lottery.co.uk/results/lotto/draw-history-uc
# and download the CSV file.
# 
# UK Lotto is pick 6 from 59. The result include a bonus number, so 6 numbers plus 1 extra.
# If your lottery uses different numbers, you will need to edit the code.

import os
import csv
import random


def select_file(filetype) -> str:
    """ List files of type filetype like '.csv' in current folder. Use '*' for all."""
    print(f"\nFiles of type '{filetype}' in this folder:")
    # add files to list and display
    files = []
    i = 0
    for item in os.listdir():
        if not os.path.isfile(item): continue
        if item.startswith('.'): continue
        if filetype == '*' or item.endswith(filetype):
            files.append(item)
            print(i, item)
            i += 1
    print()
    # select file to use. Enter to exit with no file selected
    i = -1
    inp = input("Enter file num: ").strip()
    if inp.isdigit(): i = int(inp)
    return '' if i < 0 or i >= len(files) else files[i]


def select_folder() -> str:
    """Allow user to browse the disk and select a folder. Most system folders are hidden."""
    print("\n==== Select folder to use ====")
    os.chdir(os.path.expanduser('~'))       # user's home folder
#    if os.path.isdir('Downloads'): os.chdir('Downloads')
    print("Current folder: ", os.getcwd())
    inp = input("Use this (Y)es (N)o? ").upper()
    if inp == 'Y': return os.getcwd()

    # select folder to store task data
    os.chdir(os.path.expanduser('~'))       # user's home folder
    while inp != 'U':
        print()
        dirs = []
        i = 0
        for item in os.listdir():
            if os.path.isdir(item) and not item.startswith('.'):
                dirs.append(item)
                print(f"{i} {item} ".ljust(30))
                i += 1
        print("\nCurrent Folder: ", os.getcwd())
        inp = input("(U)se this, (B)ack, or folder num: ").upper()
        if inp.isdigit():
            i = int(inp)
            if i < len(dirs): os.chdir(dirs[i])
        if inp == 'B' and os.getcwd() != os.path.expanduser('~'):
            os.chdir('..')
    return os.getcwd()


def read_settings(settings) -> None:                  # 0=settings-filename, 1=data-filename, 3=path
    os.chdir(os.path.expanduser('~'))       # go to home folder
    if not os.path.isfile(settings[0]):          # does settings file exist? No? Create it
        settings[1] = select_folder()                 # get path to data folder
        settings[2] = select_file('.csv')    # get data filename
        write_settings(settings)             # save settings for next time
    # read settings file
    with open(settings[0], 'r') as f:       # settings[0] is ini filename
        settings.clear()
        for line in f.readlines():
            settings.append(line.strip())


def write_settings(settings) -> None:               # don't really need a csv file
    os.chdir(os.path.expanduser('~'))     # save to home folder
    with open(settings[0], 'w') as f:
        f.write(settings[0] + '\n' + settings[1] + '\n' + settings[2])


def read_data(data, filepath, filename) -> None:
    data.clear()
    os.chdir(filepath)                           # change to our folder
    if not os.path.isfile(filename): return      # does data file exist?
    with open(filename, 'r') as f:          # read data
        csvreader = csv.reader(f)
        for line in csvreader:                         # read data (1st line = field names)
            data.append(line)          # avoid blank lines


def process_data():
    # data[0] = DrawDate,Ball 1,Ball 2,Ball 3,Ball 4,Ball 5,Ball 6,Bonus Ball,Ball Set,Machine,DrawNumber
    # data[1] = 12-Jun-2024,59,40,13,42,41,51,5,3,Arthur,2971
    data[0] = ['Date       ', 'Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5', 'Ball6', 'Bonus']
    for i in range(1, len(data)):
        for j in range(1, 8):
            data[i][j] = int(data[i][j])    # turn strings into numbers


def show_raw_data(data) -> None:
    print("============ Raw Lottery Data ============")
    if len(data) == 0: return
    print("Date         Ball1 Ball2 Ball3 Ball4 Ball5 Ball6 Bonus")
    for i in range(1, len(data)):
        print(f"{data[i][0]}", end='')
        print(f"{data[i][1]}".rjust(5), end='')
        print(f"{data[i][2]}".rjust(6), end='')
        print(f"{data[i][3]}".rjust(6), end='')
        print(f"{data[i][4]}".rjust(6), end='')
        print(f"{data[i][5]}".rjust(6), end='')
        print(f"{data[i][6]}".rjust(6), end='')
        print(f"{data[i][7]}".rjust(6))


def common_numbers(data, bonus):
    mydata = [[i, 0] for i in range(60)]     # zero list
    for r in range(1, len(data)):
        for c in range(1, bonus):
            mydata[data[r][c]][1] += 1       # count how many times number appears
    # print chart
    # for n in range(1, 60):
    #     print(f"{n}".rjust(2), ":", "*" * mydata[n][1])
    mydata.pop(0)        # get rid of first item = ([0,0],...
    print("Numbers ordered with LEAST common first:")
    sort_data(mydata)
    for i in range(0, 15):
        print(f"{mydata[i][0]} ", end='')
    print("\n\nNumbers ordered with MOST common first:")
    mydata.reverse()
    for i in range(0, 15):
        print(f"{mydata[i][0]} ", end='')
    print("\n")


def overdue_numbers(data, bonus):
    """Sort results with longest time since last appearance in a draw."""
    mydata = [[i, 0] for i in range(60)]     # zero list
    for row in range(1, len(data)):
        for col in range(1, bonus):
            ball = data[row][col]  # ball num
            if mydata[ball][1] == 0: mydata[ball][1] = row
    print("Overdue numbers, MOST overdue first:")
    sort_data(mydata)
    mydata.reverse()
    for i in range(0, 15):
        print(f"{mydata[i][0]} ", end='')
    print("\n")


def odd_even_numbers(data, bonus):
    """Count number of odd/even numbers in draw results."""
    odd, even = 0, 0
    for row in range(1, len(data)):
        for col in range(1, bonus):
            if data[row][col] % 2:
                odd += 1
            else:
                even += 1
    print(f"There have been {odd} odd numbers and {even} even.")
    if odd - even > 5: print("More even numbers are expected")
    if even - odd > 5: print("More even numbers are expected")
    print()


def average_numbers(data):
    """What are the averages for number 1, 2, 3... in a draw?"""
    # data[1..6] = 12-Jun-2024,59,40,13,42,41,51,5,3,Arthur,2971
    for r in range(1, len(data)):    # sort lotto result in each row
        row = data[r][1:7]
        row.sort()
        for c in range(1, 7):
            data[r][c] = row[c-1]
    # calculate average for each ball
    ball = [0, 0, 0, 0, 0, 0, 0]
    for row in range(1, len(data)):
        for c in range(1, 7):
            ball[c] += data[row][c]
    print("Average numbers for each ball in Lotto:")
    for c in range(1, 7):
        print(f"{ball[c] // (len(data)-1)} ", end='')
    print("\n")


def sort_data(a) -> None:     # sort a list of lists by column 1
    for j in range(0, len(a)):
        for i in range(len(a)-1, j, -1):
            if a[i][1] < a[i-1][1]:
                a[i-1], a[i] = a[i], a[i-1]


def analyse_data(data):
    print("======== Analyse Lottery Data ========")
    bonus = 8       # 1 more because range() doesn't reach last number
    if input("Include bonus ball in analysis? Y/N: ").upper() == 'Y': bonus = 7
    print()
    common_numbers(data, bonus)
    overdue_numbers(data, bonus)
    odd_even_numbers(data, bonus)
    average_numbers(data)


def pick_all_nums():
    """Pick 10 lines of lottery numbers."""
    print("========== Pick Lottery Entries ==========")
    nums = [i for i in range(1, 61)]     # lotto nums
    for i in range(50):                            # mix them up 50 times
        n1 = random.randint(1, 59)
        n2 = random.randint(1, 59)
        nums[n1], nums[n2] = nums[n2], nums[n1]
    nums[59] = nums[random.randint(0, 50)]             # 10 lines, 6 nums, 1-59, one repeated
    print(f"These Lottery entries use all 59 numbers once.\nOnly the number {nums[59]} is repeated.\n")
    # print lotto lines
    for r in range(10):
        print(f"Line {(r+1):02d}: ", end='')
        for c in range(6):
            print(f" {(nums[r*6 + c]):02d}", end='')
        print()
    print()


# ============= M A I N ===============
# os.system('cls') if os.name == 'nt' else os.system('clear')

data = []
settings = ['Lottery.ini', '', '']     # 0=settings file, path, datafile
read_settings(settings)     # read settings - get folder with data
if settings[2] == '': quit()        # no file selected
read_data(data, settings[1], settings[2])
process_data()
print("\n========== Lottery Helper and Analysis ==========\n")
inp = ''
while inp != 'Q':
    print("What would you like to do?")
    print("1. Show original data")
    print("2. Analyse Lottery data")
    print("3. Pick Lottery numbers")
    inp = input("\nAction or (q)uit: ").upper().strip()
    print()
    if inp == '1': show_raw_data(data)
    if inp == '2': analyse_data(data)
    if inp == '3': pick_all_nums()
