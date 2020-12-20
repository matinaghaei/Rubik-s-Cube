import copy
from queue import PriorityQueue


def rotate_right(cube, index):
    cube_copy = copy.deepcopy(cube)

    cube_copy[index][0] = cube[index][2]
    cube_copy[index][1] = cube[index][0]
    cube_copy[index][2] = cube[index][3]
    cube_copy[index][3] = cube[index][1]

    if index == 0:
        cube_copy[1][0] = cube[2][0]
        cube_copy[1][1] = cube[2][1]
        cube_copy[2][0] = cube[3][0]
        cube_copy[2][1] = cube[3][1]
        cube_copy[3][0] = cube[5][3]
        cube_copy[3][1] = cube[5][2]
        cube_copy[5][3] = cube[1][0]
        cube_copy[5][2] = cube[1][1]
    elif index == 1:
        cube_copy[0][2] = cube[5][2]
        cube_copy[0][0] = cube[5][0]
        cube_copy[2][2] = cube[0][2]
        cube_copy[2][0] = cube[0][0]
        cube_copy[4][2] = cube[2][2]
        cube_copy[4][0] = cube[2][0]
        cube_copy[5][2] = cube[4][2]
        cube_copy[5][0] = cube[4][0]
    elif index == 2:
        cube_copy[0][3] = cube[1][1]
        cube_copy[0][2] = cube[1][3]
        cube_copy[1][1] = cube[4][0]
        cube_copy[1][3] = cube[4][1]
        cube_copy[3][2] = cube[0][3]
        cube_copy[3][0] = cube[0][2]
        cube_copy[4][0] = cube[3][2]
        cube_copy[4][1] = cube[3][0]

    return cube_copy


def rotate_left(cube, index):
    cube_copy = copy.deepcopy(cube)

    cube_copy[index][0] = cube[index][1]
    cube_copy[index][1] = cube[index][3]
    cube_copy[index][2] = cube[index][0]
    cube_copy[index][3] = cube[index][2]

    if index == 0:
        cube_copy[1][1] = cube[5][2]
        cube_copy[1][0] = cube[5][3]
        cube_copy[2][1] = cube[1][1]
        cube_copy[2][0] = cube[1][0]
        cube_copy[3][1] = cube[2][1]
        cube_copy[3][0] = cube[2][0]
        cube_copy[5][2] = cube[3][1]
        cube_copy[5][3] = cube[3][0]
    elif index == 1:
        cube_copy[0][0] = cube[2][0]
        cube_copy[0][2] = cube[2][2]
        cube_copy[2][0] = cube[4][0]
        cube_copy[2][2] = cube[4][2]
        cube_copy[4][0] = cube[5][0]
        cube_copy[4][2] = cube[5][2]
        cube_copy[5][0] = cube[0][0]
        cube_copy[5][2] = cube[0][2]
    elif index == 2:
        cube_copy[0][2] = cube[3][0]
        cube_copy[0][3] = cube[3][2]
        cube_copy[1][3] = cube[0][2]
        cube_copy[1][1] = cube[0][3]
        cube_copy[3][0] = cube[4][1]
        cube_copy[3][2] = cube[4][0]
        cube_copy[4][1] = cube[1][3]
        cube_copy[4][0] = cube[1][1]

    return cube_copy


def goal_test(cube):
    for i in range(0, 6):
        if cube[i][0] != cube[i][1]:
            return False
        if cube[i][0] != cube[i][2]:
            return False
        if cube[i][0] != cube[i][3]:
            return False
    print(cube)
    return True


produced_nodes = 0
expanded_nodes = 0
answer_depth = 0
used_memory = 0
max_memory = 0


def find_answer(node):
    answer = []
    while node['parent'] is not None:
        answer.append(node['last move'])
        node = node['parent']
    return answer


def search(state, frontier):
    for node in frontier:
        if node['state'] == state:
            return node
    return None


def heuristic(state):
    four_diff = 0
    three_diff = 0
    two_diff = 0
    for i in range(6):
        if state[i][0] == state[i][1] and state[i][0] == state[i][2] and state[i][0] == state[i][3]:
            pass
        elif state[i][0] == state[i][1] and state[i][2] == state[i][3]:
            two_diff += 1
        elif state[i][0] == state[i][2] and state[i][1] == state[i][3]:
            two_diff += 1
        elif state[i][0] == state[i][3] and state[i][1] == state[i][2]:
            two_diff += 1
        elif state[i][0] == state[i][1] and state[i][1] == state[i][2]:
            two_diff += 1
        elif state[i][0] == state[i][1] and state[i][1] == state[i][3]:
            two_diff += 1
        elif state[i][0] == state[i][2] and state[i][2] == state[i][3]:
            two_diff += 1
        elif state[i][1] == state[i][2] and state[i][2] == state[i][3]:
            two_diff += 1
        elif state[i][0] == state[i][1] or state[i][0] == state[i][2] or state[i][0] == state[i][3]:
            three_diff += 1
        elif state[i][1] == state[i][2] or state[i][1] == state[i][3] or state[i][2] == state[i][3]:
            three_diff += 1
        else:
            four_diff += 1
    return two_diff + three_diff * 2 + four_diff * 4


class PriorityEntry(object):
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


def main():
    global produced_nodes
    global expanded_nodes
    global answer_depth
    global used_memory
    global max_memory

    cube_initial = [[0 for i in range(4)] for j in range(6)]
    print("cube colors:")
    for i in range(0, 6):
        arr = input()
        cube_initial[i] = list(map(int, arr.split(' ')))

    path = []
    explored = []
    frontier = PriorityQueue()
    frontier.put(PriorityEntry(0 + heuristic(cube_initial),
                               {'state': cube_initial, 'parent': None, 'depth': 0, 'last move': None}))
    explored.append(cube_initial)
    max_memory = used_memory = produced_nodes = 1

    success = False
    while not frontier.empty() and not success:
        node = frontier.get().data
        cube = node['state']
        for i in range(0, 3):
            new_cube = rotate_right(cube, i)
            if new_cube not in explored:
                if goal_test(new_cube):
                    success = True
                    answer_depth = node['depth'] + 1
                    path = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " clockwise"})
                    break
                frontier.put(PriorityEntry(node['depth'] + 1 + heuristic(new_cube),
                                           {'state': new_cube, 'parent': node, 'depth': node['depth'] + 1,
                                            'last move': "turn facet#" + str(i + 1) + " clockwise"}))
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
            new_cube = rotate_left(cube, i)
            if new_cube not in explored:
                if goal_test(new_cube):
                    success = True
                    answer_depth = node['depth'] + 1
                    path = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " anticlockwise"})
                    break
                frontier.put(PriorityEntry(node['depth'] + 1 + heuristic(new_cube),
                                           {'state': new_cube, 'parent': node, 'depth': node['depth'] + 1,
                                            'last move': "turn facet#" + str(i + 1) + " anticlockwise"}))
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
        expanded_nodes += 1

    print("Produced Nodes: %d" % produced_nodes)
    print("Expanded Nodes: %d" % expanded_nodes)
    print("Answer Depth: %d" % answer_depth)
    print("Max Memory: %d" % max_memory)

    print("\nSolution:")
    for s in reversed(path):
        print(s)


if __name__ == '__main__':
    main()
