import math
import typing
import sys


def main():
    f = sys.argv[1]
    reservations = list()
    with open(f, "r") as file:
        t = True
        for line in file:
            if t:
                t = False
                continue
            line = line.strip().replace('"', "").split(",")
            if line[8] != "Indoor":
                continue
            elif line[1] != "":
                continue
            elif line[3] != "":
                continue
            else:
                if line[16] == "":
                    continue
                if int(line[16]) < 24:
                    reservations.append(line)
    printKey()
    for item in reservations:
        prettyprint(item)


def printKey():
    items = [
        "Deleted Date",
        "Original Reservation Date",
        "Play Date",
        "Start Time",
        "End Time",
        "Facility Name",
        "Court",
        "Tags",
        "Booking User",
        "Hours Deleted in Advance of Play Time",
    ]
    for item in items:
        print(f"{item}\t", end="") if len(item) % 8 > 2 else print(
            f"{item}      \t", end=""
        )
    print()


def prettyprint(res):
    for i in range(len(res)):
        if res[i] == "":
            continue
        if i != len(res) - 1:
            try:
                int(res[i])
                continue
            except Exception as e:
                # print(e)
                pass

        print(f"{res[i]},       \t", end="") if len(res[i]) % 8 > 2 else print(
            f"{res[i]},\t", end=""
        )

    print("")


# requested output:
# filter out anything cancelled 24 hours before or more
# for reservations cancelled  with less than 24 hours:
# show when made and when cancelled
# extract hours between creation and cancellation
# adjustable thresholds for everything


if __name__ == "__main__":
    main()
