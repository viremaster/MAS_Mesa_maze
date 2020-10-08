from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .agents import CyanWalker, RedWalker
from .model import WalkerModel


def walker_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is CyanWalker:
        portrayal["Shape"] = "Model/resources/Cyan.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    if type(agent) is RedWalker:
        portrayal["Shape"] = "Model/resources/Red.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal


canvas_element = CanvasGrid(walker_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Cyan Walkers", "Color": "#00FFFF"}, {"Label": "Red Walkers", "Color": "#AA0000"}]
)

model_params = {
    "initial_cyan_walkers": UserSettableParameter(
        "slider", "Initial cyan walkers", 10, 1, 50
    ),
    "initial_red_walkers": UserSettableParameter(
        "slider", "Initial red walkers", 10, 1, 50
    ),
}

server = ModularServer(
    WalkerModel, [canvas_element, chart_element], "Walking", model_params
)
server.port = 8521
