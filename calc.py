import tkinter as tk

# Main window
main_window = tk.Tk()
main_window.geometry("310x450")  # Set window size for a more calculator-like aspect ratio

# Creating a list
numbers = []
operation = []


# Functions
def calculate_result():
    global numbers, operation

    current = screen.get()
    if current and current != 'Insert a number':
        numbers.append(current)  # Save the current number on screen before operating
    else:
        screen.delete(0, tk.END)
        screen.insert(tk.END, 'Insert a number')
        return

    if len(numbers) != len(operation) + 1:
        screen.delete(0, tk.END)
        screen.insert(tk.END, 'Invalid input')
        numbers.clear()
        operation.clear()
        return

    try:
        nums = [float(n) for n in numbers]
    except ValueError:
        screen.delete(0, tk.END)
        screen.insert(tk.END, 'Invalid number')
        numbers.clear()
        operation.clear()
        return

    expr = []
    for i in range(len(operation)):
        expr.append(nums[i])
        expr.append(operation[i])
    expr.append(nums[-1])

    i = 1
    while i < len(expr) - 1:
        op = expr[i]
        if op in ('*', '/'):
            left = expr[i - 1]
            right = expr[i + 1]
            if op == '*':
                result = left * right
            else:
                if right == 0:
                    screen.delete(0, tk.END)
                    screen.insert(tk.END, 'Division by zero')
                    numbers.clear()
                    operation.clear()
                    return
                result = left / right
            expr[i - 1:i + 2] = [result]
            i = 1  # Reset i to check for more multiplications/divisions
        else:
            i += 2

    i = 1
    while i < len(expr) - 1:
        op = expr[i]
        left = expr[i - 1]
        right = expr[i + 1]
        if op == '+':
            result = left + right
        elif op == '-':
            result = left - right
        else:
            screen.delete(0, tk.END)
            screen.insert(tk.END, f"Unknown op {op}")
            return
        expr[i - 1:i + 2] = [result]
        i = 1  # Reset i to start from beginning

    screen.delete(0, tk.END)
    screen.insert(0, str(expr[0]))
    numbers.clear()
    operation.clear()


def print_num():
    global numbers, operation
    print(numbers)
    print(operation)


def erase():
    global screen, numbers, operation
    screen.delete(0, tk.END)
    numbers = []
    operation = []


def delete_last_char():
    current = screen.get()
    if current and current != 'Insert a number':
        screen.delete(len(current) - 1, tk.END)


def print_onto_screen(value):
    global screen
    if screen.get() == 'Insert a number':
        screen.delete(0, tk.END)
    screen.insert(tk.END, value)


def save_operate(symbol, num):
    global numbers, operation
    if num.strip() == '' or num == 'Insert a number':
        screen.delete(0, tk.END)
        screen.insert(tk.END, 'Insert a number')
        return
    try:
        float(num)  # Validation
    except ValueError:
        screen.delete(0, tk.END)
        screen.insert(tk.END, 'Invalid number')
        return
    numbers.append(num)
    operation.append(symbol)
    screen.delete(0, tk.END)


# Graphical settings
main_window.title("Mini Calculator")
main_window.resizable(False, False)
main_window.configure(bg="#222222")

# Set a calculator-like style for buttons and entry
button_style = {
    "font": ("Arial", 16, "bold"),
    "bg": "#4A4A4A",
    "fg": "#FFFFFF",
    "activebackground": "#666666",
    "activeforeground": "#FFFFFF",
    "bd": 0,
    "width": 5,
    "height": 2,
    "cursor": "hand2"
}

operation_button_style = {
    "font": ("Arial", 16, "bold"),
    "bg": "#FF9500",
    "fg": "#FFFFFF",
    "activebackground": "#FFB54C",
    "relief": "raised",
    "activeforeground": "#FFFFFF",
    "bd": 0,
    "width": 5,
    "height": 2,
    "cursor": "hand2"
}

entry_style = {
    "font": ("Arial", 24, "bold"),
    "bg": "#222222",
    "fg": "#FFFFFF",
    "bd": 0,
    "insertbackground": "#FFFFFF",
    "justify": "right",
    "relief": "sunken"
}


# Apply styles to buttons and entry after creation
def apply_styles():
    for widget in main_window.winfo_children():
        if isinstance(widget, tk.Button):
            if widget['text'] in ['+', '-', '*', '/', '=']:
                widget.configure(**operation_button_style)
            else:
                widget.configure(**button_style)
        elif isinstance(widget, tk.Entry):
            widget.configure(**entry_style)


main_window.after(0, lambda: apply_styles())

# Screen
screen = tk.Entry(main_window, width=16, bd=0, justify="right")
screen.grid(row=0, column=0, columnspan=4, padx=12, pady=20, ipady=18, sticky="nsew")

# Buttons, texts and the like
buttons = [
    # row 1
    ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('/', 1, 3, 'op'),
    # row 2
    ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('*', 2, 3, 'op'),
    # row 3
    ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('-', 3, 3, 'op'),
    # row 4
    ('.', 4, 0, 'num'), ('0', 4, 1, 'num'), ('=', 4, 2, 'equal'), ('+', 4, 3, 'op'),
    # row 5
    ('C', 5, 0, 'clear'), ('⌫', 5, 2, 'delete')  # Ojo: el '⌫' abarca col=2 y col=3
]

# Create the buttons
for text, row, col, btype in buttons:
    if btype == 'num':
        cmd = lambda val=text: print_onto_screen(val)
    elif btype == 'op':
        cmd = lambda op=text: save_operate(op, screen.get())
    elif btype == 'equal':
        cmd = calculate_result
    elif btype == 'clear':
        cmd = erase
    elif btype == 'delete':
        cmd = delete_last_char
    else:
        continue  # Ignore types not set up

    btn = tk.Button(main_window, text=text, width=5, command=cmd)

    # Let's set up the postitions
    if text == 'C':
        btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
        btn.configure(bg="#A5A5A5", fg="#000000")
    elif text == '⌫':
        btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
        btn.configure(bg="#A5A5A5", fg="#000000")
    else:
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

main_window.mainloop()
