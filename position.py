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
