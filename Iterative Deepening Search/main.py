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
answer = []


def dfs(cube, max_depth, current_depth):
    global produced_nodes
    global expanded_nodes
    global answer_depth
    global used_memory
    global max_memory

    used_memory += 1
    max_memory = max(max_memory, used_memory)
    produced_nodes += 1
    expanded_nodes += 1

    if goal_test(cube):
        answer_depth = current_depth
        used_memory -= 1
        return True

    if current_depth == max_depth:
        used_memory -= 1
        return False

    result = False
    for i in range(0, 3):
        new_cube = rotate_right(cube, i)
        result = dfs(new_cube, max_depth, current_depth + 1)
        if result:
            answer.append("turn facet#" + str(i + 1) + " clockwise")
            break
        new_cube = rotate_left(cube, i)
        result = dfs(new_cube, max_depth, current_depth + 1)
        if result:
            answer.append("turn facet#" + str(i + 1) + " anticlockwise")
            break

    used_memory -= 1
    return result


def main():
    cube = [[0 for i in range(4)] for j in range(6)]
    initial_depth = int(input("initial depth: "))
    print("cube colors:")
    for i in range(0, 6):
        arr = input()
        cube[i] = list(map(int, arr.split(' ')))

    max_depth = initial_depth
    while not dfs(cube, max_depth, 0):
        max_depth += 1
        print(max_depth)

    print("Produced Nodes: %d" % produced_nodes)
    print("Expanded Nodes: %d" % expanded_nodes)
    print("Answer Depth: %d" % answer_depth)
    print("Max Memory: %d" % max_memory)

    print("\nSolution:")
    for a in reversed(answer):
        print(a)


if __name__ == '__main__':
    main()
