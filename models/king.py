from models.figure import Figure
from models.board import Board


class King(Figure):
    name = "king"

    def __init__(self, current_field):
        super().__init__(current_field)
        self.board = Board()

    def list_available_moves(self):
        current_index = self.find_in_nested_list(self.board.fields, self.current_field)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                row = current_index[0] + d[0]
                col = current_index[1] + d[1]
                if -1 < row < 8 and 8 > col > -1:
                    possible_moves.append(self.board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        if (
            self.board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"