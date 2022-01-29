from __future__ import annotations  # make typehints vanish at runtime
import datetime, sys
from typing import *

from platformdirs import user_cache_dir

# for python 3.10 and up


class Entry:
    def __init__(
        self,
        *,
        creation_time="",
        deletion_time="",
        play_start_time="",
        court="",
        players="",
        booking_user="",
        hours_before_play="",
    ):
        self.creation_time = creation_time
        self.deletion_time = deletion_time
        res_time = datetime.datetime.strptime(self.creation_time, "%m/%d/%y %I:%M %p")
        play_time = datetime.datetime.strptime(self.deletion_time, "%m/%d/%y %I:%M %p")
        self.time_delta = play_time - res_time
        self.play_start_time = play_start_time
        self.court = court
        self.players = players
        self.booking_user = booking_user
        self.hours_before_play = hours_before_play


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
            else:
                resv = list()
                for item in line:
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
                rsv = list()
                rsv.append(resv[1])
                rsv.append(resv[0])

                res_time = datetime.datetime.strptime(resv[1], "%m/%d/%y %I:%M %p")
                play_time = datetime.datetime.strptime(
                    " ".join([resv[2], resv[3]]), "%m/%d/%y %I:%M %p"
                )
                time_delta = play_time - res_time
                # print(time_delta)
                rsv.append(str(time_delta))
                # time delta needs to go here
                rsv.append(" ".join([resv[2], resv[3]]))
                rsv.append(resv[6])
                rsv.append(resv[7])
                rsv.append(resv[8])
                rsv.append(resv[9])
                reservations.append(rsv)

    for item in reservations[0]:
        print(type(item))

    day = datetime.timedelta(seconds=86400)
    problem_rsvs = list()
    possible_problem_rsvs = list()

    for item in reservations:
        res_time = datetime.datetime.strptime(item[0], "%m/%d/%y %I:%M %p")
        print(item)
        play_time = datetime.datetime.strptime(item[3], "%m/%d/%y %I:%M %p")
        time_delta = play_time - res_time
        print(time_delta)
        print(item[2])
        if time_delta > day:
            problem_rsvs.append(item)
        else:
            possible_problem_rsvs.append(item)

    keyItems = [
        "Reservation Creation Time",
        "Reservation Deletion Time",
        "Reservation Time Delta",
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

    """
    #Sample Code:
    # jays_pretty_print(
    #     header=["title", "author", "year"],
    #     data=[
    #         ["aasfasdfasdfadfasfdas", "bfdsf", "c"],
    #         ["dss", "edd", "f"],
    #     ],
    # )
    """

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


# requested output:
# filter out anything cancelled 24 hours before or more
# for reservations cancelled  with less than 24 hours:
# show when made and when cancelled
# extract hours between creation and cancellation
# adjustable thresholds for everything


if __name__ == "__main__":
    main()
