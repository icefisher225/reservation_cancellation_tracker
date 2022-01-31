from __future__ import annotations
from ast import parse  # make typehints vanish at runtime
import datetime, sys
from pickle import NONE
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
        hours_deleted_before_play="",
        empty=False,
    ):
        if empty == False:
            self.creation_time = creation_time
            self.deletion_time = deletion_time
            res_time = datetime.datetime.strptime(
                self.creation_time, "%m/%d/%y %I:%M %p"
            )
            play_time = datetime.datetime.strptime(
                self.deletion_time, "%m/%d/%y %I:%M %p"
            )
            self.time_delta = play_time - res_time
            self.play_start_time = play_start_time
            self.court = court
            self.players = players
            self.booking_user = booking_user
            self.hours_deleted_before_play = hours_deleted_before_play
        self.empty = empty

    @property
    def get_creation_time(self):
        return self.creation_time

    @property
    def get_deletion_time(self):
        return self.deletion_time

    @property
    def get_play_start_time(self):
        return self.play_start_time

    def prettyprint(self):
        return [
            str(self.creation_time),
            str(self.deletion_time),
            str(self.time_delta),
            str(self.play_start_time),
            self.court,
            self.players,
            self.booking_user,
            self.hours_deleted_before_play,
        ]


class Keys:
    def __init__(self, *, fmt=[]):
        if fmt == []:
            self._key_lst = [
                "Reservation Creation Time",
                "Reservation Deletion Time",
                "Reservation Time Delta",
                "Play Start Time",
                "Court",
                "Players/Machines",
                "Booking User",
                "Hours Deleted Before Play Time",
            ]
        else:
            self._key_lst = list()
            for item in fmt:
                self._key_lst.append(item)

    @property
    def get_keys(self):
        return self._key_lst


def get_time(st):
    """
    :st: A string to be converted to a date/time
    :return: A datetime object of the date/time
    """
    return datetime.datetime.strptime(st, "%m/%d/%y %I:%M %p")


def parse_line(line):
    """
    :line -> str:      Line from CSV
    :return -> Entry:  Entry contaning either the line's information or the empty tag
    """
    line = line.strip().replace('"', "").split(",")
    if (
        line[8] != "Indoor"
        or line[1] != ""
        or line[3] != ""
        or line[16] == ""
        or int(line[16]) > 24
    ):
        return Entry(empty=True)
    else:
        resv = list()
        for item in line:
            if item == "":
                # Checks and removes empty fields from the line. Could cause problems...
                # TODO: Replace this entire chunk of code with one that parses the first line of the CSV and determines what needs to go where based on that
                continue
            if item.isnumeric():
                if int(item) > 24:
                    # check if reservation was deleted more than 24 hours in advance at the same time as removing all the irrelevant numeric fields
                    # yes, this is cheating and will likely cause issues in the future.
                    # TODO: fix this by creating a proper genericized CSV parser
                    continue
            resv.append(item)
        return Entry(
            creation_time=resv[1],
            deletion_time=resv[0],
            play_start_time=" ".join([resv[2], resv[3]]),
            court=resv[6],
            players=", ".join(
                resv[7]
                .replace("<i>", "")
                .replace("</i>", "")
                .replace("<hr>", ": ")
                .replace("&#39;", "'")
                .replace("#1I", "#1")
                .replace("#2I", "#2")
                .split("<br>")
            ),
            booking_user=resv[8],
            hours_deleted_before_play=resv[9],
        )


def main():
    f = sys.argv[1]
    reservations = list()
    with open(f, "r") as file:
        # This is where a first line parser would come in...
        key = file.readline()
        for line in file:
            entry = parse_line(line)
            if entry.empty == False:
                reservations.append(entry)

    day = datetime.timedelta(seconds=86400)
    problem_rsvs = list()
    possible_problem_rsvs = list()

    for item in reservations:
        if item.time_delta > day:
            problem_rsvs.append(item.prettyprint())
        else:
            possible_problem_rsvs.append(item.prettyprint())

    keys = Keys()

    print("\nReservations created outside of a 24-hour play window:\n")
    pretty_print(header=keys.get_keys, data=problem_rsvs)
    print("\n\nReservations created inside a 24-hour play window:\n")
    pretty_print(header=keys.get_keys, data=possible_problem_rsvs)


def pretty_print(
    *,
    header: list[str],
    data: list[list[str]],
    output: Callable[[str], Any] = print,
):

    """
    #Sample Code:
    # pretty_print(
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
