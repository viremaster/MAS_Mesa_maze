from mesa import Agent
from .static_objects import Finish, Wall, RedObstacle, CyanObstacle
from random import randint

red_obstacle = 0
cyan_obstacle = 0


class CyanWalker(Agent):
    """
    Walky boy.
    """
    # Load the global variable if there is an obstacle
    global cyan_obstacle

    finished = False
    grid = None
    x = None
    y = None
    moore = True
    first = True
    previous_trace = []
    trace_tracker = None
    noise = 0
    cyan_obstacle_present = cyan_obstacle
    box_drop_chance = 0
    box_duration = 0
    box_amount = 0

    def __init__(self, unique_id, pos, model, trace_tracker, moore=True, noise=0, box_drop_chance=0, box_duration=0, box_amount=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False
        self.trace_tracker = trace_tracker
        self.noise = noise
        self.cyan_obstacle_present = cyan_obstacle
        self.obstacle = CyanObstacle(self.model.next_id(), self.pos, self.model, 0, box_duration)
        self.box_drop_chance = box_drop_chance
        self.box_duration = box_duration
        self.box_amount = box_amount

    def step(self):
        """
        Move, then check if finished
        """
        # Check if there is an obstacle
        global cyan_obstacle
        self.cyan_obstacle_present = cyan_obstacle

        # If there is check if it should be removed
        if self.obstacle.present > self.box_duration:
            self.obstacle.present = 0
            self.model.schedule.remove(self.obstacle)
            self.model.grid.remove_agent(self.obstacle)
            cyan_obstacle -= 1

        # Store the previous position
        previous_pos = self.pos

        # Make a move
        self.non_random_move()

        # If you moved, put a trace in the previous square
        if not self.finished and not previous_pos == self.pos:
            if self.pos[0] > previous_pos[0]:
                trace = EfficientTrace(previous_pos, self, "Right", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[0] < previous_pos[0]:
                trace = EfficientTrace(previous_pos, self, "Left", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[1] > previous_pos[1]:
                trace = EfficientTrace(previous_pos, self, "Up", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[1] < previous_pos[1]:
                trace = EfficientTrace(previous_pos, self, "Down", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            if not self.first:
                self.previous_trace.set_next(trace)
            self.previous_trace = trace
            if self.first:
                self.first = False

        # Check if you finished, if so remove yourself and update your trace
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True
            self.previous_trace.distance = 1
            self.previous_trace.previous.adjust_distance()
            self.model.grid.remove_agent(self)

    def random_move(self):
        """
        Make a random move
        """
        # Make a list of all the moves in your neighborhood
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        next_moves_copy = next_moves.copy()
        # For every move in the list
        for i in next_moves:
            # If the square is occupied
            i_types = self.model.grid.get_cell_list_contents(i)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, RedObstacle)]
            if occupied:
                # Remove the move from the list of possible moves
                next_moves_copy.remove(i)
        # Add standing still to the list of possible moves
        next_moves_copy.append(self.pos)

        # Move to a random one of the possible options
        next_move = self.random.choice(next_moves_copy)
        self.model.grid.move_agent(self, next_move)

    def non_random_move(self):
        """
        Make a move that follows traces if possible, otherwise make a random_move()
        """
        global cyan_obstacle

        # As long as you haven't finished
        if not self.finished:
            # Randomly determine whether to place an obstacle
            if cyan_obstacle < self.box_amount and randint(1, 100) <= self.box_drop_chance:
                # Add an obstacle to the model and schedule also update the variables
                self.model.grid.place_agent(self.obstacle, self.pos)
                self.model.schedule.add(self.obstacle)
                cyan_obstacle += 1
                self.cyan_obstacle_present = cyan_obstacle
            else:
                # Randomly determine whether to follow a trace or not
                if randint(1, 100) >= self.noise:
                    # Find if there is a shortest path among the traces in this square.
                    trace = self.trace_tracker.find_shortest_trace(self.pos)
                    if trace:
                        # If there is one, follow it if the space it leads to is not occupied.
                        i_types = self.model.grid.get_cell_list_contents(self.pointing_at(trace.direction))
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, RedObstacle)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, self.pointing_at(trace.direction))
                    else:
                        self.random_move()
                else:
                    self.random_move()

    def pointing_at(self, direction):
        """
        Return the space that a trace is pointing to
        """
        if direction == "Up":
            return self.pos[0], self.pos[1]+1
        elif direction == "Down":
            return self.pos[0], self.pos[1]-1
        elif direction == "Left":
            return self.pos[0]-1, self.pos[1]
        else:
            return self.pos[0]+1, self.pos[1]


class RedWalker(Agent):
    """
    Walky boy but different colour, comments for this class can be found in the CyanWalker class above.
    """
    global red_obstacle

    finished = False
    grid = None
    x = None
    y = None
    moore = True
    first = True
    previous_trace = []
    trace_tracker = None
    noise = 0
    red_obstacle_present = red_obstacle
    box_drop_chance = 0
    box_duration = 0
    box_amount = 0

    def __init__(self, unique_id, pos, model, trace_tracker, moore=True, noise=0, box_drop_chance=0, box_duration=0, box_amount=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False
        self.trace_tracker = trace_tracker
        self.noise = noise
        self.red_obstacle_present = red_obstacle
        self.obstacle = RedObstacle(self.model.next_id(), self.pos, self.model, 0, box_duration)
        self.box_drop_chance = box_drop_chance
        self.box_duration = box_duration
        self.box_amount = box_amount

    def step(self):
        global red_obstacle
        self.red_obstacle_present = red_obstacle

        if self.obstacle.present > self.box_duration:
            self.obstacle.present = 0
            self.model.schedule.remove(self.obstacle)
            self.model.grid.remove_agent(self.obstacle)
            red_obstacle -= 1

        previous_pos = self.pos

        self.non_random_move()

        if not self.finished and not previous_pos == self.pos:
            if self.pos[0] > previous_pos[0]:
                trace = EfficientTrace(previous_pos, self, "Right", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[0] < previous_pos[0]:
                trace = EfficientTrace(previous_pos, self, "Left", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[1] > previous_pos[1]:
                trace = EfficientTrace(previous_pos, self, "Up", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            elif self.pos[1] < previous_pos[1]:
                trace = EfficientTrace(previous_pos, self, "Down", self.previous_trace)
                self.trace_tracker.add_trace(trace)
            if not self.first:
                self.previous_trace.set_next(trace)
            self.previous_trace = trace
            if self.first:
                self.first = False

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        finish = [obj for obj in this_cell if isinstance(obj, Finish)]
        if finish:
            self.finished = True
            self.previous_trace.distance = 1
            self.previous_trace.previous.adjust_distance()
            self.model.grid.remove_agent(self)

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=self.moore, include_center=False)
        next_moves_copy = next_moves.copy()
        for i in next_moves:
            i_types = self.model.grid.get_cell_list_contents(i)
            occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, CyanObstacle)]
            if occupied:
                next_moves_copy.remove(i)
        next_moves_copy.append(self.pos)
        next_move = self.random.choice(next_moves_copy)
        self.model.grid.move_agent(self, next_move)

    def non_random_move(self):
        global red_obstacle

        if not self.finished:
            if red_obstacle < self.box_amount and randint(1, 100) <= self.box_drop_chance:
                self.model.grid.place_agent(self.obstacle, self.pos)
                self.model.schedule.add(self.obstacle)
                red_obstacle += 1
                self.red_obstacle_present = red_obstacle
            else:
                if randint(1, 100) >= self.noise:
                    trace = self.trace_tracker.find_shortest_trace(self.pos)
                    if trace:
                        i_types = self.model.grid.get_cell_list_contents(self.pointing_at(trace.direction))
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker) or isinstance(j, Wall) or isinstance(j, CyanObstacle)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, self.pointing_at(trace.direction))
                    else:
                        self.random_move()
                else:
                    self.random_move()
        else:
            self.random_move()

    def pointing_at(self, direction):
        if direction == "Up":
            return self.pos[0], self.pos[1]+1
        elif direction == "Down":
            return self.pos[0], self.pos[1]-1
        elif direction == "Left":
            return self.pos[0]-1, self.pos[1]
        else:
            return self.pos[0]+1, self.pos[1]


class TraceTracker:
    """
    A class that keeps track of all the traces of this color.
    """
    traces = []

    def __init__(self):
        self.traces = []

    def add_trace(self, trace):
        self.traces.append(trace)

    def find_traces(self, pos):
        results = []
        for trace in self.traces:
            if trace.pos == pos:
                results.append(trace)
        return results

    def find_shortest_trace(self, pos):
        current_length = -1
        current_fastest = None
        for trace in self.traces:
            if trace.pos == pos and 0 < trace.distance and (current_length > trace.distance or current_length == -1):
                current_fastest = trace
                current_length = trace.distance
        return current_fastest


class EfficientTrace:
    pos = (0, 0)
    owner = 0
    direction = "Up"
    next = None
    previous = None
    distance = -1

    def __init__(self, pos, owner, direction, previous):
        self.pos = pos
        self.owner = owner
        self.direction = direction
        self.previous = previous

    def set_next(self, next_trace):
        self.next = next_trace

    def adjust_distance(self):
        self.distance = self.next.distance + 1
        if self.previous and self.distance < 975:
            self.previous.adjust_distance()
