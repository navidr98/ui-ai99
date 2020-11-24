import random
import copy
from base import BaseAgent, TurnData, Action


class State:
    def __init__(self):
        self.map_data = []
        self.carrying = None
        self.position = [None, None]
        self.collected_list = []
    
    def __eq__(self, other_state):
        if other_state.map_data != self.map_data:
            return False
        elif other_state.carrying != self.carrying:
            return False
        elif other_state.position[0] != self.position[0]:
            return False
        elif other_state.position[1] != self.position[1]:
            return False
        # elif other_state.collected_list != self.collected_list:
        #     return False
        
        return True


class Node:
    def __init__(self, parent_node = None, action: Action = None, init_state = None):
        self.parent = parent_node
        self.parent_action = action
        self.cost = 0

        if init_state:
            self.state = init_state
        else:
            self.state = State()
            self.deduce_state()

    def deduce_state(self):
        self.cost = self.parent.cost + 1
        """deduces the state that caused by parent_action"""

        if self.parent_action == Action.UP:  # set position of next state
            self.state.position[0] = self.parent.state.position[0] - 1
            self.state.position[1] = self.parent.state.position[1]
        elif self.parent_action == Action.DOWN:
            self.state.position[0] = self.parent.state.position[0] + 1
            self.state.position[1] = self.parent.state.position[1]
        elif self.parent_action == Action.RIGHT:
            self.state.position[1] = self.parent.state.position[1] + 1
            self.state.position[0] = self.parent.state.position[0]
        elif self.parent_action == Action.LEFT:
            self.state.position[1] = self.parent.state.position[1] - 1
            self.state.position[0] = self.parent.state.position[0]
        
        symbol_in_map = self.parent.state.map_data[self.state.position[0]][self.state.position[1]]
        # set map of next state
        if symbol_in_map == '.':  # empty 
            self.state.map_data = copy.deepcopy(self.parent.state.map_data)
            self.state.carrying = self.parent.state.carrying
            self.state.collected_list = copy.deepcopy(self.parent.state.collected_list)
        elif symbol_in_map == 'a':  # agent's base
            self.state.map_data = copy.deepcopy(self.parent.state.map_data)
            if self.parent.state.carrying != None:  # agent is carrying a diamond
                self.state.collected_list.append(self.parent.state.carrying)
                self.state.carrying = None
            else:  # agent is not carrying a diamond
                self.state.collected_list = copy.deepcopy(self.parent.state.collected_list)
                self.state.carrying = None
        elif int(symbol_in_map) >= 0:  # some diamond
            if self.parent.state.carrying != None:  # agent is carrying a diamond
                self.state.map_data = copy.deepcopy(self.parent.state.map_data)
                self.state.carrying = self.parent.state.carrying
                self.state.collected_list = copy.deepcopy(self.parent.state.collected_list)
            else:  # agent is not carrying diamond
                self.state.map_data = copy.deepcopy(self.parent.state.map_data)
                self.state.carrying = int(symbol_in_map)
                self.state.map_data[self.state.position[0]][self.state.position[1]] = '.'
                self.state.collected_list = copy.deepcopy(self.parent.state.collected_list)

    # def __eq__(self, other_node):
    #     if other_node.parent != self.parent:
    #         return False
    #     elif other_node.parent_action != self.parent_action:
    #         return False
    #     elif other_node.state != self.state:
    #         return False
    #     elif other_node.cost != self.cost:
    #         return False
    #     return True

class Agent(BaseAgent):

    def __init__(self):
        BaseAgent.__init__(self)
        self.start_node = None
        self.diamond_state = None
        self.diamond_goal_state = State()
        self.first_goal_state = State()
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

        # returning agent action by calling breadth_first_search(turnData) 
        action = self.breadth_first_search(turn_data)
        if action == -1:  # failure
            pass
        else:
            return action

        # # temporary
        # return random.choice(action)#################


    def breadth_first_search(self, turn_data: TurnData) -> Action:
        """performs breadth first search on problem"""
        current_state = self.transform_turnData_to_state(turn_data)
        frontier = []
        explored_set = []

        if self.is_first_turn:
            self.is_first_turn = False
            self.start_node = Node(init_state=current_state)
            frontier.append(self.start_node)

            # calculating diamond_goal_state and first_goal_state
            self.calculating_first_goal_state()

            while True:
                if not frontier:  # list is empty
                    return -1
                node = frontier.pop(0)  # chooses the shallowest node in frontier
                explored_set.append(node.state)

                for action in self.actions(node.state):
                    child = self.child_node(node, action)
                    if (child.state not in explored_set):
                        child_is_in_frontier = False
                        for item in frontier:  # check if child exists in frontier
                            if item.parent != child.parent:
                                continue
                            elif item.state != child.state:
                                continue
                            elif item.parent_action != child.parent_action:
                                continue
                            elif item.cost != child.cost:
                                continue
                            else:
                                child_is_in_frontier = True

                        if not child_is_in_frontier:  # child is not in frontier
                            if self.goal_test(child.state, from_start=True):  # check if child is goal
                                self.diamond_state = child.state
                                self.solution(child)
                                first_action = self.solution_list.pop(len(self.solution_list) - 1)
                                return first_action

                            frontier.append(child)
        elif current_state == self.diamond_state:
            self.calculating_diamond_goal_state()
            frontier.append(Node(init_state=current_state))
            while True:
                if not frontier:  # list is empty
                    return -1
                node = frontier.pop(0)  # chooses the shallowest node in frontier
                explored_set.append(node.state)

                for action in self.actions(node.state):
                    child = self.child_node(node, action)
                    if (child.state not in explored_set):
                        child_is_in_frontier = False
                        for item in frontier:  # check if child exists in frontier
                            if item.parent != child.parent:
                                continue
                            elif item.state != child.state:
                                continue
                            elif item.parent_action != child.parent_action:
                                continue
                            elif item.cost != child.cost:
                                continue
                            else:
                                child_is_in_frontier = True

                        if not child_is_in_frontier:  # child is not in frontier
                            if self.goal_test(child.state, from_start=False):  # check if child is goal
                                self.solution(child)
                                first_action = self.solution_list.pop(len(self.solution_list) - 1)
                                return first_action

                            frontier.append(child)
            pass
        else:
            return self.solution_list.pop(len(self.solution_list) - 1)

    def calculating_diamond_goal_state(self):
        self.diamond_goal_state.map_data = copy.deepcopy(self.diamond_state.map_data)
        self.diamond_goal_state.carrying = None
        self.diamond_goal_state.collected_list.append(self.diamond_state.carrying)

    def calculating_first_goal_state(self):
        # finding position of diamond in first state
        diamond_position = ()
        for row_index, row in enumerate(self.start_node.state.map_data):
            for column_index, _ in enumerate(row):
                if self.start_node.state.map_data[row_index][column_index] not in ('a', '.', '*'):
                    diamond_position = (row_index, column_index)

        self.first_goal_state.map_data = copy.deepcopy(self.start_node.state.map_data)
        self.first_goal_state.carrying = int(self.first_goal_state.map_data[diamond_position[0]][diamond_position[1]])
        self.first_goal_state.map_data[diamond_position[0]][diamond_position[1]] = '.'
        self.first_goal_state.collected_list = None
        self.first_goal_state.position = diamond_position
        
    def transform_turnData_to_state(self, turn_data: TurnData) -> State:
        """
        ransforms turn_data to state
        """
        state = State()
        state.turns_left = turn_data.turns_left
        for item in turn_data.agent_data:
            if item.name == self.name:
                state.carrying = item.carrying
                state.position[0] = item.position[0]
                state.position[1] = item.position[1]
                state.collected_list = item.collected

        state.map_data = turn_data.map

        return state

    def goal_test(self, child_state: State, from_start: bool):
        if from_start:
            if child_state == self.first_goal_state:
                return True
            else:
                return False
        else:  # check if child_state is equal to diamond_goal_state
            if child_state.collected_list != self.diamond_goal_state.collected_list:
                return False
            elif child_state.carrying != None:
                return False
            elif child_state.map_data != self.diamond_goal_state.map_data:
                return False
            return True

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
    
    def child_node(self, parent : Node, action: Action) -> Node:
        """creates a child node with provided parameter"""
        child_node = Node(parent, action)
        return child_node

    def solution(self, child: Node):
        while True:
            if child.parent_action != None:
                self.solution_list.append(child.parent_action)
                child = child.parent
            else:
                return

    def print_map(self, inp):
        for row in inp:
            for column in row:
                print(column, end='')
            print()

    def print_node(self, node: Node):
        print("\nprinting node: ", node)
        print("parent node: ", node.parent)
        print("parent action: ", node.parent_action)
        print("map: ")
        self.print_map(node.state.map_data)
        print(node.state.position)
        print(node.state.carrying)
        print(node.state.collected_list)

    def print_state(self, state: State):
        self.print_map(state.map_data)
        print(state.position)
        print(state.carrying)
        print(state.collected_list)



if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
