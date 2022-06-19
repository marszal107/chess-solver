from abc import ABC, abstractmethod
from flask import Flask, jsonify, abort, make_response, request
from models.board import Board


class Figure(ABC):
    def __init__(self, current_field):
        self.board = Board()
        if self.board.occupation.get(current_field) != "":
            self.current_field = None
        else:
            self.current_field = current_field
            self.board.occupation[current_field] = self.name

    @abstractmethod
    def list_available_moves(self):
        """
        The list_available_moves function accepts a board object as an argument and returns a list of all the possible moves that can be made on that board.
        The function should return an empty list if there are no available moves.

        :param self: Refer to the object itself
        :return: A list of all the possible moves that can be made by a player
        :doc-author: Trelent
        """
        pass

    @abstractmethod
    def validate_move(self, dest_field):
        """
        The validate_move function checks to see if the move is valid.
        It does this by checking if the space is empty and within bounds of the board.
        If it passes these tests, then it returns True.

        :param self: Access the class attributes
        :param dest_field: Check if the destination field is empty
        :return: A boolean value
        :doc-author: Trelent
        """
        pass

    def find_in_nested_list(self, list, field):
        for sub_list in list:
            if field in sub_list:
                return (list.index(sub_list), sub_list.index(field))

    def check_message(self, current_field):
        """
        The check_message function is used to check if the current field is equal to the current field of a figure.
        If it is, then it returns a list of available moves for that figure. If not, then it returns an error message.

        :param self: Access the class attributes and methods
        :param current_field: Check if the current field is equal to the field that was sent by the user
        :return: A list of dictionaries, which contains the available moves for the selected figure and some other information
        :doc-author: Trelent
        """
        if self.current_field == current_field:
            template = [
                {
                    "availableMoves": self.list_available_moves(),
                    "error": None,
                    "figure": self.name,
                    "currentField": self.current_field,
                }
            ]
            return template
        elif (
            self.current_field != current_field
            and current_field in self.board.occupation.keys()
        ):
            template = [
                {
                    "availableMoves": [],
                    "error": "Wrong figure",
                    "figure": None,
                    "currentField": None,
                }
            ]
            abort(404, description=template)
            return jsonify(template)
        elif (
            self.current_field != current_field
            and current_field not in self.board.occupation.keys()
        ):
            template = [
                {
                    "availableMoves": [],
                    "error": "Field doesn't exist",
                    "figure": None,
                    "currentField": None,
                }
            ]
            abort(409, description=template)
            return jsonify(template)

    def validate_message(self, current_field, dest_field):
        """
        The validate_message function is used to validate the move of a figure.
        It takes two parameters: current_field and dest_field.
        The function checks if the destination field is occupied by another figure, if so it will return an error message.
        If not, it will check if the move is valid or invalid and return an

        :param self: Access the class attributes and methods
        :param current_field: Determine the current position of the figure
        :param dest_field: Check if the destination field is occupied by another figure
        :return: A dictionary with the following keys:
        :doc-author: Trelent
        """
        move, error = self.validate_move(dest_field)
        if move == "valid":
            template = [
                {
                    "move": move,
                    "figure": self.name,
                    "error": error,
                    "currentField": current_field,
                    "destField": dest_field,
                }
            ]
            return template
        elif move == "invalid" and dest_field not in self.board.occupation.keys():
            template = [
                {
                    "move": move,
                    "figure": self.name,
                    "error": error,
                    "currentField": current_field,
                    "destField": dest_field,
                }
            ]
            abort(404, description=template)
            return jsonify(template)
        elif move == "invalid" and dest_field in self.board.occupation.keys():
            template = [
                {
                    "move": move,
                    "figure": self.name,
                    "error": error,
                    "currentField": current_field,
                    "destField": dest_field,
                }
            ]
            abort(409, description=template)
            return jsonify(template)
