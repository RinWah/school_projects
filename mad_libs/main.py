'''
adj = input("enter an adjective: ")
noun = input("enter a noun: ")
verb = input("enter a verb: ")

print(f"the {adj} {noun} decided to {verb} today.")
'''

import tkinter as tk

# 1. create the main window
root = tk.Tk()
root.title("mad libs game")

# 2. create labels + entry boxes for each word
adj_label = tk.Label(root, text="adjective:")
adj_label.grid(row=0, column=0, padx=5, pady=5, sticky="e") # what is this? what is sticky lol
adj_entry = tk.Entry(root, width=20)
adj_entry.grid(row=0, column=1, padx=5, pady=5)

noun_label = tk.Label(root, text="noun:")
noun_label.grid(row=1, column=0, padx=5, pady=5, sticky="e") # is this row 1 bc it goes under the adj label?
noun_entry = tk.Entry(root, width=20)
noun_entry.grid(row=1, column=1, padx=5, pady=5)

verb_label = tk.Label(root, text="verb:")
verb_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
verb_entry = tk.Entry(root, width=20)
verb_entry.grid()