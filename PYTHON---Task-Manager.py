import tkinter as tk

def add_task():
    task = entry_task.get()
    if task:
        tasks.append(task)
        update_task_list()

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
        tasks[index] = new_task
        update_task_list()

def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task)

def on_select(event):
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        task = tasks[index]
        entry_task.delete(0, tk.END)
        entry_task.insert(tk.END, task)

tasks = []

root = tk.Tk()
root.title("Task Manager")

frame_input = tk.Frame(root)
frame_input.pack()

label_task = tk.Label(frame_input, text="Task:")
label_task.grid(row=0, column=0)

entry_task = tk.Entry(frame_input)
entry_task.grid(row=0, column=1)

button_add = tk.Button(frame_input, text="Add", command=add_task)
button_add.grid(row=0, column=2)

frame_tasks = tk.Frame(root)
frame_tasks.pack()

task_list = tk.Listbox(frame_tasks, width=50)
task_list.pack(side=tk.LEFT)

task_list.bind('<<ListboxSelect>>', on_select)

scrollbar = tk.Scrollbar(frame_tasks, orient=tk.VERTICAL)
scrollbar.config(command=task_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list.config(yscrollcommand=scrollbar.set)

frame_buttons = tk.Frame(root)
frame_buttons.pack()

button_remove = tk.Button(frame_buttons, text="Remove", command=remove_task)
button_remove.pack(side=tk.LEFT)

button_edit = tk.Button(frame_buttons, text="Edit", command=edit_task)
button_edit.pack(side=tk.LEFT)

root.mainloop()
