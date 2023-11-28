from location import location
from graph import graph

def create_graph():
    # Create Locations
    a = location("A")
    b = location("B")
    c = location("C")
    d = location("D")
    e = location("E")
    f = location("F")
    g = location("G")
    h = location("H")
    i = location("I")
    j = location("J")
    k = location("K")
    l = location("L")
    m = location("M")
    n = location("N")
    o = location("O")
    p = location("P")
    q = location("Q")
    r = location("R")
    s = location("S")
    t = location("T")
    u = location("U")
    v = location("V")
    w = location("W")
    x = location("X")
    y = location("Y")
    z = location("Z")

    # Create Neighbors (Arcs)
    a.add_neighbor(b, 19)
    a.add_neighbor(u, 6)

    b.add_neighbor(c, 18)

    c.add_neighbor(d, 22)
    c.add_neighbor(w, 7)

    d.add_neighbor(e, 23)

    e.add_neighbor(f, 11)
    e.add_neighbor(o, 8)
    e.add_neighbor(y, 8)

    f.add_neighbor(g, 6)

    g.add_neighbor(h, 8)
    g.add_neighbor(q, 5)

    h.add_neighbor(i, 9)

    i.add_neighbor(j, 10)
    i.add_neighbor(s, 4)

    j.add_neighbor(a, 9)
    j.add_neighbor(k, 7)
    j.add_neighbor(z, 8)

    k.add_neighbor(j, 11)
    k.add_neighbor(l, 6)
    k.add_neighbor(u, 8)

    l.add_neighbor(k, 2)
    l.add_neighbor(m, 7)
    l.add_neighbor(s, 10)
    l.add_neighbor(u, 11)

    m.add_neighbor(l, 5)
    m.add_neighbor(n, 9)
    m.add_neighbor(r, 5)

    n.add_neighbor(m, 4)
    n.add_neighbor(o, 4)

    o.add_neighbor(e, 12)
    o.add_neighbor(n, 2)
    o.add_neighbor(p, 7)
    o.add_neighbor(x, 3)

    p.add_neighbor(o, 9)
    p.add_neighbor(q, 5)

    q.add_neighbor(g, 7)
    q.add_neighbor(p, 4)
    q.add_neighbor(r, 2)

    r.add_neighbor(m, 2)
    r.add_neighbor(q, 8)
    r.add_neighbor(s, 6)

    s.add_neighbor(i, 11)
    s.add_neighbor(l, 8)
    s.add_neighbor(r, 5)
    s.add_neighbor(t, 4)

    t.add_neighbor(k, 6)

    u.add_neighbor(a, 15)
    u.add_neighbor(k, 9)
    u.add_neighbor(l, 9)
    u.add_neighbor(v, 10)

    v.add_neighbor(u, 9)
    v.add_neighbor(w, 7)

    w.add_neighbor(c, 13)
    w.add_neighbor(v, 7)
    w.add_neighbor(x, 3)

    x.add_neighbor(o, 7)
    x.add_neighbor(w, 6)

    # y.add_neighbor()

    # z.add_neighbor()

    locations = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z]

    # Create graph
    newGraph = graph()
    for newLocation in locations:
        newGraph.add_location(newLocation)
    return newGraph

def path_to_string(path):
    pathString = "["
    for i in path:
        pathString = f"{pathString}{i.get_name()}, "
    if len(path) > 0:
        pathString = f"{pathString[:-2]}]"
    else:
        pathString = f"{pathString}]"
    return pathString

newGraph = create_graph()
newGraph.set_q_values(100)
for eachLocation in newGraph.get_locations():
    print(eachLocation)
print('~'*75)

rand = newGraph.get_random_location()
print(f'Destination: {rand}')
newGraph.q_learning(rand)
for x in newGraph.get_locations():
    dfs_path, dfs_cost = newGraph.depth_first_search(x, rand)
    print(f"DFS:\t{x.get_name()} -> {rand.get_name()} = {path_to_string(dfs_path)}, {dfs_cost}")
    q_path, q_cost = newGraph.get_shortest_path(x, rand)
    print(f"Q:\t{x.get_name()} -> {rand.get_name()} = {path_to_string(q_path)}, {q_cost}\n")
    