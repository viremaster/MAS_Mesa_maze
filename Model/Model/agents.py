from mesa import Agent
from random import randint


class CyanWalker(Agent):
    """
    Walky boy
    """
    finished = False
    grid = None
    x = None
    y = None
    moore = True
    first = True
    previous_trace = []

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False

    def step(self):
        """
        A model step. Move. Then check if you have finished, if so set your status to finished.
        """
        previous_pos = self.pos

        self.random_move()

        if not self.finished and not previous_pos == self.pos:
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
            if not self.first:
                self.previous_trace.set_next(trace)
            self.previous_trace = trace
            if self.first:
                self.first = False

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        # Make a copy of the possible moves
        next_moves_copy = next_moves.copy()

        # For every possible move
        for i in next_moves:
            # Retrieve the types of the agents within the target of that move
            i_types = self.model.grid.get_cell_list_contents(i)
            """
            You can add the walls into this statement.
            """
            # If there are types that are Walkers (or Walls)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
            if occupied:
                # Remove that move from the possibilities
                next_moves_copy.remove(i)
        # Add standing still to the possibilities
        next_moves_copy.append(self.pos)
        # Choose a move randomly
        next_move = self.random.choice(next_moves_copy)
        # Move
        self.model.grid.move_agent(self, next_move)


class RedWalker(Agent):
    """
    Walky boy but different colour, comments for this class can be found in the CyanWalker class above.
    """
    finished = False
    grid = None
    x = None
    y = None
    moore = True
    first = True
    previous_trace = []
    following_trace = []

    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False

    def step(self):

        previous_pos = self.pos

        self.non_random_move()

        if not self.finished and not previous_pos == self.pos:
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
            if not self.first:
                self.previous_trace.set_next(trace)
            self.previous_trace = trace
            if self.first:
                self.first = False

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        next_moves_copy = next_moves.copy()
        count = 0
        for i in next_moves:
            count += 1
            i_types = self.model.grid.get_cell_list_contents(i)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
            if occupied:
                next_moves_copy.remove(i)
        next_moves_copy.append(self.pos)
        next_move = self.random.choice(next_moves_copy)
        self.model.grid.move_agent(self, next_move)

    def non_random_move(self):
        if not self.finished:
            if self.following_trace:
                if self.following_trace.next:
                    self.model.grid.move_agent(self, self.following_trace.next.pos)
                    self.following_trace = self.following_trace.next
                else:
                    self.move_in_direction(self.following_trace.direction)
            else:
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                trace = [obj for obj in this_cell if isinstance(obj, ArrowTrace) and obj.owner.finished and isinstance(obj.owner, RedWalker)]
                if trace:
                    index = randint(0, len(trace)-1)
                    if trace[index].next:
                        self.model.grid.move_agent(self, trace[index].next.pos)
                        self.following_trace = trace[index].next
                    else:
                        self.move_in_direction(trace[index].direction)
                else:
                    self.random_move()
        else:
            self.random_move()

    def move_in_direction(self, direction):
        if direction == "Up":
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1))
        elif direction == "Down":
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1))
        elif direction == "Left":
            self.model.grid.move_agent(self, (self.pos[0]-1, self.pos[1]))
        else:
            self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1]))


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
    next = []

    def __init__(self, unique_id, pos, model, owner, direction):
        super().__init__(unique_id, model)
        self.pos = pos
        self.owner = owner
        self.direction = direction

    def sprite(self):
        # if self.owner.finished:
        #     if self.direction == "Up":
        #         return "Model/resources/Up.png"
        #     elif self.direction == "Down":
        #         return "Model/resources/Down.png"
        #     elif self.direction == "Left":
        #         return "Model/resources/Left.png"
        #     else:
        #         return "Model/resources/Right.png"
        return ""

    def set_next(self, next_trace):
        self.next = next_trace


class EfficientArrowTrace():
    owner = 0
    direction = "Up"
    next = []

    def set_next(self, next_trace):
        self.next = next_trace