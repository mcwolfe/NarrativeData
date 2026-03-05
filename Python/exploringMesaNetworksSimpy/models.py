import mesa
import random
import networkx as nx
from agents import Walker, ChargingStation


class MyModel(mesa.Model):
    def __init__(self, G):
        super().__init__()
        self.grid = mesa.space.NetworkGrid(G)
        for i in range(10):
            walker = Walker(self, energy=random.randint(5, 15))
            node = random.choice(list(G.nodes()))
            self.grid.place_agent(walker, node)
        station = ChargingStation(self)
        self.grid.place_agent(station, 20)

    def step(self):
        self.agents_by_type[Walker].do("step")
        self.agents_by_type[ChargingStation].do("step")


