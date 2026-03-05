import mesa
import random
import networkx as nx



class Walker(mesa.Agent):

    def __init__(self, model, energy):
        super().__init__(model)
        self.energy = energy
        self.active = True


    def step(self):
        stations = self.model.agents_by_type[ChargingStation]
        if self.active  == False:
            print("waiting")
            return
        for station in stations:
            distance = nx.shortest_path_length(self.model.grid.G, self.pos, station.pos)

            if self.energy < distance + 1:
                path = nx.shortest_path(self.model.grid.G, self.pos, station.pos)
                next_node = path[1]  # path[0] is current node
                print(f"Agent {self.unique_id} heading to station! Moving to {next_node}")
            else:
                neighbors = list(self.model.grid.G.neighbors(self.pos))
                next_node = random.choice(neighbors)
                print(f"Agent {self.unique_id} wandering to {next_node}")

            occupants = self.model.grid.get_cell_list_contents([next_node])
            walker_occupants = [a for a in occupants if isinstance(a, Walker)]
            if len(walker_occupants) < self.model.grid.G.nodes[next_node]['capacity']:
                self.model.grid.move_agent(self, next_node)
                self.energy -= 1
            else:
                print(f"Agent {self.unique_id} stopped from wandering to {next_node}")
                



class ChargingStation(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
    
    def step(self):
        occupants = self.model.grid.get_cell_list_contents([self.pos])
        walkers = [a for a in occupants if isinstance(a, Walker)]
        print(f"Station sees {len(walkers)} walkers")
        for walker in walkers:
                walker.active = False
                walker.energy += 5
                print(f"Station charging walker {walker.unique_id} — energy now: {walker.energy}")
                if walker.energy > 20:
                    walker.active = True
                
