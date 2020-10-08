from .random_walk import RandomWalker


class CyanWalker(RandomWalker):
    """
    Walky boy
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        """
        A model step. Move.
        """
        self.random_move()


class RedWalker(RandomWalker):
    """
    Walky boy but different colour
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        """
        A model step. Move.
        """
        self.random_move()
