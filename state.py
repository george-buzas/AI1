#!/usr/bin/env python3
import maze


class State:
	"""Class to save the possible states in"""
	def __init__(self, room, parent, cost=0, priority=0):
		self.parent = parent
		self.room = room
		self.cost = cost
		self.priority = priority

	def get_room(self):
		"""
		:return: The room of which this state is in
		"""
		return self.room

	# returns the previous state
	def get_parent(self):
		"""
		:return: The parent/previous state
		"""
		return self.parent

	def get_cost(self):
		"""
		:return: The cost to get to this state
		"""
		return self.cost

	def set_cost(self, cost):
		"""
		Set the cost of this state
		:param cost: The cost of this state
		"""
		self.cost = cost

	def print_actions(self, first_call=True):
		"""
		Prints the sequence af action from start state to this state
		"""
		if first_call:  # if it is the first call to this function, print begin statement
			print("Sequence of actions: ", end="")

		if self.parent is None:  # no parent, so we are at the start node: return
			return
		else:
			self.parent.print_actions(False)
			direction = maze.Maze().get_move_dir(self.parent.room.coords, self.room.coords)
			print(direction[0], end="")

		if first_call:  # if it is the first call to this function, print newline
			print()

	def print_path_helper(self):
		"""
		Helper function to print the path from start state to this state
		"""
		if self.parent is not None:
			# if it has parent state, then first print path to that state
			self.parent.print_path_helper()
			# print previous room and this room and cost till this room
			string = str(self.parent.room.coords) + " -> "
			string += str(self.room.coords)
			string += " cost: " + str(self.cost)
			print(string)

	def print_path(self):
		"""
		Prints the path from start state to this state
		"""
		self.print_path_helper()
		print()

	def __lt__(self, other):
		"""
		Function used to compare two states for the priority queue
		:param other: State to compare this state with
		:return: True is this states priority is lower than the priority of other state. Otherwise False
		"""
		return self.priority < other.priority
