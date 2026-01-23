from pysat.solvers import Glucose3

A = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
]

n = 3
k = 2
start = 0
end = 2


def p(t, i):
    return t * n + i + 1


solver = Glucose3()

solver.add_clause([p(0, start)])
for i in range(n):
    if i != start:
        solver.add_clause([-p(0, i)])

solver.add_clause([p(k, end)])

for t in range(k + 1):

    solver.add_clause([p(t, i) for i in range(n)])

    for i in range(n):
        for j in range(i + 1, n):
            solver.add_clause([-p(t, i), -p(t, j)])

for t in range(k):
    for i in range(n):
        for j in range(n):
            if A[i][j] == 0:
                solver.add_clause([-p(t, i), -p(t + 1, j)])

if solver.solve():
    print("SAT: Path exists")

    model = solver.get_model()

    path = {}
    for v in model:
        if v > 0:
            v -= 1
            t = v // n
            i = v % n
            path[t] = i

    print("Path:", [path[t] for t in range(k + 1)])

else:
    print("UNSAT: No path exists")

solver.delete()

