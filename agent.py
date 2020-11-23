import random
from base import BaseAgent, TurnData, Action


class State:
    def __init__(self):
        self.map_data = []
        self.carrying = None
        self.turns_left = None
        self.position = ()
        self.collected_list = []


class Node:
    def __init__(self, parent_node: State = None, parent_action: Action = None):
        self.parent_node = parent_node
        self.parent_action = parent_action
        self.state = None
        self.cost = 0

    def deduce_state(self):
        """deduces the state that caused by parent_action"""
        pass

    def calculate_cost(self):
        """adds the cost of parent_action to parent_node.cost"""
        pass



class Agent(BaseAgent):

    def __init__(self):
        BaseAgent.__init__(self)
        self.start_state = None
        self.diamond_state = None
        self.is_first_turn = True
        self.solution_list = []
        print(f"MY NAME: {self.name}")
        print(f"PLAYER COUNT: {self.agent_count}")
        print(f"GRID SIZE: {self.grid_size}")
        print(f"MAX TURNS: {self.max_turns}")
        print(f"DECISION TIME LIMIT: {self.decision_time_limit}")


    def do_turn(self, turn_data: TurnData) -> Action:
        print(f"TURN {self.max_turns - turn_data.turns_left}/{self.max_turns}")
        for agent in turn_data.agent_data:
            print(f"AGENT {agent.name}")
            print(f"POSITION: {agent.position}")
            print(f"CARRYING: {agent.carrying}")
            print(f"COLLECTED: {agent.collected}")
        for row in turn_data.map:
            print(''.join(row))

        action = self.breadth_first_search(turn_data)
        # returning agent action by calling breadth_first_search(turnData) 

        # temporary
        return Action.RIGHT


    def breadth_first_search(self, turn_data: TurnData) -> Action:
        """performs breadth first search on problem"""
        current_state = self.transform_turnData_to_state(turn_data)
        x = self.actions(current_state)
        print(x)
        return None ##################################################3
        frontier = []
        explored_set = {}

        if self.is_first_turn:
            self.start_state = current_state
            self.is_first_turn = False
        elif current_state == self.start_state:
            # first creating relative goal state
            # do searching diamond state
            # creating solution_list actions
            pass
        elif current_state == self.diamond_state:
            # first creating relative final goal state
            # do searching for final goal
            # creating solution_list actions
            pass
        else:
            # simply returning an action from solution_list
            pass
    

    def transform_turnData_to_state(self, turn_data: TurnData) -> State:
        """
        ransforms turn_data to state
        """
        state = State()
        state.turns_left = turn_data.turns_left
        for item in turn_data.agent_data:
            if item.name == self.name:
                state.carrying = item.carrying
                state.position = item.position
                state.collected_list = item.collected

        state.map_data = turn_data.map

        return state

    def pop(self):
        pass

    def insert(self):
        pass

    def goal_test(self, child_state: State, goal_state: State):
        pass

    def actions(self, state: State) -> list:
        """returns list of possible actions"""
        possible_actions = []
        rows = len(state.map_data)
        columns = len(state.map_data[0])
        x = state.position[0]
        y = state.position[1]

        up_position = x - 1
        if up_position >= 0 :  # up is not boundary
            if state.map_data[up_position][y] != '*':  # there is no wall upside
                possible_actions.append(Action.UP)
        
        down_position = x + 1
        if down_position != rows:  # down is not boundary
            if state.map_data[down_position][y] != '*':  # there is no wall downside
                possible_actions.append(Action.DOWN)

        left_position = y - 1
        if left_position >= 0 :  # left is not boundary
            if state.map_data[x][left_position] != '*':  # there is no wall leftside
                possible_actions.append(Action.LEFT)

        right_position = y + 1
        if right_position != columns :  # right is not boundary
            if state.map_data[x][right_position] != '*':  # there is no wall rightside
                possible_actions.append(Action.RIGHT)

        return possible_actions
    
    def child_node(self, state: State, action: Action, parent_cost: int) -> Node:
        



if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
