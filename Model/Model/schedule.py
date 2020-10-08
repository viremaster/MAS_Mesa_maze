from collections import defaultdict

from mesa.time import RandomActivation


class RandomActivationByColour(RandomActivation):
    """
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    """

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_colour = defaultdict(dict)

    def add(self, agent):
        """
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        """

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_colour[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        """
        Remove all instances of a given agent from the schedule.
        """

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_colour[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        """
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        """
        if by_breed:
            for agent_class in self.agents_by_colour:
                self.step_colour(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_colour(self, colour):
        """
        Shuffle order and run all agents of a given breed.

        Args:
            colour: Class object of the colour to run.
        """
        agent_keys = list(self.agents_by_colour[colour].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_colour[colour][agent_key].step()

    def get_colour_count(self, colour_class):
        """
        Returns the current number of agents of certain breed in the queue.
        """
        return len(self.agents_by_colour[colour_class].values())

    def get_finished_count(self, colour_class):
        finished = 0
        agent_keys = list(self.agents_by_colour[colour_class].keys())
        for agent_key in agent_keys:
            if self.agents_by_colour[colour_class][agent_key].finished:
                finished += 1
        return finished
