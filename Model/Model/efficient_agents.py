from mesa import Agent
from .agents import Finish
from random import randint


class CyanWalker(Agent):
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
    trace_tracker = None
    noise = 0

    def __init__(self, unique_id, pos, model, trace_tracker, moore=True, noise=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False
        self.trace_tracker = trace_tracker
        self.noise = noise

    def step(self):

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
            print(self.noise)
            if randint(1, 100) >= self.noise:
                trace = self.trace_tracker.find_shortest_trace(self.pos)
                if trace:
                    if trace.next:
                        i_types = self.model.grid.get_cell_list_contents(trace.next.pos)
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, trace.next.pos)
                    else:
                        i_types = self.model.grid.get_cell_list_contents(self.pointing_at(trace.direction))
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, self.pointing_at(trace.direction))
                else:
                    self.random_move()
            else:
                print("noised")
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
    trace_tracker = None
    noise = 0

    def __init__(self, unique_id, pos, model, trace_tracker, moore=True, noise=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.finished = False
        self.trace_tracker = trace_tracker
        self.noise = noise

    def step(self):

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
            print(self.noise)
            if randint(1, 100) >= self.noise:
                trace = self.trace_tracker.find_shortest_trace(self.pos)
                if trace:
                    if trace.next:
                        i_types = self.model.grid.get_cell_list_contents(trace.next.pos)
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, trace.next.pos)
                    else:
                        i_types = self.model.grid.get_cell_list_contents(self.pointing_at(trace.direction))
                        occupied = [j for j in i_types if isinstance(j, CyanWalker) or isinstance(j, RedWalker)]
                        if occupied:
                            return
                        else:
                            self.model.grid.move_agent(self, self.pointing_at(trace.direction))
                else:
                    self.random_move()
            else:
                print("noised")
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
        if self.previous:
            self.previous.adjust_distance()
