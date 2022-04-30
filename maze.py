#!/usr/bin/env python3
import sys
from room import Room


class Maze:
    """Class to save all the characteristics of a maze"""

    def __init__(self, file_name="default.maze"):
        self.width = None
        self.height = None
        self.floors = None
        self.rooms = None
        self.goal = None
        self.start = None
        self.read_maze(file_name)

    def get_goal(self):
        """
        :return: The coordinates (x, y, z) of the goal room
        """
        return self.goal

    def get_start(self):
        """
        :return: The coordinates (x, y, z) of the start room
        """
        return self.start

    def get_room(self, x, y, z):
        """
        returns the room with coordinates (x, y, z)
        :param x: z coordinate of the desired room
        :param y: x coordinate of the desired room
        :param z: y coordinate of the desired room
        :return: The room with coordinates (x, y, z)
        """
        return self.rooms[x][y][z]

    # -------------------------------------------------------------------------------------	#
    # The part below is only for reading the maze files and printing the maze				#
    # it is not needed to look through it or to understand it 								#
    # ------------------------------------------------------------------------------------- #

    @staticmethod
    def get_move_dir(from_coords, to_coords):
        if from_coords[2] - to_coords[2] == -1:
            return "UP"
        if from_coords[2] - to_coords[2] == 1:
            return "DOWN"
        if from_coords[0] - to_coords[0] == -1:
            return "EAST"
        if from_coords[0] - to_coords[0] == 1:
            return "WEST"
        if from_coords[1] - to_coords[1] == 1:
            return "NORTH"
        if from_coords[1] - to_coords[1] == -1:
            return "SOUTH"
        return ""

    @staticmethod
    def get_dir(room, to_from, direction):
        coords = room.get_coords()
        if coords in direction and to_from in direction[coords]:
            return direction[room.get_coords()][to_from]
        return ""

    def read_maze(self, file_name):
        try:
            f = open(file_name, "r")
        except FileNotFoundError:
            print("File: " + file_name + " not found, exit")
            sys.exit(-1)
        self.width = int(f.readline().split("Width:")[1].strip())
        self.height = int(f.readline().split("Height:")[1].strip())
        self.floors = int(f.readline().split("Floors:")[1].strip())
        self.rooms = [[[None for _ in range(self.floors)]
                       for _ in range(self.height)] for _ in range(self.width)]

        for idx in range(self.floors):
            self.read_floor(f)

    @staticmethod
    def get_heuristic(row):
        string = (str(row[1]) + str(row[2])).strip()
        try:
            return int(string)
        except ValueError:
            return None

    @staticmethod
    def check_connection(room, cell, direction):
        check = " "
        cost = 1
        if direction == "UP":
            check = "U"
            cost += 2
        if direction == "DOWN":
            check = "D"
            cost += 1
        if cell == check or cell.isnumeric():
            room.connections.append(direction)
            if cell.isnumeric():
                room.costs[direction] = int(cell)
            else:
                room.costs[direction] = cost

    def read_floor(self, f):
        line = f.readline()
        # get rid of empty lines
        while "Floor #" not in line:
            line = f.readline()
        floor = int(line.split("Floor #")[1].strip())
        lines = [None] * 5
        # order:0 UP, 1 DOWN,2 NORTH,3 SOUTH,4 EAST,5 WEST

        # read first row
        lines[0] = f.readline()
        # loop through each row
        for idy in range(self.height):
            for i in range(1, 5):
                lines[i] = f.readline()
            for idx in range(self.width):
                # create room and add to array
                room = Room((idx, idy, floor), self)
                self.rooms[idx][idy][floor] = room
                start = idx * 8
                # get part of input for one room
                r = [row[start:start + 9] for row in lines]
                room.heuristicValue = self.get_heuristic(r[1])
                self.check_connection(room, r[2][2], "UP")
                self.check_connection(room, r[2][6], "DOWN")
                self.check_connection(room, r[0][4], "NORTH")
                self.check_connection(room, r[4][4], "SOUTH")
                self.check_connection(room, r[2][8], "EAST")
                self.check_connection(room, r[2][0], "WEST")
                if "G" in r[2]:
                    self.goal = (idx, idy, floor)
                    room.set_goal()
                if "X" in r[2]:
                    self.start = (idx, idy, floor)
                    room.set_start()
            # last line is first line for next row
            lines[0] = lines[4]

    def get_room_line_one(self, room, print_coords, direction):
        # value_when_true if condition else value_when_false
        c = " "
        if self.get_dir(room, 'from', direction) is "NORTH":
            c = "v"
        if self.get_dir(room, 'to', direction) is "NORTH":
            c = "^"

        return ("|--|%s|--" % c) if room.can_move_to("NORTH") else "|-------"

    def get_room_line_two(self, room, print_coords, direction):
        west = "-" if room.can_move_to("WEST") else "|"
        c = " "
        if self.get_dir(room, 'from', direction) is "NORTH":
            c = "v"
        if self.get_dir(room, 'to', direction) is "NORTH":
            c = "^"
        heuristic = "  "
        if room.get_heuristic_value() is not None:
            heuristic = '{:>2}'.format(room.get_heuristic_value())
        cost = "   "
        coords = room.get_coords()
        if coords in direction and 'cost' in direction[coords]:
            cost = '{:>3}'.format(direction[room.get_coords()]['cost'])
        return "%s%s %s%s" % (west, heuristic, c, cost)

    def get_middle_char(self, room, direction):
        if room.is_start():
            return "X"
        if room.is_goal():
            return "G"
        if self.get_dir(room, 'to', direction) is "UP":
            return "o"
        if self.get_dir(room, 'to', direction) is "DOWN":
            return "o"
        if self.get_dir(room, 'from', direction) is "UP":
            return "o"
        if self.get_dir(room, 'from', direction) is "DOWN":
            return "o"
        return " "

    def get_room_line_three(self, room, print_coords, direction):
        up = "U" if room.can_move_to("UP") else " "
        down = "D" if room.can_move_to("DOWN") else " "
        west = " " if room.can_move_to("WEST") else "|"
        from_to_west = " "
        from_to_east = " "
        if self.get_dir(room, 'from', direction) is "WEST":
            from_to_west = ">"
        if self.get_dir(room, 'to', direction) is "WEST":
            from_to_west = "<"
        if self.get_dir(room, 'from', direction) is "EAST":
            from_to_east = "<"
        if self.get_dir(room, 'to', direction) is "EAST":
            from_to_east = ">"

        mid = self.get_middle_char(room, direction)
        return ("%s%s%s%s%s%s%s%s" %
                (west, from_to_west, up, from_to_west, mid, from_to_east, down, from_to_east))

    def get_room_line_four(self, room, print_coords, direction):
        west = "-" if room.can_move_to("WEST") else "|"
        if print_coords:
            return "%s %s %s %s " % ((west,) + room.get_coords())
        c = " "
        if self.get_dir(room, 'from', direction) is "SOUTH":
            c = "^"
        if self.get_dir(room, 'to', direction) is "SOUTH":
            c = "v"
        return "%s   %s   " % (west, c)

    def get_directions(self, state):
        direction = {}
        while state is not None:
            parent = state.get_parent()
            if parent is None:
                break
            coords = state.get_room().get_coords()
            if coords not in direction:
                direction[coords] = {}
            direction[coords]['from'] = \
                self.get_move_dir(coords, parent.get_room().get_coords())
            direction[coords]['cost'] = state.get_cost()

            if parent.get_room().get_coords() not in direction:
                direction[parent.get_room().get_coords()] = {}
            direction[parent.get_room().get_coords()]['to'] = \
                self.get_move_dir(parent.get_room().get_coords(), coords)

            state = parent
        return direction

    def get_floor_string(self, idz, print_coords, direction={}):
        lines = [""] * (4 * self.height + 1)
        y_line = 0
        for idy in range(self.height):
            y_line = idy * 4
            for idx in range(self.width):
                room = self.rooms[idx][idy][idz]
                lines[y_line] += self.get_room_line_one(room, print_coords, direction)
                lines[y_line + 1] += self.get_room_line_two(room, print_coords, direction)
                lines[y_line + 2] += self.get_room_line_three(room, print_coords, direction)
                lines[y_line + 3] += self.get_room_line_four(room, print_coords, direction)

            for i in range(4):
                lines[y_line + i] += "|"
        lines[y_line + 4] += "|-------" * self.width + "|"
        return lines

    def print_maze(self, print_coords=False):
        """
        Prints the maze to std out. If print_coords is True, then it also prints the coordinates in each cell
        :param print_coords: Boolean (True, False) to print coordinates or not.
        """
        self.print_maze_with_path(None, print_coords=print_coords)

    def print_maze_with_path(self, state, print_coords=False):
        d = self.get_directions(state)
        print("Width: %d \nHeight: %d \nFloors: %d" %
              (self.width, self.height, self.floors))

        # loop descending through all floors
        for f in range(self.floors - 1, -1, -1):
            print("\nFloor #" + str(f))
            for line in self.get_floor_string(f, print_coords, direction=d):
                print(line)
