import heapq
import math


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for i, v in enumerate(from_state):
        for j, m in enumerate(to_state):
            if v == 0 or m == 0:
                continue
            if v == m:
                distance += manhattan_distance(i, j)

    return distance

def index_to_coord(index):
    y = math.floor(index/3)
    x = index - 3*y
    return (x, y)

def manhattan_distance(i, j):
    x1, y1 = index_to_coord(i)
    x2, y2 = index_to_coord(j)
    return abs(x1 - x2) + abs(y1 - y2)


def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    for i, v in enumerate(state):
        if v == 0:
            if (i - 3) >= 0 and state[i-3] != 0: # up
                new_state = state.copy()
                succ_states.append(new_state)
                swap_index(new_state, i, i-3) 
            if (i + 3) < 9 and state[i+3] != 0: # down
                new_state = state.copy()
                swap_index(new_state, i, i+3)
                succ_states.append(new_state)
            if i%3 != 0 and state[i-1] != 0: # left
                new_state = state.copy()
                swap_index(new_state, i, i-1)
                succ_states.append(new_state)
            if i%3 != 2 and state[i+1] != 0: # right
                new_state = state.copy()
                swap_index(new_state, i, i+1)
                succ_states.append(new_state)
   
    return sorted(succ_states)

def swap_index(state, i, j):
    tmp = state[i]
    state[i] = state[j]
    state[j] = tmp

def max(a, b):
    return a if a > b else b


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    max_length = 0
    queue_length = 0

    open = []
    closed = []

    g = 0
    h = get_manhattan_distance(state, goal_state)
    f = g + h
    parent_index = -1
    heapq.heappush(open,(f, state, (g, h, parent_index)))
    queue_length += 1
    max_length = max(max_length, queue_length)

    while (True):
        if (not open):
            print("ERROR")
        n = heapq.heappop(open)
        queue_length -= 1
        # closed.append(n)
        closed_index = -1
        for i, item in enumerate(closed):
                if item[1] == n[1]:
                    closed_index = i
                    break
        if closed_index == -1:
            closed_index = len(closed)
            closed.append(n)

        if n[1] == goal_state:
            break
        successors = get_succ(n[1])
        
        for s in successors:
            s_in_open_i = -1
            s_in_closed_i = -1
            for i, item in enumerate(open):
                if item[1] == s:
                    s_in_open_i = i
                    break
            for i, item in enumerate(closed):
                if item[1] == s:
                    s_in_closed_i = i
                    break
            
            # s_in_open_i = next((i for i, item in enumerate(open) if item[1] == s), -1)
            # s_in_closed_i = next((i for i, item in enumerate(closed) if item[1] == s), -1)

            h = get_manhattan_distance(s, goal_state)
            g = n[2][0] + 1
            f = g + h
            parent_index = closed_index
            if (s_in_open_i == -1) and (s_in_closed_i == -1):
                heapq.heappush(open,(f, s, (g, h, parent_index)))
                queue_length += 1
                max_length = max(max_length, queue_length)
            if s_in_open_i != -1:
                n = open[s_in_open_i]
                if g < n[2][0]:
                    open[s_in_open_i] = (f, s, (g, h, parent_index))
                    heapq.heapify(open)
                    # heapq.heappush(open,(f, s, (g, h, parent_index)))
            if s_in_closed_i != -1:
                n = closed[s_in_closed_i]
                if g < n[2][0]:
                    closed[s_in_closed_i] = (f, s, (g, h, parent_index))
                    if s_in_open_i == -1:
                        heapq.heappush(open,(f, s, (g, h, parent_index)))    
                        queue_length += 1
                        max_length = max(max_length, queue_length)

    print("finished running")
    print(*closed, sep='\n')
    print(closed_index)

    travelsal = []
    n = closed[closed_index]
    while (True):
        travelsal.append(n)
        if n[2][2] == -1:
            break
        n = closed[n[2][2]]

    travelsal.reverse()

    state_info_list = []
    moves = 0
    for e in travelsal:
        current_state = e[1]
        h = e[2][1]
        state_info_list.append((current_state, h, moves))
        moves += 1


    # This is a format helper.
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute max length
    # it can help to avoid any potential format issue.
    for state_info in state_info_list:
        current_state = state_info[0]
        h = state_info[1]
        move = state_info[2]
        print(current_state, "h={}".format(h), "moves: {}".format(move))
    print("Max queue length: {}".format(max_length))

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    # print_succ([2,5,1,4,0,6,7,0,3])
    # print_succ([2,5,1,4,0,6,7,0,3])

    # print_succ([3, 4, 6, 0, 0, 1, 7, 2, 5])
    # print()
    # print_succ([6, 0, 0, 3, 5, 1, 7, 2, 4])
    # print()
    # print_succ([0, 4, 7, 1, 3, 0, 6, 2, 5])
    # print()

    # print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    # print()

    # solve([2,5,1,4,0,6,7,0,3])
    # solve([4,3,0,5,1,6,7,2,0])
    # solve([3, 4, 6, 0, 0, 1, 7, 2, 5])
    solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    # solve([0, 4, 7, 1, 3, 0, 6, 2, 5])
    print()
