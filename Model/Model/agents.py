from mesa import Agent
from .random_walk import RandomWalker


class CyanWalker(RandomWalker):
    """
    Walky boy
    """
    finished = False

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.finished = False

    def step(self):
        """
        A model step. Move.
        """
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True


class RedWalker(RandomWalker):
    """
    Walky boy but different colour
    """
    finished = False

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.finished = False

    def step(self):
        """
        A model step. Move.
        """
        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True


class Finish(Agent):

    finished = False

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass
