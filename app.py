from abc import ABC, abstractmethod
from string import ascii_uppercase
from flask import Flask, jsonify, abort, make_response, request


class Board:
    def __init__(self):
        self.fields = [[i + str(j) for i in ascii_uppercase[:8]] for j in range(1, 9)]
        self.occupation = {
            i + str(j): "" for i in ascii_uppercase[:8] for j in range(1, 9)
        }


class Figure(ABC):
    def __init__(self, current_field):
        if board.occupation.get(current_field) != "":
            self.current_field = None
        else:
            self.current_field = current_field
            board.occupation[current_field] = self.name

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
            and current_field in board.occupation.keys()
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
            and current_field not in board.occupation.keys()
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
        elif move == "invalid" and dest_field not in board.occupation.keys():
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
        elif move == "invalid" and dest_field in board.occupation.keys():
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


class King(Figure):
    name = "king"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                row = current_index[0] + d[0]
                col = current_index[1] + d[1]
                if -1 < row < 8 and 8 > col > -1:
                    possible_moves.append(board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"


class Queen(Figure):
    name = "queen"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                for i in range(1, 9):
                    row = current_index[0] + d[0] * i
                    col = current_index[1] + d[1] * i
                    if -1 < row < 8 and 8 > col > -1:
                        possible_moves.append(board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        dest_index = self.find_in_nested_list(board.fields, dest_field)
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            diff = (dest_index[0] - current_index[0], dest_index[1] - current_index[1])
            if diff[0] > 0 and diff[1] == 0:
                for i in range(diff[0]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0 and diff[1] == 0:
                for i in range(0, diff[0], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] == 0 and diff[1] > 0:
                for i in range(diff[1]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] == 0 and diff[1] < 0:
                for i in range(0, diff[1], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] > 0 and diff[1] > 0:
                for i in range(diff[0]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0 and diff[1] > 0:
                for i in range(0, diff[0], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] > 0 and diff[1] < 0:
                for i in range(diff[1]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0 and diff[1] < 0:
                for i in range(0, diff[1], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"


class Rook(Figure):
    name = "rook"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        directions = [(1, 0), (0, 1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                for i in range(1, 9):
                    row = current_index[0] + d[0] * i
                    col = current_index[1] + d[1] * i
                    if -1 < row < 8 and 8 > col > -1:
                        possible_moves.append(board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        dest_index = self.find_in_nested_list(board.fields, dest_field)
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            diff = (dest_index[0] - current_index[0], dest_index[1] - current_index[1])
            if diff[0] > 0:
                for i in range(diff[0]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0:
                for i in range(0, diff[0], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            if diff[1] > 0:
                for i in range(diff[1]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[1] < 0:
                for i in range(0, diff[1], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"


class Bishop(Figure):
    name = "bishop"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        directions = [(1, 1), (1, -1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                for i in range(1, 9):
                    row = current_index[0] + d[0] * i
                    col = current_index[1] + d[1] * i
                    if -1 < row < 8 and 8 > col > -1:
                        possible_moves.append(board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        dest_index = self.find_in_nested_list(board.fields, dest_field)
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            diff = (dest_index[0] - current_index[0], dest_index[1] - current_index[1])
            if diff[0] > 0 and diff[1] > 0:
                for i in range(diff[0]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0 and diff[1] > 0:
                for i in range(0, diff[0], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] > 0 and diff[1] < 0:
                for i in range(diff[1]):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0 and diff[1] < 0:
                for i in range(0, diff[1], -1):
                    if (
                        board.occupation.get(
                            board.fields[dest_index[0] - i][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"


class Knight(Figure):
    name = "knight"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        directions = [
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        possible_moves = []
        for dir in directions:
            # for m in (-1, 1):
            d = (dir[0], dir[1])
            row = current_index[0] + d[0]
            col = current_index[1] + d[1]
            if -1 < row < 8 and 8 > col > -1:
                possible_moves.append(board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            return "valid", None
        else:
            print("Field already taken")
            return "invalid", "Current move is not permitted"


class Pawn(Figure):
    name = "pawn"

    def __init__(self, current_field):
        super().__init__(current_field)

    def list_available_moves(self):
        d = (1, 0)
        current_index = self.find_in_nested_list(board.fields, self.current_field)
        row = current_index[0] + d[0]
        col = current_index[1] + d[1]
        if -1 < row < 8 and 8 > col > -1:
            return board.fields[row][col]

    def validate_move(self, dest_field):
        if (
            board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"


class API:
    app = Flask(__name__)

    @staticmethod
    @app.route("/api/v1/<figure>/<current_field>", methods=["GET"])
    def check_available_moves(figure, current_field):
        """
        The check_available_moves function takes a figure and the current field as arguments.
        It returns a list of available moves for that figure on that field.

        :param figure: Determine which figure is currently being moved
        :param current_field: Check if the move is possible
        :return: A list of available moves for a given figure and field
        :doc-author: Trelent
        """
        if figure == "king":
            return jsonify(king.check_message(current_field)[0])
        elif figure == "queen":
            return jsonify(queen.check_message(current_field)[0])
        elif figure == "rook":
            return jsonify(rook.check_message(current_field)[0])
        elif figure == "bishop":
            return jsonify(bishop.check_message(current_field)[0])
        elif figure == "knight":
            return jsonify(knight.check_message(current_field)[0])
        elif figure == "pawn":
            return jsonify(pawn.check_message(current_field)[0])

    @staticmethod
    @app.route("/api/v1/<figure>/<current_field>/<dest_field>", methods=["GET"])
    def validate_available_moves(figure, current_field, dest_field):
        """
        The validate_available_moves function is used to validate the moves of a given figure.
        It takes two parameters: current_field and dest_field, which are both strings.
        The function returns a JSON object with either an error message or the list of available moves.

        :param figure: Determine which figure is currently on the current_field
        :param current_field: Get the current position of the piece
        :param dest_field: Check if the destination field is occupied by a figure of the same color
        :return: A json object with the following structure:
        :doc-author: Trelent
        """
        if figure == "king":
            return jsonify(king.validate_message(current_field, dest_field))
        elif figure == "queen":
            return jsonify(queen.validate_message(current_field, dest_field))
        elif figure == "rook":
            return jsonify(rook.validate_message(current_field, dest_field))
        elif figure == "bishop":
            return jsonify(bishop.validate_message(current_field, dest_field))
        elif figure == "knight":
            return jsonify(knight.validate_message(current_field, dest_field))
        elif figure == "pawn":
            return jsonify(pawn.validate_message(current_field, dest_field))

    @staticmethod
    @app.errorhandler(404)
    def not_found(e):
        """
        The not_found function is called when no routes match. It's passed a few objects that may be useful in
        building a response.

            e: an Exception object, which can be used to get the exception message (e.message) and HTTP status code (e.status_code).
            request: the Request object from

        :param e: Pass in the error message that is generated when a user tries to access a page that doesn't exist
        :return: A 404 error message
        :doc-author: Trelent
        """
        return jsonify(str(e)), 404

    @staticmethod
    @app.errorhandler(409)
    def conflict(e):
        """
        The conflict function is used to determine if there is a conflict between two
           time periods.  It takes in two lists of the form [start, end] and returns True
           if they overlap, False otherwise.

        :param e: Represent the current state of the board
        :return: A list of the variables that are in conflict with variable e
        :doc-author: Trelent
        """
        return jsonify(str(e)), 409


if __name__ == "__main__":
    board = Board()
    pawn = Pawn("C5")
    pawn2 = Pawn("C4")
    pawn3 = Pawn("C3")
    pawn4 = Pawn("F6")
    pawn5 = Pawn("E4")
    pawn6 = Pawn("E3")
    king = King("D5")
    queen = Queen("D7")
    bishop = Bishop("D3")
    knight = Knight("C2")
    rook = Rook("F4")
    api = API()
    api.app.run(debug=True, port=8000)
