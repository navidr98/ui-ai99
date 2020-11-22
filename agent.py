import random
from base import BaseAgent, TurnData, Action
from base import read_utf, write_utf


class State:
    def __init__(self):
        self.map = None
        self.carrying = False


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
        self.is_first_turn = False
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
        return Action.DOWN

    def transform_turnData_to_state(self, turn_data: TurnData) -> State:
        """
        ransforms turn_data to state
        """
        return None

    def breadth_first_search(self, turn_data: TurnData):
        """performs breadth first search on problem"""
        current_state = self.transform_turnData_to_state(turn_data)
        frontier = []
        explored_set = {}

        if self.is_first_turn:
            self.start_state = current_state
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
        

    def pop(self):
        pass

    def insert(self):
        pass

    def goal_test(self, child_state: State, goal_state: State):
        pass

    def actions(self, state: State):
        pass

    




if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
