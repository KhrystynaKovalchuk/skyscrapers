"""
https://github.com/KhrystynaKovalchuk/skyscrapers
"""
def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    # >>> read_input("check.txt")
    # ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    file = open(path, "r")
    lines = []
    for line in file.readlines():
        lines.append(line.replace("\n", ""))
    file.close()
    return lines


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    check_lst = [1]  # counter
    needed_string = input_line[1:-1]
    lowest = needed_string[0]

    for i in range(len(needed_string) - 1):
        if lowest < needed_string[i + 1]:
            check_lst.append(1)
            lowest = needed_string[i + 1]
    if len(check_lst) == pivot:
        return True
    return False

# print(left_to_right_check("5124531", 5))

def right_to_left_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from right to left.
    Return True if number of building from the right-most hint is visible looking to the left,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> right_to_left_check("*143223", 3)
    True
    >>> right_to_left_check("*524534", 5)
    False
    """
    return left_to_right_check(input_line[::-1], pivot)


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5',\
     '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215',\
     '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215',\
     '*35214*', '*41532*', '*2*1***'])
    False
    """
    check = []
    for element in board:
        for elmnt in list(element):
            if elmnt == "?":
                check.append(1)
    if check != []:
        return False
    else:
        return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
     '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    els = board[1: len(board) - 1]
    buildings = [list(el[1:len(el) - 1]) for el in els]
    res = []
    for building in buildings:
        unique = set(building)
        if len(unique) == len(building):
            res.append(building)
    if res == buildings:
        return True
    else:
        return False


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    true_or_false = []
    for line in board[1:-1]:

        if line[0] != '*' and line[-1] != '*':
            res1 = left_to_right_check(line, int(line[0]))
            res2 = right_to_left_check(line, int(line[-1]))
            res_avg = res1 and res2
            true_or_false.append(res_avg)
        elif line[0] != '*':
            res = left_to_right_check(line, int(line[0]))
            true_or_false.append(res)
        elif line[-1] != '*':
            res = right_to_left_check(line, int(line[-1]))
            true_or_false.append(res)
    true_or_false.append(check_uniqueness_in_rows(board))
    return all(true_or_false)


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    new_board = form_columns(board)
    return check_horizontal_visibility(new_board)

def form_columns(board):
    """
    Returns columns from board.
    >>> form_columns([])
    []
    """
    lst = []
    general = []
    for i in range(len(board)):
        for line in board:
            lst.append(line[i])
        general.append(lst.copy())
        lst.clear()
    return general


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    # >>> check_skyscrapers("check.txt")
    # True
    # >>> check_skyscrapers("input.txt")
    # False
    """
    board = read_input(input_path)
    lines = check_uniqueness_in_rows(board)
    correct_board = check_not_finished_board(board)
    if lines == True and correct_board == True:
        horizontal = check_horizontal_visibility(board)
        vertical = check_columns(board)
        if horizontal == True and vertical == True:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
