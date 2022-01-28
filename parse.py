from __future__ import annotations  # make typehints vanish at runtime
import math, datetime, time, typing
import sys

from typing import *

# for python 3.10 and up


def main():
    f = sys.argv[1]
    reservations = list()
    with open(f, "r") as file:
        file.readline()
        for line in file:
            line = line.strip().replace('"', "").split(",")
            if (
                line[8] != "Indoor"
                or line[1] != ""
                or line[3] != ""
                or line[16] == ""
                or int(line[16]) > 24
            ):
                continue
            reservations.append(line)
    fmt_res = list()

    # TODO: fix the error in this code, it emits a "list of lists of lists"
    for res in reservations:
        resv = list()
        for item in res:
            if item == "":
                continue
            if item.isnumeric():
                if int(item) > 24:
                    continue
            resv.append(
                ", ".join(
                    item.replace("<i>", "")
                    .replace("</i>", "")
                    .replace("<hr>", ": ")
                    .replace("&#39;", "'")
                    .replace("#1I", "#1")
                    .replace("#2I", "#2")
                    .split("<br>")
                )
            )
        fmt_res.append(resv)

    reservations.clear()

    for line in fmt_res:
        rsv = list()
        rsv.append(line[1])
        rsv.append(line[0])
        rsv.append(" ".join([line[2], line[3]]))
        rsv.append(line[6])
        rsv.append(line[7])
        rsv.append(line[8])
        rsv.append(line[9])
        reservations.append(rsv)

    day = datetime.timedelta(seconds=86400)
    problem_rsvs = list()
    possible_problem_rsvs = list()

    for item in reservations:
        res_time = datetime.datetime.strptime(item[0], "%m/%d/%y %I:%M %p")
        play_time = datetime.datetime.strptime(item[2], "%m/%d/%y %I:%M %p")
        # print(f"{play_time=}\t{res_time=}\t{play_time-res_time=}")
        if play_time - res_time > day:
            problem_rsvs.append(item)
        else:
            possible_problem_rsvs.append(item)

    keyItems = [
        "Reservation Creation Time",
        "Deleted Time",
        "Play Start Time",
        "Court",
        "Players/Machines",
        "Booking User",
        "Hours Deleted Before Play Time",
    ]

    print("\nReservations created outside of a 24-hour play window:\n")
    jays_pretty_print(header=keyItems, data=problem_rsvs)
    print("\n\nReservations created inside a 24-hour play window:\n")
    jays_pretty_print(header=keyItems, data=possible_problem_rsvs)


def jays_pretty_print(
    *,
    header: list[str],
    data: list[list[str]],
    output: Callable[[str], Any] = print,
):

    assert isinstance(data, list)
    assert len(data), "no items in data"

    assert isinstance(
        data[0], list
    ), f"data[0] is not a list, it is a {type(data[0])}, data must be a list[list[str]]"
    assert len(data[0]), "no items in data's first item"

    assert isinstance(
        data[0][0], str
    ), f"data[0][0] is not a string, it is a {type(data[0][0])}, data must be a list[list[str]]"

    assert len(header) == len(
        data[0]
    ), f"header and data must have same length, header[{len(header)}] != data[{len(data[0])}]"

    # smoosh together all the data and header
    lines = [header] + data

    # make an array where each element is the length of the corresponding string in the lines variable
    lengths = tuple(tuple(map(len, line)) for line in lines)

    # find the max length of each column
    # start with no lengths in each
    widths: Iterable[int] = [0] * len(header)

    for lengths_line in lengths:
        widths = tuple(map(max, widths, lengths_line))

    # print(f"{widths=}")

    for index, line in enumerate(lines):
        assert all(
            isinstance(i, str) for i in line
        ), f"all elements in line must be strings, line index {index} has a not string element in it"

        output(" | ".join(item.ljust(width) for width, item in zip(widths, line)))


# def printKey():

#     for item in items:
#         # len = 0
#         # for i in range(12):
#         #     if len(item)
#         #     short += 1
#         print(f"{item}\t", end="") if len(item) % 8 > 2 else print(
#             f"{item}      \t", end=""
#         )
#     print()

"""
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
"""

# requested output:
# filter out anything cancelled 24 hours before or more
# for reservations cancelled  with less than 24 hours:
# show when made and when cancelled
# extract hours between creation and cancellation
# adjustable thresholds for everything


if __name__ == "__main__":
    # jays_pretty_print(
    #     header=["title", "author", "year"],
    #     data=[
    #         ["aasfasdfasdfadfasfdas", "bfdsf", "c"],
    #         ["dss", "edd", "f"],
    #     ],
    # )
    main()
