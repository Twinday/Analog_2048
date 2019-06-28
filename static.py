def search_path(matrix, start, end):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    goal_state = end


    def dfs(current_path):
        row, col = current_path[-1]
        if (row, col) == goal_state:
            return True

        for direction in [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]:
            new_row, new_col = direction
            if (0 <= new_row < num_rows and 0 <= new_col < num_cols and
                    matrix[new_row][new_col] == "0" and
                    (new_row, new_col) not in current_path):

                current_path.append((new_row, new_col))
                if dfs(current_path):
                    return True
                else:
                    current_path.pop()


    result = [start]
    if dfs(result):
        return True
    else:
        return False
