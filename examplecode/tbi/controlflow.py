class ControlFlow:
    def __init__(self):
        self.call_stack = []
        self.current_line = None
        self.program_end = False
        self.program = {}
        self.sorted_lines = []  # List of sorted line numbers
        self.current_index = 0  # Index to track current position in sorted_lines

    def load_program(self, program_list):
        """ Load and sort the program by line numbers into a dictionary. """
        self.program = {line: stmt for line, stmt in program_list}
        self.sorted_lines = sorted(self.program.keys())  # Store sorted line numbers
        if self.program:
            self.current_line = self.sorted_lines[0]  # Start at the first line number
            self.current_index = 0

    def run_program(self):
        """ Run the program by traversing statements according to their line numbers. """
        if self.current_line is None:
            raise ValueError("Program not loaded or no statements to execute")

        while not self.program_end and self.current_line in self.program:
            statement = self.program[self.current_line]
            statement.execute()
            # Automatically move to the next line unless altered externally
            self.next_line()

    def next_line(self):
        """ Helper to advance to the next line in the sorted order. """
        self.current_index += 1  # Move to the next index in the sorted list
        if self.current_index < len(self.sorted_lines):
            self.current_line = self.sorted_lines[self.current_index]
        else:
            self.end_program()  # End the program if there are no more lines

    def call_subroutine(self, line_number):
        """ Saves the next line and jumps to the subroutine at line_number. """
        self.call_stack.append(self.sorted_lines[self.current_index + 1])  # Save the next line
        self.current_line = line_number
        self.current_index = self.sorted_lines.index(line_number)  # Update the index

    def return_from_subroutine(self):
        """ Return from a subroutine by popping the return address from the stack. """
        self.current_line = self.call_stack.pop()
        self.current_index = self.sorted_lines.index(self.current_line)  # Update the index to match the current line

    def end_program(self):
        """ Set the program to end. """
        self.program_end = True
