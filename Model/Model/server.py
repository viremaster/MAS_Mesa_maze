from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .static_objects import Finish, Wall, RedObstacle, CyanObstacle
from .model import WalkerModel
from .efficient_agents import RedWalker, CyanWalker


def walker_portrayal(agent):
    """
    Gives a portrayal of every agent.
    """

    if agent is None:
        return

    portrayal = {}

    if type(agent) is CyanWalker:
        portrayal["Shape"] = "Model/resources/Cyan.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is RedWalker:
        portrayal["Shape"] = "Model/resources/Red.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Finish:
        portrayal["Color"] = ["#008800"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Wall:
        portrayal["Color"] = ["#808080"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is RedObstacle:
        portrayal["Color"] = ["#AA0000"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is CyanObstacle:
        portrayal["Color"] = ["#00FFFF"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(walker_portrayal, 30, 30, 500, 500)
chart_element = ChartModule(
    [{"Label": "Finished Cyan Walkers", "Color": "#00FFFF"}, {"Label": "Finished Red Walkers", "Color": "#AA0000"}]
)

model_params = {
    "initial_cyan_walkers": UserSettableParameter(
        "slider", "Initial cyan walkers", 50, 1, 50
    ),
    "initial_red_walkers": UserSettableParameter(
        "slider", "Initial red walkers", 50, 1, 50
    ),
    "cyan_noise": UserSettableParameter(
        "slider", "Cyan walker noise", 0, 0, 100
    ),
    "red_noise": UserSettableParameter(
        "slider", "Red walker noise", 0, 0, 100
    ),
    "cyan_box_drop_chance": UserSettableParameter(
        "slider", "Cyan box drop chance", 10, 0, 100
    ),
    "cyan_box_duration": UserSettableParameter(
        "slider", "Cyan box duration", 10, 0, 100
    ),
    "cyan_box_amount": UserSettableParameter(
        "slider", "Cyan box amount", 20, 0, 20
    ),
    "red_box_drop_chance": UserSettableParameter(
        "slider", "Red box drop chance", 10, 0, 100
    ),
    "red_box_duration": UserSettableParameter(
        "slider", "Red box duration", 10, 0, 100
    ),
    "red_box_amount": UserSettableParameter(
        "slider", "Red box amount", 20, 0, 20
    ),

}

server = ModularServer(
    WalkerModel, [canvas_element, chart_element], "Walking", model_params
)
server.port = 8521
