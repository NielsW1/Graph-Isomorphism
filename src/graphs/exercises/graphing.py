from src.graphs.modules.graph import *
from src.graphs.modules.graph_io import load_graph, save_graph, write_dot

def create_path_graph(n):
  G = Graph(False, n)
  verts = G.vertices
  [G.add_edge(Edge(verts[v], verts[v + 1])) for v in range(n - 1)]
  return G

def create_cycle_graph(n):
  G = Graph(False, n)
  verts = G.vertices
  [G.add_edge(Edge(verts[v], verts[v + 1 if v < n - 1 else 0])) for v in range(n)]
  return G

def add_cycle(G, verts):
  n = len(verts)
  [G.add_edge(Edge(verts[v], verts[v + 1 if v < n - 1 else 0])) for v in range(n)]
  return G

def create_complete_graph(n):
  G = Graph(False, n)
  verts = G.vertices
  [G.add_edge(Edge(verts[u], verts[v])) for u in range(n) for v in range(v + 1, n)]
  return G

def create_2cycle_graph(n, m):
  G = Graph(False, n + m)
  add_cycle(G, G.vertices[:n])
  add_cycle(G, G.vertices[n:])
  return G

def complement(g):
  with open(f'examplegraphs/{g}.gr') as f:
    G = load_graph(f)
  n = len(G.vertices)
  res = copy_vertices(G)

  for u in range(n):
    for v in range(u + 1, n):
      if not G.find_edge(G.vertices[u], G.vertices[v]):
        res.add_edge(Edge(res.vertices[u], res.vertices[v]))

  with open(f'examplegraphs/{g}2.gr', 'w') as f:
    save_graph(res, f)

def copy_vertices(g):
  copy = Graph(False, 0)
  [copy.add_vertex(Vertex(copy, label = v)) for v in g.vertices]
  return copy

def merge_sort_graphs(g1, g2):
  with open(f'examplegraphs/{g1}.gr') as f1:
    G1 = load_graph(f1)
  with open(f'examplegraphs/{g2}.gr') as f2:
    G2 = load_graph(f2)

  vertices = G1.vertices + G2.vertices
  vertices.sort(key = lambda v: len(v.neighbours), reverse=True)
  return vertices

def generate_dot(g):
  with open(f'{g}.grl') as f1:
    G = load_graph(f1)
  with open('../mygraph.dot', 'w') as f:
    write_dot(G, f)

from collections import deque

def breadth_first_search(g):
  with open(f'examplegraphs/{g}.gr') as f:
    G = load_graph(f)

  n = len(G.vertices)
  queue = deque([G.vertices[0]])
  visited_count = 0

  G.vertices[0].set_visited()
  label = 0

  while queue:
    v = queue.popleft()
    v.label = label
    label += 1
    visited_count += 1

    for neighbour in v.neighbours:
      if not neighbour.is_visited():
        neighbour.set_visited()
        queue.append(neighbour)

  with open('../bfs.dot', 'w') as f:
    write_dot(G, f)

  return visited_count == n

def depth_first_search(g):
  with open(f'examplegraphs/{g}.gr') as f:
    G = load_graph(f)

  n = len(G.vertices)
  queue = deque([G.vertices[0]])
  visited_count = 0

  G.vertices[0].set_visited()
  label = 0

  while queue:
    v = queue.pop()
    v.label = label
    label += 1
    visited_count += 1

    for neighbour in v.neighbours:
      if not neighbour.is_visited():
        neighbour.set_visited()
        queue.append(neighbour)

  with open('../dfs.dot', 'w') as f:
    write_dot(G, f)

  return visited_count == n

def depth_first_recursive_search(G, v, label):
  v.set_visited()
  v.label = label
  neighbours = v.neighbours
  if len(neighbours) == 0:
    return
  else:
    for neighbour in neighbours:
      if not neighbour.is_visited():
        depth_first_recursive_search(G, neighbour, label + 1)

def recursive_start(g):
  with open(f'examplegraphs/{g}.gr') as f:
    G = load_graph(f)
  start = G.vertices[0]
  depth_first_recursive_search(G, start, 0)
  with open('../dfs_rec.dot', 'w') as f:
    write_dot(G, f)

print(breadth_first_search("examplegraph"))
print(depth_first_search("examplegraph"))
print(recursive_start("examplegraph"))
generate_dot("SampleGraphsBasicColorRefinement/colorref_smallexample_4_16")





