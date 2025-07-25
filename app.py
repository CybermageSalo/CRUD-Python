import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conexão com banco
conn = sqlite3.connect('crud.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT
)''')

def insert_task():
    title = entry_title.get()
    description = entry_description.get()
    if title:
        cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
        conn.commit()
        entry_title.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        list_tasks()
    else:
        messagebox.showwarning("Erro", "Título é obrigatório")

def list_tasks():
    listbox.delete(0, tk.END)
    for row in cursor.execute("SELECT id, title FROM tasks"):
        listbox.insert(tk.END, f"{row[0]} - {row[1]}")

def update_task():
    selected = listbox.curselection()
    if selected:
        task_id = int(listbox.get(selected).split(" - ")[0])
        new_title = entry_title.get()
        new_description = entry_description.get()
        if new_title:
            cursor.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ?",
                           (new_title, new_description, task_id))
            conn.commit()
            list_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_id = int(listbox.get(selected).split(" - ")[0])
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        list_tasks()
    else:
        messagebox.showwarning("Erro", "Nenhuma tarefa selecionada")

# Interface
root = tk.Tk()
root.title("Gerenciador de Tarefas")

tk.Label(root, text="Título").pack()
entry_title = tk.Entry(root)
entry_title.pack()

tk.Label(root, text="Descrição").pack()
entry_description = tk.Entry(root)
entry_description.pack()

tk.Button(root, text="Adicionar Tarefa", command=insert_task).pack()
tk.Button(root, text="Remover Tarefa", command=delete_task).pack()
tk.Button(root, text="Atualizar Tarefa", command=update_task).pack()


listbox = tk.Listbox(root, width=50)
listbox.pack()

def on_select(event):
    selected = listbox.curselection()
    if selected:
        task_id = int(listbox.get(selected).split(" - ")[0])
        cursor.execute("SELECT title, description FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task:
            entry_title.delete(0, tk.END)
            entry_title.insert(0, task[0])
            entry_description.delete(0, tk.END)
            entry_description.insert(0, task[1])

listbox.bind('<<ListboxSelect>>', on_select)


list_tasks()
root.mainloop()
