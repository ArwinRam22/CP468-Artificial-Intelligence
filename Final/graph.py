import random

class graph:
    def __init__(self) -> None:
        self.locations = []
        self.count = 0

    def get_locations(self):
        return self.locations
        
    def get_count(self):
        return self.count
        
    def get_random_location(self):
        """
        Get a random location
        Parameters:
            -
        Returns:
            (location) = random location
        """
        return random.choice(self.get_locations())
    
    def get_location(self, find_name):
        """
        Get a location by name
        Params:
            (str) = Name to search for
        Returns:
            (location) = location with specified name
            None = location not found
        """
        for i in self.locations:
            if (find_name == i.get_name()):
                return i
        return None
    
    def add_location(self, location_to_add):
        """
        Add a new location to graph
        Params:
            (location) = new location
        Returns:
            (boolean) = true if location is added, false if it already exists
        """
        if location_to_add not in self.locations:
            self.locations.append(location_to_add)
            self.count = self.count + 1
            return True
        else:
            print(f'{location_to_add} already exists in graph')
            return False

    def depth_first_search(self, start, finish):
        """
        Depth-first search from start to finish
        Parameters
            (String) = name of starting location
            (String) = name of destination location
        Returns
            (List) = path of locations leading to destination
            (int) = cost to travel using path
        """
        start_location = self.get_location(start.get_name())
        finish_location = self.get_location(finish.get_name())
        if start_location is None:
            print(f"Error #1: Starting location ({start}) not in graph.")
            return [], 0
        if finish_location is None:
            print(f"Error #2: Ending location ({finish}) not in graph.")
            return [], 0
        
        path, cost = self.depth_first_search_aux(start_location, finish_location, [], [], 0)

        return path, cost

    def depth_first_search_aux(self, current, finish, explored, path, cost):
        """
        depth_first_search auxiliary method
        Parameters
            (location) = current location
            (location) = destination location
            (List) = explored locations
            (List) = current path from start
            (int) = cost to travel with current path
        Returns
            (List) = path of locations leading to destination
            (int) = cost to travel using path
        """
        bestPath = []
        bestCost = -1
        if current.get_name() == finish.get_name():
            path.append(current)
            return path, cost
        
        neighbors = current.get_neighbors()
        for n in neighbors:
            if n not in explored:
                current_neighbor = self.get_location(n)
                temp_cost = current.get_travel_cost(current_neighbor)
                newPath, newCost = self.depth_first_search_aux(current_neighbor, finish, explored+[current.get_name()], path+[current], cost+temp_cost)
                if newPath != []:
                    if bestPath == [] or newCost < bestCost:
                        bestPath = newPath
                        bestCost = newCost

        return bestPath, bestCost

    def set_q_values(self, new_q_value):
            """
            Change all q-values to the same value
            Params:
                (int) = new q-value
            Returns:
                (boolean) = true if q-values are changed
            """
            for i in self.locations:
                i.set_q_value(new_q_value)
            return True
    
    def is_terminal_state(self, current_location, terminal):
        """
        Determines if the current location is the destination or a dead-end
        Params:
            (location) = Current location
            (location) = Destination
        Returns:
            (int) 1 = Current location is destination
            (int) 0 = Current location has neighbors and is not destination
            (int) -1 = Current location has no neighbors
        """
        if current_location.get_name() == terminal.get_name():
            return 1
        elif len(current_location.get_neighbors()) == 0:
            return -1
        return 0

    def get_next_location(self, current_location, terminal, epsilon):
        """
        Epsilon greedy algorithm that chooses action (which neighbor node to travel to)
        Params:
            (graph) = graph holding information of all nodes
            (dict) = Dictionary holding q-values
            (location) = current location
            (int) = epsilon
        Returns:
            (tuple[location, int]) = Neighbor node of current location, cost to travel
            None = when no neighbor nodes are present
        """
        next_location = None
        cost = 0
        
        if random.random() < epsilon:
            # Choose best path
            next_location, cost = self.get_lowest_q_value(current_location, terminal)

        elif current_location is not None:
            # Choose random path
            max = len(current_location.get_neighbor_names())-1
            if max >= 0:
                random_index = random.randint(0, max)
                neighbor_list = list(current_location.get_neighbor_names())
                random_neighbor = neighbor_list[random_index]
                next_location = self.get_location(random_neighbor)
                cost = current_location.get_travel_cost(next_location)

        return next_location, cost

    def get_lowest_q_value(self, current_location, terminal):
        """
        Determines lowest q-value of neighbor nodes from current location
        Params:
            (location) = current location
        Returns:
            (tuple[location, int]) = Neighbor node with lowest q-value of current location, cost to travel
            (tuple[None, int]) = when no neighbor nodes are present
        """
        min = 10000
        neighbor_dict = current_location.get_neighbors()
        cost = 0
        lowest_location = None
        if self.is_terminal_state(current_location, terminal) == 0:
            for x in neighbor_dict:
                neighbor = self.get_location(x)
                newCost = current_location.get_travel_cost(neighbor)
                compare = neighbor.get_q_value()
                if min > compare or cost == 0 or (min == compare and cost > newCost):
                    lowest_location = neighbor
                    cost = newCost
                    min = compare 
        elif self.is_terminal_state(current_location, terminal) == 1:
            lowest_location = current_location
            cost = 0

        return lowest_location, cost
    
    def q_learning(self, terminal):
        """
        Determines q-values for all locations depending on the destination node
        Params:
            (location) = destination
        Returns:
            (graph) = graph holding updated information of all nodes
        """
        EPSILON = 0.9
        DISCOUNT = 0.9
        LEARNING_RATE = 0.3
        EPISODES = 10000
        self.set_q_values(100)
        terminal.set_q_value(0)

        for e in range(EPISODES):
            # Choose random starting non-terminal location
            current_loc = self.get_random_location()
            if terminal is not None:
                while self.is_terminal_state(current_loc, terminal) != 0:
                    current_loc = self.get_random_location()

            while self.is_terminal_state(current_loc, terminal) == 0:
                # Choose action - choose next location to travel to
                next_loc, travel_cost = self.get_next_location(current_loc, terminal, EPSILON)
                if next_loc is None:
                    break

                # Determine q-value of next location 
                    # Get lowest q-value of neighbors of next location
                    # if no neighbors, get q-value of next location
                min_q_value_neighbor, cost = self.get_lowest_q_value(current_loc, terminal)
                if min_q_value_neighbor is not None:
                    min_q_value = min_q_value_neighbor.get_q_value()
                else:
                    min_q_value = next_loc.get_q_value()

                # Update q-values of current location
                new_q_value = current_loc.get_q_value() + LEARNING_RATE * ((travel_cost*2) + (DISCOUNT * min_q_value) - current_loc.get_q_value())
                current_loc.set_q_value(new_q_value)

                # Transition states
                current_loc = next_loc

        return

    def get_shortest_path(self, start, finish):
        """
        Determines shortest path from a starting location to 
        a destination location using q-values
        Params:
            (location) = current location
            (location) = destination
        Returns:
            (list) = list of nodes representing shortest path
        """

        LIMIT = 25
        EPSILON = 1
        shortest_path = []
        smallest_cost = 0

        if self.is_terminal_state(start, finish) != 1:
            current_loc = start
            max_count = 0
            while self.is_terminal_state(current_loc, finish) != 1 and max_count <= LIMIT:
                shortest_path.append(current_loc)
                next_loc, cost = self.get_next_location(current_loc, finish, EPSILON)
                if next_loc is not None:
                    smallest_cost = cost + smallest_cost
                    current_loc = next_loc
                max_count = max_count + 1
            if self.is_terminal_state(current_loc, finish) == 1:
                shortest_path.append(current_loc)
            else:
                shortest_path = []
                smallest_cost = -1

        return shortest_path, smallest_cost