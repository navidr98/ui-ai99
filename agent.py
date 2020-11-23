import random
from base import BaseAgent, TurnData, Action


class State:
    def __init__(self):
        self.map_data = []
        self.carrying = None
        self.position = ()
        self.collected_list = []
    
    def __eq__(self, other_state):
        if other_state.map_data != self.map_data:
            return False
        elif other_state.carrying != self.carrying:
            return False
        elif other_state.position != self.position:
            return False
        elif other_state.collected_list != self.collected_list:
            return False
        
        return True


class Node:
    def __init__(self, parent_node = None, action: Action = None, init_state = None):
        self.parent = parent_node
        self.parent_action = action
        self.cost = 0

        if init_state == None:
            self.state = State()
            self.deduce_state()
        else:
            self.state = init_state

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
            self.state.map_data = self.parent.state.map_data[:]
            self.state.carrying = self.parent.state.carrying
            self.state.collected_list = self.parent.state.collected_list[:]
        elif symbol_in_map == 'a':  # agent's base
            self.state.map_data = self.parent.state.map_data[:]
            if self.parent.state.carrying != None:  # agent is carrying a diamond
                self.state.collected_list.append(self.parent.state.carrying)
                self.state.carrying = None
            else:  # agent is not carrying a diamond
                self.state.collected_list = self.parent.state.collected_list[:]
                self.state.carrying = None
        elif int(symbol_in_map) >= 0:  # some diamond
            if self.parent.state.carrying != None:  # agent is carrying a diamond
                self.state.map_data = self.parent.state.map_data[:]
                self.state.carrying = self.parent.state.carrying
                self.state.collected_list = self.parent.state.collected_list[:]
            else:  # agent is not carrying diamond
                self.state.map_data = self.parent.state.map_data[:]
                self.state.carrying = int(symbol_in_map)
                self.state.map_data[self.state.position[0]][self.state.position[1]] = '.'
                self.state.collected_list = self.parent.state.collected_list[:]

    def __eq__(self, other_node):
        if other_node.parent != self.parent:
            return False
        elif other_node.parent_action != self.parent:
            return False
        elif other_node.state != self.state:
            return False
        elif other_node.cost != self.cost:
            return False
        return True

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

        action = self.breadth_first_search(turn_data)
        # returning agent action by calling breadth_first_search(turnData) 

        # temporary
        return random.choice(action)


    def breadth_first_search(self, turn_data: TurnData) -> Action:
        """performs breadth first search on problem"""
        current_state = self.transform_turnData_to_state(turn_data)
       
        # possible_actions = self.actions(current_state) ##########################
        # for action in possible_actions:##############################3
        #     child = self.child_node(parent=self.start_node, action=action)#####################
        #     with open("test-child-node", "a") as f:
        #         f.write("\n\n###############################")
        #         f.write("\nmap: " + str(child.state.map_data))
        #         f.write("\ncarrying: " +  str(child.state.carrying))
        #         f.write("\ncollected_list: " +  str(child.state.collected_list))
        #         f.write("\npostion: " + str(child.state.position))
        #         f.write("\ncost: " + str(child.cost))
        #         f.write("################################")
        # return possible_actions ##################################################3
        frontier = []
        explored_set = []

        if self.is_first_turn:
            self.start_node = Node(init_state=current_state)
            frontier.append(self.start_node)
            # calculating diamond_goal_state and first_goal_state
            self.calculating_first_goal_state()

            self.is_first_turn = False

            while True:
                if not frontier:  # list is empty
                    return -1
                node = frontier.pop(0)  # chooses the shallowest node in frontier
                explored_set.append(node.state)

                for action in self.actions(node.state):
                    child = self.child_node(node, action)
                    if (child.state not in explored_set) and (child not in frontier):
                        if self.goal_test(child.state, True):
                            # save solution to solution_list
                            # save first action of the solution list
                            # update solution list
                            # return first action
                            return self.solution(child, )##################################

                        frontier.append(child)
                        

                        

                    
            # first creating relative goal state
            # do searching diamond state
            # creating solution_list actions
        elif current_state == self.diamond_state:
            # first creating relative final goal state
            # do searching for final goal
            # creating solution_list actions
            pass
        else:
            # simply returning an action from solution_list
            pass
    
    def calculating_first_goal_state(self):
        # finding position of diamond in first state
        diamond_position = ()
        for row in self.start_node.state.map_data:
            for column in row:
                if self.start_node.state.map_data[row][column] not in ('a', '.', '*'):
                    diamond_position = (row, column)
        
        self.first_goal_state.map_data = self.start_node.state.map_data[:]
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
                state.position = item.position
                state.collected_list = item.collected

        state.map_data = turn_data.map

        return state

    def goal_test(self, child_state: State, from_start: bool):
        if from_start:
            if child_state == self.first_goal_state:
                return True
            else:
                return False
        else:
            pass
        return None

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
        return None
        


        



if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)
