import random
import copy
import time
from base import BaseAgent, TurnData, Action


class State:  
    def __init__(self, map_data, carrying: int, collected_list: list):
        self.map_data = copy.deepcopy(map_data)
        self.carrying = carrying
        self.collected_list = copy.deepcopy(collected_list)
        self.position = [None, None]
    
    def __eq__(self, other):
        if other.map_data != self.map_data:
            return False
        elif other.carrying != self.carrying:
            return False
        elif other.position[0] != self.position[0]:
            return False
        elif other.position[1] != self.position[1]:
            return False
        elif other.collected_list != self.collected_list:
            return False
        
        return True

class Node: 
    def __init__(self, state: State, parent_node, parent_action: Action):
        self.state = state
        self.parent_node = parent_node
        self.parent_action = parent_action
        self.cost = 0
        if(parent_node != None):  # check if this Node is start_node or not
            self.cost = parent_node.cost + 1

class Agent(BaseAgent):

    def __init__(self):
        BaseAgent.__init__(self)
        self.solution_list = []
        self.is_carrying_diamond = False
        self.goal_state = None
        self.elapsed_time = 0
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
        with open("agent-map5", "w") as f:
                f.write(str(self.elapsed_time))
        if action == -1:  # failure
            pass
        else:
            return action


    def breadth_first_search(self, turn_data: TurnData) -> Action:
        """performs breadth first search on problem"""
        current_state = self.transform_turnData_to_state(turn_data)
        frontier = []
        explored_set = []

        if not self.solution_list:  # solution_list is empty
            if  type(current_state.carrying) == type(None):   # in current state, agent is not carrying a diamand
                self.is_carrying_diamond = False
            else:  # in current state, agent is carrying a diamond
                self.is_carrying_diamond = True

            # executing algorithm to find solution to seek diamond
            
            # finding goal state
            self.find_goal_state(current_state.map_data)
            if current_state == self.goal_state:
                return 
            frontier = [Node(state=current_state, parent_node=None, parent_action=None)]
            explored_set = []

            while True:
                first_time = time.perf_counter()
                if not frontier:  # frontier is emtpy
                    return -1
                node = frontier.pop(0)  # chooses the shallowest node in frontier
                explored_set.append(node.state)
                for action in self.actions(node.state):
                    child = self.child_node(node, action)
                    child_is_in_frontier = False
                    for frontier_node in frontier:
                        if child.state == frontier_node.state:  # check if child.state is in frontier
                            child_is_in_frontier = True
                    
                    if not child_is_in_frontier and (child.state not in explored_set):
                        if self.goal_test(child):
                            self.solution(child)
                            first_action = self.solution_list.pop(len(self.solution_list) - 1)
                            return first_action
                        frontier.append(child)  
                second_time = time.perf_counter()
                self.elapsed_time += second_time - first_time
  
        else:  # solution_list is not empty
            # returning an action from solution_list
            return self.solution_list.pop()        

    def find_goal_state(self, current_state_map):
        """
            finds goal state, based on if agent is carrying a diamond
        """
        if self.is_carrying_diamond:  # agent is carrying a diamond, so its goal state is agent with collected diamond
            goal_map = copy.deepcopy(current_state_map)
            self.goal_state.collected_list.append(self.goal_state.carrying)
            goal_state_collected_list = copy.deepcopy(self.goal_state.collected_list)
            self.goal_state = State(goal_map, None, goal_state_collected_list)
        else:  # agent is not carrying a diamond, so its goal state is agent with diamond 
            goal_map = copy.deepcopy(current_state_map)
            for row_index, row in enumerate(goal_map):
                for column_index, column in enumerate(row):
                    if column not in ('a', '.', '*'): 
                        goal_map[row_index][column_index] = '.'
                        self.goal_state = State(goal_map, int(column), [])
                        self.goal_state.position[0] = row_index
                        self.goal_state.position[1] = column_index
                        return
        
    def transform_turnData_to_state(self, turn_data: TurnData) -> State:  
        """
        ransforms turn_data to state
        """
        for item in turn_data.agent_data:
            if item.name == self.name:
                state = State(turn_data.map, item.carrying, item.collected)
                state.position[0] = item.position[0]
                state.position[1] = item.position[1]
                return state

    def goal_test(self, node: Node):
        if self.is_carrying_diamond:
            if node.state.map_data == self.goal_state.map_data:
                if node.state.collected_list == self.goal_state.collected_list:
                    if node.state.carrying == self.goal_state.carrying :  # found a solution
                        return True
        else:
            if node.state == self.goal_state:
                return True
        
        return False

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
    
    def child_node(self, node: Node, action: Action) -> Node:

        state_position = [None, None]
        state_map_data = []
        state_carrying = None
        state_collected_list = []

        if action == Action.UP:  # set position of next state
            state_position[0] = node.state.position[0] - 1
            state_position[1] = node.state.position[1]
        elif action == Action.DOWN:
            state_position[0] = node.state.position[0] + 1
            state_position[1] = node.state.position[1]
        elif action == Action.RIGHT:
            state_position[1] = node.state.position[1] + 1
            state_position[0] = node.state.position[0]
        elif action == Action.LEFT:
            state_position[1] = node.state.position[1] - 1
            state_position[0] = node.state.position[0]
        
        symbol_in_map = node.state.map_data[state_position[0]][state_position[1]]
        if symbol_in_map == '.':  # empty 
            state_map_data = copy.deepcopy(node.state.map_data)
            state_carrying = node.state.carrying
            state_collected_list = copy.deepcopy(node.state.collected_list)
        elif symbol_in_map == 'a':  # agent's base
            state_map_data = copy.deepcopy(node.state.map_data)
            if node.state.carrying != None:  # agent is carrying a diamond
                state_collected_list.append(node.state.carrying)
                state_carrying = None
            else:  # agent is not carrying a diamond
                state_collected_list = copy.deepcopy(node.state.collected_list)
                state_carrying = None
        elif int(symbol_in_map) >= 0:  # some diamond
            if node.state.carrying != None:  # agent is carrying a diamond
                state_map_data = copy.deepcopy(node.state.map_data)
                state_carrying = node.state.carrying
                state_collected_list = copy.deepcopy(node.state.collected_list)
            else:  # agent is not carrying diamond
                state_map_data = copy.deepcopy(node.state.map_data)
                state_carrying = int(symbol_in_map)
                state_map_data[state_position[0]][state_position[1]] = '.'
                state_collected_list = copy.deepcopy(node.state.collected_list)

        child_node_state = State(state_map_data, state_carrying, state_collected_list)
        child_node_state.position[0] = state_position[0]
        child_node_state.position[1] = state_position[1]

        return Node(child_node_state, node, action)

    def solution(self, child: Node):
        while True:
            if child.parent_action != None:
                self.solution_list.append(child.parent_action)
                child = child.parent_node
            else:  # reached to first node
                return



if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
