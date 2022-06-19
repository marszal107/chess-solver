import unittest
from models.pawn import Pawn


class PawnTestCases(unittest.TestCase):
    def test_pawn_should_move_one_forward(self):
        # Arrange
        pawn = Pawn('E1')

        # Act
        available_moves = pawn.list_available_moves()

        # Assert
        self.assertEqual(len(available_moves), 1)
        self.assertEqual(available_moves[0], 'E2')

    def test_pawn_shouldnt_move_one_forward_on_last_tile(self):
        # Arrange
        pawn = Pawn('E8')

        # Act
        available_moves = pawn.list_available_moves()

        # Assert
        self.assertEqual(available_moves, None)

    def test_pawn_should_move_when_field_empty(self):
        # Arrange
        pawn = Pawn('E1')

        # Act
        validation, error = pawn.validate_move('E2')

        # Assert
        self.assertEqual(validation, 'valid')

    def test_pawn_shouldnt_move_when_field_occupied(self):
        # Arrange
        pawn = Pawn('E1')
        pawn2 = Pawn('E2')

        # Act
        validation, error = pawn.validate_move('E2')

        # Assert
        self.assertEqual(validation, 'valid')


if __name__ == '__main__':
    unittest.main()
