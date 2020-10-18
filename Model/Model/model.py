from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import Finish, Wall
from .schedule import RandomActivationByColour
from .efficient_agents import CyanWalker, RedWalker, TraceTracker


class WalkerModel(Model):
    """
    Walking model
    """

    height = 30
    width = 30

    initial_cyan_walkers = 10
    initial_red_walkers = 10

    cyan_noise = 0
    red_noise = 0

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating random walkers."
    )

    def __init__(
        self,
        height=30,
        width=30,
        initial_cyan_walkers=10,
        initial_red_walkers=10,
        cyan_noise=0,
        red_noise=0
    ):
        """
        Create a new walker model with the given parameters.

        Args:
            initial_cyan_walkers: Number of cyan walkers to start with
            initial_red_walkers: Number of red walkers to start with
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_cyan_walkers = initial_cyan_walkers
        self.initial_red_walkers = initial_red_walkers

        self.schedule = RandomActivationByColour(self)
        self.grid = MultiGrid(self.height, self.width, torus=False)
        self.datacollector = DataCollector(
            {
                "Finished Cyan Walkers": lambda m: m.schedule.get_finished_count(CyanWalker),
                "Finished Red Walkers": lambda m: m.schedule.get_finished_count(RedWalker),
            }
        )

        # Create walls:
        wallsX = [4, 10, 12, 13, 14, 17, 18, 23, 24, 25, 28,
                  4, 5, 6, 8, 14, 16, 20, 24, 28,
                  4, 8, 9, 10, 12, 14, 16, 17, 18, 19, 20, 21, 24, 26, 27, 28,
                  6, 8, 10, 12, 13, 14, 18, 20, 21, 24,
                  4, 6, 16, 18, 27,
                  4, 6, 8, 10, 11, 13, 14, 16, 20, 23, 25, 27,
                  4, 11, 12, 13, 17, 18, 20, 21, 22, 23, 27, 28, 29,
                  4, 9, 12, 15, 20, 26, 27,
                  6, 7, 8, 9, 12, 13, 14, 15, 17, 18, 22, 23, 24,
                  8, 14, 18, 22, 24, 28,
                  4, 8, 9, 11, 16, 20, 22, 24, 25, 28,
                  4, 6, 11, 12, 13, 14, 16, 17, 24, 27, 28, 29,
                  4, 5, 6, 8, 9, 10, 11, 17, 18, 19, 21, 22, 23, 24,
                  1, 2, 8, 14, 21, 26,
                  2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26, 27,
                  2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 19, 20, 21, 22, 24, 25, 26, 27,
                  1, 2, 8, 14, 21, 26,
                  4, 5, 6, 8, 9, 10, 11, 17, 18, 19, 21, 22, 23, 24,
                  4, 6, 11, 12, 13, 14, 16, 17, 24, 27, 28, 29,
                  4, 8, 9, 11, 16, 20, 22, 24, 25, 28,
                  8, 14, 18, 22, 24, 28,
                  6, 7, 8, 9, 12, 13, 14, 15, 17, 18, 22, 23, 24,
                  4, 9, 12, 15, 20, 26, 27,
                  4, 11, 12, 13, 17, 18, 20, 21, 22, 23, 27, 28, 29,
                  4, 6, 8, 10, 11, 13, 14, 16, 20, 23, 25, 27,
                  4, 6, 16, 18, 27,
                  6, 8, 10, 12, 13, 14, 18, 20, 21, 24,
                  4, 8, 9, 10, 12, 14, 16, 17, 18, 19, 20, 21, 24, 26, 27, 28,
                  4, 5, 6, 8, 14, 16, 20, 24, 28,
                  4, 10, 12, 13, 14, 17, 18, 23, 24, 25, 28]

        wallsY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                  3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                  4, 4, 4, 4, 4,
                  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                  7, 7, 7, 7, 7, 7, 7,
                  8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                  9, 9, 9, 9, 9, 9,
                  10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                  11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
                  12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                  13, 13, 13, 13, 13, 13,
                  14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
                  15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                  16, 16, 16, 16, 16, 16,
                  17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
                  18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                  19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
                  20, 20, 20, 20, 20, 20,
                  21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
                  22, 22, 22, 22, 22, 22, 22,
                  23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23,
                  24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24,
                  25, 25, 25, 25, 25,
                  26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
                  27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27,
                  28, 28, 28, 28, 28, 28, 28, 28, 28,
                  29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29]

        # wallsX = [2,3]
        # wallsY = [5,6]

        for i in range(0, len(wallsX)):
            xcor = wallsX[i]
            ycor = wallsY[i]
            # x = self.random.randrange(0, self.width)
            # y = self.random.randrange(0, self.height)
            wall = Wall(self.next_id(), (xcor, ycor), self)
            self.grid.place_agent(wall, (xcor, ycor))

        # For each Cyan walker
        cyan_tracker = TraceTracker()
        for i in range(self.initial_cyan_walkers):
            # Pick a random spot (Within the boundary)
            x = self.random.randrange(0, 4)
            y = self.random.randrange(17, 30)

            # Check if it is occupied by another CyanWalker
            occupied = False
            for j in self.grid[x][y]:
                if type(j) == CyanWalker:
                    occupied = True

            # While the spot is occupied
            while occupied:
                # Pick a random spot (Within the boundary)
                x = self.random.randrange(0, 4)
                y = self.random.randrange(17, 30)

                # Check if it is occupied by another CyanWalker
                occupied = False
                for j in self.grid[x][y]:
                    if type(j) == CyanWalker:
                        occupied = True

            # Make the walker and place it on the grid and the schedule
            walker = CyanWalker(self.next_id(), (x, y), self, cyan_tracker, False, cyan_noise)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

        # The red walkers work in the same fashion as the Cyan walkers
        red_tracker = TraceTracker()
        for i in range(self.initial_red_walkers):
            x = self.random.randrange(0, 4)
            y = self.random.randrange(0, 13)

            occupied = False
            for j in self.grid[x][y]:
                if type(j) == RedWalker:
                    occupied = True

            while occupied:
                x = self.random.randrange(0, 4)
                y = self.random.randrange(0, 13)

                occupied = False
                for j in self.grid[x][y]:
                    if type(j) == RedWalker:
                        occupied = True

            walker = RedWalker(self.next_id(), (x, y), self, red_tracker, False, red_noise)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

        # In all x's and y's in the range.
        for x in range(28, 30):
            for y in range(14, 16):
                # Add a finish agent
                finish = Finish(self.next_id(), (x, y), self)
                self.grid.place_agent(finish, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_colour_count(CyanWalker),
                    self.schedule.get_colour_count(RedWalker),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number of cyan walkers: ", self.schedule.get_colour_count(CyanWalker))
            print("Initial number of red walkers: ", self.schedule.get_colour_count(RedWalker))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number cyan walkers: ", self.schedule.get_colour_count(CyanWalker))
            print("Final number red walkers: ", self.schedule.get_colour_count(RedWalker))
