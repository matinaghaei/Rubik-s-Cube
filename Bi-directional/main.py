import copy


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
    return True


produced_nodes = 0
expanded_nodes = 0
answer_depth = 0
used_memory = 0
max_memory = 0


def generate_goal_state(a, b, c):
    f = [0, 5, 4, 6, 2, 1, 3]
    return [[f[b], f[b], f[b], f[b]],
            [f[a], f[a], f[a], f[a]],
            [f[c], f[c], f[c], f[c]],
            [a, a, a, a],
            [b, b, b, b],
            [c, c, c, c]]


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

    answer1 = []
    answer2 = []
    explored = []
    frontier_initial = [{'state': cube_initial, 'parent': None, 'last move': None}]
    explored.append(cube_initial)
    cube_goal = generate_goal_state(cube_initial[3][3], cube_initial[4][3], cube_initial[5][1])
    frontier_goal = [{'state': cube_goal, 'parent': None, 'last move': None}]
    explored.append(cube_goal)
    max_memory = used_memory = produced_nodes = 2

    success = False
    while len(frontier_initial) > 0 and len(frontier_goal) > 0:
        node = frontier_initial.pop(0)
        cube = node['state']
        for i in range(0, 3):
            new_cube = rotate_right(cube, i)
            if new_cube not in explored:
                frontier_initial.append({'state': new_cube, 'parent': node,
                                         'last move': "turn facet#" + str(i + 1) + " clockwise"})
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
            elif search(new_cube, frontier_goal) is not None:
                answer1 = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " clockwise"})
                answer2 = find_answer(search(new_cube, frontier_goal))
                success = True
                break
            new_cube = rotate_left(cube, i)
            if new_cube not in explored:
                frontier_initial.append({'state': new_cube, 'parent': node,
                                         'last move': "turn facet#" + str(i + 1) + " anticlockwise"})
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
            elif search(new_cube, frontier_goal) is not None:
                answer1 = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " anticlockwise"})
                answer2 = find_answer(search(new_cube, frontier_goal))
                success = True
                break
        expanded_nodes += 1
        if success:
            break

        node = frontier_goal.pop(0)
        cube = node['state']
        for i in range(0, 3):
            new_cube = rotate_right(cube, i)
            if new_cube not in explored:
                frontier_goal.append({'state': new_cube, 'parent': node,
                                      'last move': "turn facet#" + str(i + 1) + " anticlockwise"})
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
            elif search(new_cube, frontier_initial) is not None:
                answer2 = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " anticlockwise"})
                answer1 = find_answer(search(new_cube, frontier_initial))
                success = True
                break
            new_cube = rotate_left(cube, i)
            if new_cube not in explored:
                frontier_goal.append({'state': new_cube, 'parent': node,
                                      'last move': "turn facet#" + str(i + 1) + " clockwise"})
                explored.append(new_cube)
                produced_nodes += 1
                used_memory += 1
                max_memory = max(max_memory, used_memory)
            elif search(new_cube, frontier_initial) is not None:
                answer2 = find_answer({'parent': node, 'last move': "turn facet#" + str(i + 1) + " clockwise"})
                answer1 = find_answer(search(new_cube, frontier_initial))
                success = True
                break
        expanded_nodes += 1
        if success:
            break
    answer_depth = len(answer1) + len(answer2)

    print("Produced Nodes: %d" % produced_nodes)
    print("Expanded Nodes: %d" % expanded_nodes)
    print("Answer Depth: %d" % answer_depth)
    print("Max Memory: %d" % max_memory)

    print("\nSolution:")
    for s in reversed(answer1):
        print(s)
    for s in answer2:
        print(s)


if __name__ == '__main__':
    main()
