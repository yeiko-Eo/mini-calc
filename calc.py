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

# Buttons
button_7 = tk.Button(main_window, text='7', width=5, command=lambda: print_onto_screen(7))
button_7.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

button_8 = tk.Button(main_window, text='8', width=5, command=lambda: print_onto_screen(8))
button_8.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

button_9 = tk.Button(main_window, text='9', width=5, command=lambda: print_onto_screen(9))
button_9.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

button_div = tk.Button(main_window, text='/', width=5, command=lambda: save_operate('/', screen.get()))
button_div.grid(row=1, column=3, padx=2, pady=2, sticky="nsew")

button_4 = tk.Button(main_window, text='4', width=5, command=lambda: print_onto_screen(4))
button_4.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

button_5 = tk.Button(main_window, text='5', width=5, command=lambda: print_onto_screen(5))
button_5.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")

button_6 = tk.Button(main_window, text='6', width=5, command=lambda: print_onto_screen(6))
button_6.grid(row=2, column=2, padx=2, pady=2, sticky="nsew")

button_mult = tk.Button(main_window, text='*', width=5, command=lambda: save_operate('*', screen.get()))
button_mult.grid(row=2, column=3, padx=2, pady=2, sticky="nsew")

button_1 = tk.Button(main_window, text='1', width=5, command=lambda: print_onto_screen(1))
button_1.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")

button_2 = tk.Button(main_window, text='2', width=5, command=lambda: print_onto_screen(2))
button_2.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

button_3 = tk.Button(main_window, text='3', width=5, command=lambda: print_onto_screen(3))
button_3.grid(row=3, column=2, padx=2, pady=2, sticky="nsew")

button_minus = tk.Button(main_window, text='-', width=5, command=lambda: save_operate('-', screen.get()))
button_minus.grid(row=3, column=3, padx=2, pady=2, sticky="nsew")

button_dot = tk.Button(main_window, text='.', width=5, command=lambda: print_onto_screen('.'))
button_dot.grid(row=4, column=0, padx=2, pady=2, sticky="nsew")

button_0 = tk.Button(main_window, text='0', width=5, command=lambda: print_onto_screen(0))
button_0.grid(row=4, column=1, padx=2, pady=2, sticky="nsew")

button_result = tk.Button(main_window, text='=', width=5, command=calculate_result)
button_result.grid(row=4, column=2, padx=2, pady=2, sticky="nsew")

button_plus = tk.Button(main_window, text='+', width=5, command=lambda: save_operate('+', screen.get()))
button_plus.grid(row=4, column=3, padx=2, pady=2, sticky="nsew")

button_erase = tk.Button(main_window, text='C', width=5, command=erase)
button_erase.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")
button_erase.configure(bg="#A5A5A5", fg="#000000")

button_delete = tk.Button(main_window, text='⌫', width=5, command=delete_last_char)
button_delete.grid(row=5, column=2, columnspan=2, padx=2, pady=2, sticky="nsew")
button_delete.configure(bg="#A5A5A5", fg="#000000")

main_window.mainloop()
