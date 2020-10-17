from mesa import Agent
from .random_walk import RandomWalker

red_obstacle = False
cyan_obstacle = False

class CyanWalker(RandomWalker):
    """
     Walky boy but different colour, comments for this class can be found in the CyanWalker class above
    """
    global cyan_obstacle

    finished = False
    grid = None
    x = None
    y = None
    moore = True
    cyan_obstacle_present = cyan_obstacle

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.finished = False
        self.cyan_obstacle_present = cyan_obstacle
        self.obstacle = CyanObstacle(self.model.next_id(), self.pos, self.model, 1)

    def step(self):
        """
        A model step. Move. Then check if you have finished, if so set your status to finished.
        """
        global cyan_obstacle
        self.cyan_obstacle_present = cyan_obstacle

        if self.obstacle.present > 11:
            self.obstacle.present = 0
            self.model.schedule.remove(self.obstacle)
            self.model.grid.remove_agent(self.obstacle)
            cyan_obstacle = False

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

    def random_move(self):
        global cyan_obstacle

        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        next_moves_copy = next_moves.copy()
        count = 0
        for i in next_moves:
            count += 1
            i_types = self.model.grid.get_cell_list_contents(i)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, RedObstacle)]
            if occupied:
                next_moves_copy.remove(i)
        next_moves_copy.append(self.pos)

        # Add dropping an obstacle to the possibilities
        if cyan_obstacle == False and self.finished == False:
            next_moves_copy.append("drop_obstacle")
        # Choose a move randomly
        next_move = self.random.choice(next_moves_copy)
        # Move
        if next_move != 'drop_obstacle':
            self.model.grid.move_agent(self, next_move)
        else:
            self.model.grid.place_agent(self.obstacle, self.pos)
            self.model.schedule.add(self.obstacle)
            cyan_obstacle = True
            self.cyan_obstacle_present = cyan_obstacle



class RedWalker(RandomWalker):
    """
     Walky boy but different colour, comments for this class can be found in the CyanWalker class above
    """
    global red_obstacle

    finished = False
    grid = None
    x = None
    y = None
    moore = True
    red_obstacle_present = red_obstacle

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.finished = False
        self.red_obstacle_present = red_obstacle
        self.obstacle = RedObstacle(self.model.next_id(), self.pos, self.model, 1)

    def step(self):
        """
        A model step. Move.
        """
        global red_obstacle
        self.red_obstacle_present = red_obstacle

        if self.obstacle.present > 11:
            self.obstacle.present = 0
            self.model.schedule.remove(self.obstacle)
            self.model.grid.remove_agent(self.obstacle)
            red_obstacle = False

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

    def random_move(self):
        global red_obstacle

        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        next_moves_copy = next_moves.copy()
        count = 0
        for i in next_moves:
            count += 1
            i_types = self.model.grid.get_cell_list_contents(i)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, CyanObstacle)]
            if occupied:
                next_moves_copy.remove(i)
        next_moves_copy.append(self.pos)

        # Add dropping an obstacle to the possibilities
        if red_obstacle == False and self.finished == False:
            next_moves_copy.append("drop_obstacle")
        # Choose a move randomly
        next_move = self.random.choice(next_moves_copy)
        # Move
        if next_move != 'drop_obstacle':
            self.model.grid.move_agent(self, next_move)
        else:
            self.model.grid.place_agent(self.obstacle, self.pos)
            self.model.schedule.add(self.obstacle)
            red_obstacle = True
            self.red_obstacle_present = red_obstacle


class Finish(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Wall(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class RedObstacle(Agent):

    def __init__(self,unique_id, pos, model, present):
        super().__init__(unique_id, model)
        self.pos = pos
        self.present = present

    def step(self):
        if self.present <= 11:
            self.present +=1

class CyanObstacle(Agent):

    def __init__(self,unique_id, pos, model, present):
        super().__init__(unique_id, model)
        self.pos = pos
        self.present = present

    def step(self):
        if self.present <= 11:
            self.present +=1

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