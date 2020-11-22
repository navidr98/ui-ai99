import random
from base import BaseAgent, TurnData, Action


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
        action_name = input("> ").upper()
        if action_name == "U":
            return Action.UP
        if action_name == "D":
            return Action.DOWN
        if action_name == "L":
            return Action.LEFT
        if action_name == "R":
            return Action.RIGHT
        return random.choice(list(Action))

    def breadth_first_search(self):
        pass

    def pop(self):
        pass

    def insert(self):
        pass

    def goal_test(self, child_state: State):
        pass


if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
