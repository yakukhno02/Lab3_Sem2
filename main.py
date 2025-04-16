import tkinter as tk
from graph_generator import generate_adjacency_matrices
from drawGraph import draw_graph


n1, n2, n3, n4 = 4, 1, 3, 3
Adir, Aundir, n = generate_adjacency_matrices(n1, n2, n3, n4)

print("Матриця для напрямленого графа:")
for row in Adir:
    print(" ".join(map(str, row)))

print("\nМатриця для ненапрямленого графа:")
for row in Aundir:
    print(" ".join(map(str, row)))

root = tk.Tk()
root.title("Графи")
canvas = tk.Canvas(root, width=1300, height=600, bg="white")
canvas.pack()

draw_graph(canvas, Adir, directed=True, n=n, offset_x=0)
draw_graph(canvas, Aundir, directed=False, n=n, offset_x=650)

canvas.create_text(325, 20, text="Напрямлений граф", font=("Arial", 14, "bold"))
canvas.create_text(975, 20, text="Ненапрямлений граф", font=("Arial", 14, "bold"))

root.mainloop()
