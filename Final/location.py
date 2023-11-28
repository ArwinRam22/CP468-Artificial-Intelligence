class location:
    def __init__(self, name) -> None:
        self.name = name
        self.neighbors = {}
        self.q_value = 0
        self.neighbor_q_values = {}
    def __str__(self) -> str:
        return (f"{self.name} (Q: {round(self.get_q_value(), 2)}): {self.get_neighbors()}")

    def set_q_value(self, new_q_value):
        self.q_value = new_q_value
        return True
    
    def get_name(self):
        return self.name
    def get_neighbors(self):
        return self.neighbors
    def get_neighbor_names(self):
        return self.neighbors.keys()
    def get_q_value(self):
        return self.q_value
    def get_neighbor_q_values(self):
        return self.neighbor_q_values
        
    def get_travel_cost(self, next_location):
        """
        Gets cost to travel from self to neighboring location
        Parameters
            (location) = neighboring location
        Returns
            (int) = cost to travel to neighboring location from current location
        """
        if self.neighbors.get(next_location.get_name()):
            return self.neighbors[next_location.get_name()]
        else:
            print(f"{next_location.get_name()} is not a neighbor to {self.get_name()}.")
        return 0
    
    def add_neighbor(self, new_neighbor, new_neighbor_cost):
        """
        Add a new neighbor to location
        Parameters
            (location) = new neighbor
            (int) = cost to travel to new neighbor
        Returns
            (boolean) = True if added, false if already a neighbor
        """
        if not self.neighbors.get(new_neighbor.get_name()):
            self.neighbors.update({new_neighbor.get_name(): new_neighbor_cost})
            return True
        else:
            print(f"{new_neighbor.get_name()} is already a neighbor to {self.get_name()}.")
            return False
        
    def update_neighbor(self, neighbor, cost):
        """
        Update cost to travel to neighbor location
        Parameters
            (location) = existing neighbor
            (int) = cost to travel to new neighbor
        Return
            (boolean) = true if updated, false if neighbor is not a neighbor
        """
        if self.neighbors.get(neighbor.get_name()):
            self.neighbors.update({neighbor.get_name(): cost})
            return True
        else:
            print(f"{neighbor.get_name()} is not a neighbor to {self.get_name()}.")
            return False
