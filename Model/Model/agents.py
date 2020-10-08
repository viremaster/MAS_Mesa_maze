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
        previous_pos = self.pos

        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True
        else:
            if self.pos[0] > previous_pos[0]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Right")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[0] < previous_pos[0]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Left")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[1] > previous_pos[1]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Up")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[1] < previous_pos[1]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Down")
                self.model.grid.place_agent(trace, previous_pos)



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

        previous_pos = self.pos

        self.random_move()

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True
        else:
            if self.pos[0] > previous_pos[0]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Right")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[0] < previous_pos[0]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Left")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[1] > previous_pos[1]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Up")
                self.model.grid.place_agent(trace, previous_pos)
            elif self.pos[1] < previous_pos[1]:
                trace = ArrowTrace(self.model.next_id(), previous_pos, self.model, self, "Down")
                self.model.grid.place_agent(trace, previous_pos)


class Finish(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass


class Trace(Agent):

    owner = 0
    colour = 0

    def __init__(self, unique_id, pos, model, owner):

        super().__init__(unique_id, model)
        self.pos = pos
        self.owner = owner
        dicto = {}
        for i in model.schedule.agents_by_colour.keys():
            dicto.update(model.schedule.agents_by_colour[i])

        owner_colour = list(dicto.keys())[list(dicto.values()).index(owner)]
        if owner_colour < 10:
            if type(owner) is RedWalker:
                self.colour = "#FF" + str(owner_colour) + "FFF"
            else:
                self.colour = "#" + str(owner_colour) + "FFFFF"
        elif owner_colour < 100:
            if type(owner) is RedWalker:
                self.colour = "#FF" + str(owner_colour) + "FF"
            else:
                self.colour = "#" + str(owner_colour) + "FFFF"
        elif owner_colour < 1000:
            if type(owner) is RedWalker:
                self.colour = "#FF" + str(owner_colour) + "F"
            else:
                self.colour = "#" + str(owner_colour) + "FFF"


class ArrowTrace(Agent):
    owner = 0
    direction = "Up"

    def __init__(self, unique_id, pos, model, owner, direction):
        super().__init__(unique_id, model)
        self.pos = pos
        self.owner = owner
        self.direction = direction

    def sprite(self):
        print("Yes")
        if self.direction == "Up":
            return "Model/resources/Up.png"
        elif self.direction == "Down":
            return "Model/resources/Down.png"
        elif self.direction == "Left":
            return "Model/resources/Left.png"
        else:
            return "Model/resources/Right.png"
