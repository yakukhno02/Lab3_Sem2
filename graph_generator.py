import random

def generate_adjacency_matrices(n1, n2, n3, n4):
    n = n3 + 10
    seed = int(f"{n1}{n2}{n3}{n4}")
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

    return Adir, Aundir, n
