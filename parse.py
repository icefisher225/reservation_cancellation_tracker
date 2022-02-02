from __future__ import annotations
from ast import parse  # make typehints vanish at runtime
import datetime, sys
from pickle import NONE
from typing import *

# from click import FileError
# from platformdirs import user_cache_dir

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
    def __init__(self, *, fmt=[], default=False, size=0):
        self._keys = {}
        self._size = size
        self.__iter = 0
        if default == True:
            fmt = [
                "Reservation Creation Time",
                "Reservation Deletion Time",
                "Reservation Time Delta",
                "Play Start Time",
                "Court",
                "Players/Machines",
                "Booking User",
                "Hours Deleted Before Play Time",
            ]
        if len(fmt) != 0:
            for item in fmt:
                self._keys[str(self._size)] = item
                self._size += 1

    # @property
    # def add_item(self, item):
    #     self._keys[str(self._size)] = item
    #     self._size += 1

    @property
    def get_keys(self):
        return list((i for i in self._keys.values()))

    def __len__(self):
        return self._size

    def __iter__(self):
        # This makes something iterable
        # returns an iterable o
        return (i for i in self._keys)
        # return self?
        # TODO: I believe this is the method I need to implement to get this to work like a normal list...
        pass

    def __next__(self):
        # this is for an actual iterATOR
        if self.__iter >= self._size:
            raise StopIteration
        else:
            temp = self._keys.get(str(self.__iter))
            self.__iter += 1
            return temp
            # TODO: This might also be a method I need to implement...
            pass


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
        or int(line[16]) >= 24
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
                if len(item) > 2:
                    continue
                # if int(item) > 24:
                #     # check if reservation was deleted more than 24 hours in advance at the same time as removing all the irrelevant numeric fields
                #     # yes, this is cheating and will likely cause issues in the future. (It's not actually checking the 25-hour thing, that's happening somewhere else)
                #     # TODO: fix this by creating a proper genericized CSV parser (done?)
                #     continue
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


def pretty_print(
    *,
    header: list[str],
    data: list[list[str]],
    output: Callable[[str], Any] = print,
):

    """
    This function was authored by @TG_Techie, edited by @icefisher225

    #Sample Code:
    # pretty_print(
    #     header=["title", "author", "year"],
    #     data=[
    #         ["Harry Potter and the Sorceror's Stone", "J.K. Rowling", "1997"],
    #         ["A Tale of Two Cities", "Charles Dickins", "1859"],
    #     ],
    # )
    """

    assert isinstance(
        data, list
    ), f"data must be type list, got type {type(data)} \ndata must be type list[list[str]]"
    assert len(data), "data cannot be empty"

    assert isinstance(
        data[0], list
    ), f"data[0] must be type list, got type {type(data[0])} \ndata must be type list[list[str]]"
    assert len(data[0]), "data[0] cannot be empty"

    assert isinstance(
        data[0][0], str
    ), f"data[0][0] must be type str, got type {type(data[0][0])} \ndata must be type list[list[str]]"
    assert len(data[0][0]), "data[0][0] cannot be empty"

    assert len(header) == len(
        data[0]
    ), f"header and data[0] must contain same number of items, header[{len(header)}] != data[0][{len(data[0])}]"

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


def help(part=2):
    if part == 1:
        return f"\nRun this script either using:\n\n\t{sys.argv[0]} -f <file> \n\t\tor\n\t{sys.argv[0]} and follow the prompts.\n\n"

    else:
        return (
            f"\nScript options: \n\n"
            + f"\t-f <file>\tPass the file to be processed\n"
            + f"\t--file <file>\n\n"
            + f"\t-h\t\tPrint help\n"
            + f"\t--help\n"
        )


def get_file():
    try:
        if sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(f"{help(2)}")
            exit()
        if sys.argv[1] == "-f" or sys.argv[1] == "--file":
            try:
                return sys.argv[2]
            except IndexError as IdxError:
                print(f"\nIncorrect usage of {sys.argv[1]}")
                print(f"{help(2)}")
                exit()
    except IndexError as IdxError:
        try:
            return input(f"Please drag and drop the file you'd like to process: ")
        except Exception as Ex:
            pass
    except Exception as Ex:
        pass
    print(f"{help(1)}")
    exit()


def main():
    f = get_file()
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

    keys = Keys(default=True)

    print("\nReservations created outside of a 24-hour play window:\n")
    pretty_print(header=keys.get_keys, data=problem_rsvs)
    print("\n\nReservations created inside a 24-hour play window:\n")
    pretty_print(header=keys.get_keys, data=possible_problem_rsvs)


if __name__ == "__main__":
    main()
