#!/usr/bin/env python3


class Room:
	"""Class to save all the characteristics of a room"""
	def __init__(self, coords, maze):
		# order: UP, DOWN, NORTH, SOUTH, EAST, WEST
		self.connections = []
		self.heuristicValue = 0
		self.costs = dict()
		self.coords = coords
		self.__goal = False
		self.__start = False
		self.maze = maze
		self.is_visited = False
		self.depth = 0

	def can_move_to(self, d):
		"""
		:param d: The desired direction
		:return: True if the move is possible, False otherwise
		"""
		return d in self.connections

	def get_connections(self):
		"""
		:return: All possible moves from this room
		"""
		return self.connections

	def is_goal(self):
		"""
		:return: True if room is the goal room, False otherwise
		"""
		return self.__goal

	def set_goal(self):
		"""
		Sets the room as goal room
		"""
		self.__goal = True

	def is_start(self):
		"""
		:return: True if room is the start room, False otherwise
		"""
		return self.__start

	def set_start(self):
		"""
		Sets the room as start room
		"""
		self.__start = True

	def get_coords(self):
		"""
		:return: The coordinates of the room (x, y, z)
		"""
		return self.coords

	def get_heuristic_value(self):
		"""
		:return: The heuristic value of the room
		"""
		return self.heuristicValue

	def make_move(self, direction, cost):
		"""
		:param direction: The direction of the move
		:param cost: The cost it took to come to this room
		:return: The new room and cost if move is possible, None otherwise
		"""
		x, y, z = self.coords
		# if move is not valid, return None
		if not self.can_move_to(direction):
			return None
		cost += self.costs[direction]
		if direction is "UP":
			z += 1
		if direction is "DOWN":
			z -= 1
		if direction is "EAST":
			x += 1
		if direction is "WEST":
			x -= 1
		if direction is "NORTH":
			y -= 1
		if direction is "SOUTH":
			y += 1
		return self.maze.rooms[x][y][z], cost
