from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .agents import CyanWalker, RedWalker, Finish, Wall, Trace, ArrowTrace, RedObstacle, CyanObstacle
from .model import WalkerModel


def walker_portrayal(agent):
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

    elif type(agent) is Trace:
        portrayal["Color"] = [agent.colour]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is ArrowTrace:
        portrayal["Shape"] = agent.sprite()
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
    return portrayal


canvas_element = CanvasGrid(walker_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Finished Cyan Walkers", "Color": "#00FFFF"}, {"Label": "Finished Red Walkers", "Color": "#AA0000"}]
)

model_params = {
    "initial_cyan_walkers": UserSettableParameter(
        "slider", "Initial cyan walkers", 10, 1, 50
    ),
    "initial_red_walkers": UserSettableParameter(
        "slider", "Initial red walkers", 10, 1, 50
    ),
    "initial_walls": UserSettableParameter(
        "slider", "Number of wall elements", 200, 1, 400
    )
}


server = ModularServer(
    WalkerModel, [canvas_element, chart_element], "Walking", model_params
)
server.port = 8521
