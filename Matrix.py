import tkinter as tk
import random
import math

n1, n2, n3, n4 = 4, 1, 3, 3
n = n3 + 10
seed = int(f"{n1}{n2}{n3}{n4}")  # 4133
k = 1.0 - n3 * 0.02 - n4 * 0.005 - 0.25

random.seed(seed)
Adir = []
for i in range(n):
    row = []
    for j in range(n):
        value = random.uniform(0, 2.0) * k
        row.append(1 if value >= 1.0 else 0)
    Adir.append(row)

Aundir = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        Aundir[i][j] = Aundir[j][i] = max(Adir[i][j], Adir[j][i])

print("Матриця напрямленого графа:")
for row in Adir:
    print(" ".join(map(str, row)))

print("\nМатриця ненапрямленого графа:")
for row in Aundir:
    print(" ".join(map(str, row)))

def get_frame_positions(n, offset_x, offset_y, spacing_x, spacing_y):
    cols, rows = 5, 4
    positions = []

    for col in range(cols):
        if len(positions) < n:
            positions.append((offset_x + col * spacing_x, offset_y))

    for row in range(1, rows - 1):
        if len(positions) < n:
            positions.append((offset_x + (cols - 1) * spacing_x, offset_y + row * spacing_y))

    for col in reversed(range(cols)):
        if len(positions) < n:
            positions.append((offset_x + col * spacing_x, offset_y + (rows - 1) * spacing_y))

    for row in reversed(range(1, rows - 1)):
        if len(positions) < n:
            positions.append((offset_x, offset_y + row * spacing_y))
    return positions

def intersects_vertex(p1, p2, center, r):
    x0, y0 = center
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    a = dx**2 + dy**2
    b = 2 * (dx * (x1 - x0) + dy * (y1 - y0))
    c = (x1 - x0)**2 + (y1 - y0)**2 - r**2
    disc = b**2 - 4 * a * c
    if disc < 0:
        return False
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    return (0 < t1 < 1) or (0 < t2 < 1)

def draw_graph(canvas, matrix, directed, offset_x=0):
    vertex_radius = 20
    positions = get_frame_positions(n, offset_x=100 + offset_x, offset_y=100, spacing_x=120, spacing_y=100)

    for i, (x, y) in enumerate(positions):
        canvas.create_oval(x - vertex_radius, y - vertex_radius,
                           x + vertex_radius, y + vertex_radius,
                           fill="lightblue", width=2)
        canvas.create_text(x, y, text=str(i+1), font=("Arial", 10, "bold"))

    for i in range(n):
        for j in range(n):
            if not directed and i != j and j < i:
                continue

            if matrix[i][j]:
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                if i == j:
                    loop_offset = vertex_radius + 15

                    if x1 == min(p[0] for p in positions):
                        lx, ly = x1 - loop_offset, y1
                        start_angle = 0
                    elif x1 == max(p[0] for p in positions):
                        lx, ly = x1 + loop_offset, y1
                        start_angle = 180
                    elif y1 == min(p[1] for p in positions):
                        lx, ly = x1, y1 - loop_offset
                        start_angle = 270
                    elif y1 == max(p[1] for p in positions):
                        lx, ly = x1, y1 + loop_offset
                        start_angle = 90
                    else:
                        lx, ly = x1 + loop_offset * 0.7, y1 - loop_offset * 0.7
                        start_angle = 315

                    arc_radius = 15
                    arc_box = (lx - arc_radius, ly - arc_radius, lx + arc_radius, ly + arc_radius)
                    canvas.create_arc(*arc_box, start=start_angle,
                                      extent=350, style=tk.ARC, width=2)

                    if directed:
                        end_angle = start_angle + 290
                        angle_rad = math.radians(end_angle)
                        end_x = lx + arc_radius * math.cos(angle_rad)
                        end_y = ly - arc_radius * math.sin(angle_rad)
                        arrow_dx = x1 - end_x
                        arrow_dy = y1 - end_y
                        arrow_len = math.hypot(arrow_dx, arrow_dy)
                        arrow_dx /= arrow_len
                        arrow_dy /= arrow_len
                        arrow_end_x = end_x + arrow_dx * 10
                        arrow_end_y = end_y + arrow_dy * 10
                        canvas.create_line(end_x, end_y, arrow_end_x, arrow_end_y,
                                           arrow=tk.LAST, width=2)
                    continue

                dx = x2 - x1
                dy = y2 - y1
                dist = math.hypot(dx, dy)
                norm_dx = dx / dist
                norm_dy = dy / dist
                start_x = x1 + norm_dx * vertex_radius
                start_y = y1 + norm_dy * vertex_radius
                end_x = x2 - norm_dx * vertex_radius
                end_y = y2 - norm_dy * vertex_radius

                blocked = False
                for k, (cx, cy) in enumerate(positions):
                    if k != i and k != j:
                        if intersects_vertex((start_x, start_y), (end_x, end_y), (cx, cy), vertex_radius + 3):
                            blocked = True
                            break

                if blocked:
                    mx, my = (start_x + end_x) / 2, (start_y + end_y) / 2
                    offset = 70
                    mx += -norm_dy * offset
                    my += norm_dx * offset

                    canvas.create_line(start_x, start_y,
                                       mx, my,
                                       end_x, end_y,
                                       width=2,
                                       arrow=(tk.LAST if directed else None),
                                       smooth=True, splinesteps=36)
                else:
                    canvas.create_line(start_x, start_y, end_x, end_y,
                                       width=2,
                                       arrow=(tk.LAST if directed else None))

root = tk.Tk()
root.title("Графи")
canvas = tk.Canvas(root, width=1300, height=600, bg="white")
canvas.pack()

draw_graph(canvas, Adir, directed=True, offset_x=0)
draw_graph(canvas, Aundir, directed=False, offset_x=650)

canvas.create_text(325, 20, text="Напрямлений граф", font=("Arial", 14, "bold"))
canvas.create_text(975, 20, text="Ненапрямлений граф", font=("Arial", 14, "bold"))

root.mainloop()