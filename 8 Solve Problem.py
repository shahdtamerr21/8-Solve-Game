import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

ROWS, COLS = 3, 3  # Define constants for rows and columns

class PuzzleGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("8-Puzzle Solver")
        
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.current_state = []
        self.empty_tile_index = 0

        self.buttons = []
        for i in range(ROWS * COLS):
            button = tk.Button(self.root, text=' ', font='normal 20 bold', width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // COLS, column=i % COLS)
            self.buttons.append(button)

        algorithms = [("Backtracking", self.solve_backtracking),
                      ("Forward Check", self.solve_forward_check),
                      ("Arc Consistency", self.solve_arc_consistency)]
        
        for i, (text, command) in enumerate(algorithms):
            tk.Button(self.root, text=text, command=command).grid(row=ROWS, column=i)

        tk.Button(self.root, text="Shuffle", command=self.shuffle_puzzle).grid(row=ROWS + 1, column=0, columnspan=3)

        self.shuffle_puzzle()
        self.root.mainloop()

    def shuffle_puzzle(self):
        self.current_state = self.goal_state[:]
        random.shuffle(self.current_state)
        while not self.is_solvable(self.current_state):
            random.shuffle(self.current_state)
        self.empty_tile_index = self.current_state.index(0)
        self.display_board()

    def display_board(self):
        for i in range(ROWS * COLS):
            self.buttons[i].config(text=str(self.current_state[i]) if self.current_state[i] != 0 else ' ')

    def on_button_click(self, index):
        if self.is_movable(index):
            self.make_move(index)
            self.display_board()
            if self.is_solved():
                messagebox.showinfo("Game Over", "Congratulations! You solved the puzzle!")

    def make_move(self, index):
        new_state = self.current_state[:]
        new_state[self.empty_tile_index], new_state[index] = new_state[index], new_state[self.empty_tile_index]
        self.empty_tile_index = index
        self.current_state = new_state

    def is_movable(self, index):
        return abs(self.empty_tile_index - index) in (1, ROWS)

    def is_solved(self):
        return self.current_state == self.goal_state

    def is_solvable(self, state):
        inv_count = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] and state[j] and state[i] > state[j]:
                    inv_count += 1
        return inv_count % 2 == 0  # Solvable if inversion count is even

    def solve_backtracking(self):
        solution = self.backtrack(self.current_state, set())
        if solution:
            self.current_state = solution
            self.display_board()
            messagebox.showinfo("Solution Found", "The puzzle has been solved!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for this configuration.")

    def backtrack(self, state, visited):
        stack = [state]
        
        while stack:
            current_state = stack.pop()

            if current_state == self.goal_state:
                return current_state

            state_tuple = tuple(current_state)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            for move in self.get_possible_moves(current_state):
                stack.append(move)
        
        return None

    def get_possible_moves(self, state):
        possible_moves = []
        empty_index = state.index(0)
        empty_row, empty_col = divmod(empty_index, COLS)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                new_index = new_row * COLS + new_col
                new_state = state[:]
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                possible_moves.append(new_state)

        return possible_moves

    def solve_forward_check(self):
        visited = set()  # Track visited states
        if self.forward_check(self.current_state, visited):
            self.display_board()
            messagebox.showinfo("Solution Found", "The puzzle has been solved using Forward Checking!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for this configuration.")

    def forward_check(self, state, visited):
        stack = [(state, [])]  # Stack contains tuples of (current state, path)
        
        while stack:
            current_state, path = stack.pop()
            # Check if the current state is the goal
            if current_state == self.goal_state:
                self.current_state = current_state  # Update current state
                self.display_board()  # Update the display
                return True

            state_tuple = tuple(current_state)
            if state_tuple in visited:
                continue  # Avoid revisiting the same state
            visited.add(state_tuple)

            # Generate possible moves
            for move in self.get_possible_moves(current_state):
                if tuple(move) not in visited and self.is_solvable(move):
                    stack.append((move, path + [move]))  # Add new state to the stack with the path

        return False  # No solution found
    
    def solve_arc_consistency(self):
        visited = set()
        if self.arc_consistency(self.current_state, visited):
            self.display_board()
            messagebox.showinfo("Solution Found", "The puzzle has been solved using Arc Consistency!")
        else:
            messagebox.showinfo("No Solution", "No solution exists for this configuration.")

    def arc_consistency(self, state, visited):
        queue = deque([(state, visited.copy())])

        while queue:
            current_state, visited_states = queue.popleft()

            if current_state == self.goal_state:
                self.current_state = current_state
                return True

            state_tuple = tuple(current_state)
            if state_tuple in visited_states:
                continue

            visited_states.add(state_tuple)

            for move in self.get_possible_moves(current_state):
                if self.is_solvable(move):
                    queue.append((move, visited_states.copy()))

        return False

if __name__ == "__main__":
    PuzzleGame()
