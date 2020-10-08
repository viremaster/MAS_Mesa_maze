from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import CyanWalker, RedWalker
from .schedule import RandomActivationByColour


class WalkerModel(Model):
    """
    Walking model
    """

    height = 20
    width = 20

    initial_cyan_walkers = 10
    initial_red_walkers = 10

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating random walkers."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_cyan_walkers=10,
        initial_red_walkers=10,
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
                "Cyan Walkers": lambda m: m.schedule.get_colour_count(CyanWalker),
                "Red Walkers": lambda m: m.schedule.get_colour_count(RedWalker),
            }
        )

        # Create walkers:
        for i in range(self.initial_cyan_walkers):
            x = self.random.randrange(0, self.width - 13)
            y = self.random.randrange(0, self.height - 10)
            walker = CyanWalker(self.next_id(), (x, y), self, True)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

        for i in range(self.initial_red_walkers):
            x = self.random.randrange(0, self.width - 13)
            y = self.random.randrange(self.height - 10, self.height)
            walker = RedWalker(self.next_id(), (x, y), self, True)
            self.grid.place_agent(walker, (x, y))
            self.schedule.add(walker)

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
