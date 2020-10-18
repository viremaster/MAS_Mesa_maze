from mesa import Agent


class Finish(Agent):
    """
    A finish line agent
    """

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass


class Wall(Agent):
    """
    A wall agent
    """

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos


class CyanObstacle(Agent):
    """
    An obstacle agent
    """
    finished = False

    def __init__(self, unique_id, pos, model, present):
        super().__init__(unique_id, model)
        self.pos = pos
        self.present = present

    def step(self):
        if self.present <= 11:
            self.present += 1


class RedObstacle(Agent):
    """
    An obstacle agent
    """
    finished = False

    def __init__(self, unique_id, pos, model, present):
        super().__init__(unique_id, model)
        self.pos = pos
        self.present = present

    def step(self):
        if self.present <= 11:
            self.present += 1
