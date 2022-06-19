from models.figure import Figure
from models.board import Board


class Rook(Figure):
    name = "rook"

    def __init__(self, current_field):
        super().__init__(current_field)
        self.board = Board()

    def list_available_moves(self):
        current_index = self.find_in_nested_list(self.board.fields, self.current_field)
        directions = [(1, 0), (0, 1)]
        possible_moves = []
        for dir in directions:
            for m in (-1, 1):
                d = (dir[0] * m, dir[1] * m)
                for i in range(1, 9):
                    row = current_index[0] + d[0] * i
                    col = current_index[1] + d[1] * i
                    if -1 < row < 8 and 8 > col > -1:
                        possible_moves.append(self.board.fields[row][col])
        return possible_moves

    def validate_move(self, dest_field):
        current_index = self.find_in_nested_list(self.board.fields, self.current_field)
        dest_index = self.find_in_nested_list(self.board.fields, dest_field)
        if (
            self.board.occupation.get(dest_field) == ""
            and dest_field in self.list_available_moves()
        ):
            diff = (dest_index[0] - current_index[0], dest_index[1] - current_index[1])
            if diff[0] > 0:
                for i in range(diff[0]):
                    if (
                        self.board.occupation.get(
                            self.board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[0] < 0:
                for i in range(0, diff[0], -1):
                    if (
                        self.board.occupation.get(
                            self.board.fields[dest_index[0] - i][dest_index[1]]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            if diff[1] > 0:
                for i in range(diff[1]):
                    if (
                        self.board.occupation.get(
                            self.board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            elif diff[1] < 0:
                for i in range(0, diff[1], -1):
                    if (
                        self.board.occupation.get(
                            self.board.fields[dest_index[0]][dest_index[1] - i]
                        )
                        != ""
                    ):
                        return "invalid", "Current move is not permitted"
            return "valid", None
        else:
            return "invalid", "Current move is not permitted"