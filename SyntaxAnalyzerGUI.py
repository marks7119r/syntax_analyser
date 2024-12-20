import tkinter as tk
from tkinter import messagebox
import SyntaxAnalyzer

def analyzer(input_string):
    # Tokenize the input string (Lexical Analyzer)
    tokens = SyntaxAnalyzer.tokenize(input_string)
    # Parse the tokens (Syntax Analyzer)
    syntax_tree = SyntaxAnalyzer.parse(tokens)
    return syntax_tree

def analyze_code():
    # Get the input code from the Text widget
    code = code_input.get("1.0", tk.END).strip()
    
    # Check if input is empty
    if not code:
        messagebox.showerror("Error", "Please enter some code to analyze.")
        return

    # Split the input code into multiple lines
    code_lines = code.splitlines()

    # Initialize a list to hold the results of each line
    syntax_trees = []

    try:
        # Process each line individually
        for i, line in enumerate(code_lines, start=1):
            # Call the analyzer function for each line
            syntax_tree = analyzer(line.strip())  
            syntax_trees.append(f"Line {i}:\n{syntax_tree}\n")

        
        result_output.delete(1.0, tk.END)  # Clear previous output
        result_output.insert(tk.END, "\n".join(syntax_trees))  # Display new output

    except SyntaxError as e:
        # Handle parsing errors
        messagebox.showerror("Syntax Error", str(e))
    except Exception as e:
        # Handle other errors
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Syntax Analyzer")

# Adjust window size and position
window_width = 600
window_height = 500

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the window's size and position
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Set minimum size
root.minsize(400, 300)

# Enable resizing
root.resizable(True, True)

# Set font type and size (for text widgets)
font = ("Courier New", 12)  

# Create the input section (code input)
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

code_label = tk.Label(input_frame, text="Enter Code:")
code_label.pack(side=tk.LEFT)

code_input = tk.Text(input_frame, height=10, width=50, font=font)
code_input.pack(side=tk.LEFT)

# Create the output section (syntax tree output)
output_frame = tk.Frame(root)
output_frame.pack(padx=10, pady=10)

result_label = tk.Label(output_frame, text="Syntax Tree:")
result_label.pack(side=tk.LEFT)

result_output = tk.Text(output_frame, height=10, width=50, font=font)
result_output.pack(side=tk.LEFT)

# Create the analyze button
analyze_button = tk.Button(root, text="Analyze", command=analyze_code)
analyze_button.pack(pady=10)

# Run the main GUI loop
root.mainloop()
