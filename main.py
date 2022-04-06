# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("print it out loud")


def hackerlandRadioTransmitters(x, k):
    x = sorted(x)
    dup_tracker = 0
    for i in range(1, len(x)):
        if x[i] != x[i-1]:
            dup_tracker += 1
            x[dup_tracker] = x[i]
    x = x[:dup_tracker+1]
    max_loc = x[-1]
    location_marker = [0]*(max_loc+1)
    accumulation = [0]*(max_loc+1)
    count_dups = 0
    for i in range(0, len(x)):
        if i > 0 and x[i] == x[i-1]:
            count_dups += 1
        location_marker[x[i]] = 1
    accumulation[0] = 0
    for i in range(1, len(location_marker)):
        accumulation[i] = location_marker[i] + accumulation[i - 1]
    jump = 2*k + 1
    transmitter_counter = 0
    i = 0
    while i < len(location_marker):
        if location_marker[i] != 0:
            if i + k < len(location_marker) and (accumulation[i + k] - accumulation[i]) != 0:
                transmitter_counter += 1
                steps = x[accumulation[i + k] - 1]
                i = steps + k + 1
            else:
                transmitter_counter += 1
                i += (k + 1)
        else:
            i += 1
    return transmitter_counter

import sys
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = [7, 2, 4, 6, 5, 9, 12, 11]
    k = 2
    x = sorted(x)
    print(hackerlandRadioTransmitters(x, k))
    n, k = 7, 2
    x = [9, 5, 4, 6, 15, 12]
    print(hackerlandRadioTransmitters(x, k))
    import codecs
    with codecs.open("input.txt", "r+", encoding="utf-8") as data_reader:
        n, k = data_reader.readline().rstrip().split()
        n = int(n)
        k = int(k)
        x = list(map(int, data_reader.readline().rstrip().split()))
        print(hackerlandRadioTransmitters(x, k))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
