from string import ascii_uppercase


class Board:
    def __init__(self):
        self.fields = [[i + str(j) for i in ascii_uppercase[:8]] for j in range(1, 9)]
        self.occupation = {
            i + str(j): "" for i in ascii_uppercase[:8] for j in range(1, 9)
        }
