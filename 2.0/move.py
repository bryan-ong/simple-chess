from square import Square
class Move:

    # Initial and final are Squares
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __str__(self):
        return f"""
Initial:    {Square.get_alpha_col(self.initial.col)}{self.initial.row}
Final:      {Square.get_alpha_col(self.final.col)}{self.final.row}
        """