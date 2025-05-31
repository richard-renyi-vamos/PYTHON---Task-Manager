import tkinter as tk

def add_task():
    task = entry_task.get()
    due = entry_due.get()
    if task:
        full_task = f"{task} (Due: {due})" if due else task
        tasks.append(full_task)
        update_task_list()
        entry_task.delete(0, tk.END)
        entry_due.delete(0, tk.END)

def remove_task():
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        del tasks[index]
        update_task_list()

def edit_task():
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        new_task = entry_task.get()
        due = entry_due.get()
        full_task = f"{new_task} (Due: {due})" if due else new_task
        tasks[index] = full_task
        update_task_list()
        entry_task.delete(0, tk.END)
        entry_due.delete(0, tk.END)

def mark_task_done():
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        task = tasks[index]
        if not task.startswith("[✔] "):
            tasks[index] = "[✔] " + task
        update_task_list()

def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as f:
            loaded = f.readlines()
            global tasks
            tasks = [task.strip() for task in loaded]
            update_task_list()
    except FileNotFoundError:
        pass

def search_task():
    query = entry_search.get().lower()
    task_list.selection_clear(0, tk.END)
    for i, task in enumerate(tasks):
        if query in task.lower():
            task_list.selection_set(i)
            task_list.activate(i)

def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task)

def on_select(event):
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        task = tasks[index]
        # Remove [✔] if exists for editing clarity
        clean_task = task.replace("[✔] ", "")
        entry_task.delete(0, tk.END)
        entry_task.insert(tk.END, clean_task.split(" (Due:")[0])
        if "(Due:" in clean_task:
            due_part = clean_task.split("(Due:")[-1].replace(")", "").strip()
            entry_due.delete(0, tk.END)
            entry_due.insert(tk.END, due_part)

# --- GUI SETUP ---
tasks = []

root = tk.Tk()
root.title("Task Manager")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

# Task Entry
label_task = tk.Label(frame_input, text="Task:")
label_task.grid(row=0, column=0)
entry_task = tk.Entry(frame_input, width=30)
entry_task.grid(row=0, column=1)

# Due Date Entry
label_due = tk.Label(frame_input, text="Due:")
label_due.grid(row=1, column=0)
entry_due = tk.Entry(frame_input, width=30)
entry_due.grid(row=1, column=1)

# Add Button
button_add = tk.Button(frame_input, text="Add", command=add_task)
button_add.grid(row=0, column=2, rowspan=2, padx=5)

# Search Entry
label_search = tk.Label(frame_input, text="Search:")
label_search.grid(row=2, column=0)
entry_search = tk.Entry(frame_input, width=30)
entry_search.grid(row=2, column=1)
button_search = tk.Button(frame_input, text="Search", command=search_task)
button_search.grid(row=2, column=2)

# Task List with Scrollbar
frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10)

task_list = tk.Listbox(frame_tasks, width=50, height=10)
task_list.pack(side=tk.LEFT)
task_list.bind('<<ListboxSelect>>', on_select)

scrollbar = tk.Scrollbar(frame_tasks, orient=tk.VERTICAL)
scrollbar.config(command=task_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
task_list.config(yscrollcommand=scrollbar.set)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_remove = tk.Button(frame_buttons, text="Remove", command=remove_task)
button_remove.pack(side=tk.LEFT, padx=2)

button_edit = tk.Button(frame_buttons, text="Edit", command=edit_task)
button_edit.pack(side=tk.LEFT, padx=2)

button_done = tk.Button(frame_buttons, text="Mark Done", command=mark_task_done)
button_done.pack(side=tk.LEFT, padx=2)

button_save = tk.Button(frame_buttons, text="Save", command=save_tasks)
button_save.pack(side=tk.LEFT, padx=2)

button_load = tk.Button(frame_buttons, text="Load", command=load_tasks)
button_load.pack(side=tk.LEFT, padx=2)

# Load existing tasks at startup (optional)
load_tasks()

# Auto-save on close (optional)
root.protocol("WM_DELETE_WINDOW", lambda: (save_tasks(), root.destroy()))

root.mainloop()
