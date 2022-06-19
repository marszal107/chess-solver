from string import ascii_uppercase
from abc import ABC, abstractmethod
from flask import Flask, jsonify, abort, make_response, request
from models.board import Board
from models.bishop import Bishop
from models.figure import Figure
from models.king import King
from models.knight import Knight
from models.pawn import Pawn
from models.queen import Queen
from models.rook import Rook


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
