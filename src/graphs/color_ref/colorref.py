import time
from src.graphs.modules.graph_io import load_graph
from collections import Counter

class Coloring(object):

  def __init__(self, graphs, color_list, color_classes, iterations, discrete):
    self.graphs = graphs
    self.color_list = color_list
    self.color_classes = color_classes
    self.iterations = iterations
    self.discrete = discrete

  def __eq__(self, other: list[int]):
    return self.color_list == other

  def get_result(self):
    return self.graphs, self.color_classes, self.iterations, self.discrete


def basic_colorref(g):
  graphs = load_graphs(g)
  eq_coloring_list = []

  for index, graph in enumerate(graphs):
    init_color_map = {v: len(v.neighbours) for v in graph.vertices}

    refined_color_map, color_classes, iteration = refine_color_map(init_color_map)

    eq_coloring_list = update_coloring_list(eq_coloring_list, refined_color_map, color_classes, index, iteration)

  return [c.get_result() for c in eq_coloring_list]

def load_graphs(g):
  with open(g) as f:
    G = load_graph(f, read_list=True)
  return G[0]

def refine_color_map(init_color_map):
  color_map = init_color_map
  color_classes = get_color_classes(color_map)
  iteration = 0
  stable = False

  while not stable:
    new_color_map = get_color_map(color_map)
    new_color_classes = get_color_classes(new_color_map)

    stable = color_classes == new_color_classes

    color_map = new_color_map
    color_classes = new_color_classes

    iteration += 1

  return color_map, color_classes, iteration

def get_color_map(color_map):
  return {v: get_neighbourhood_hash(v, color_map) for v in color_map.keys()}

def get_neighbourhood_hash(v, color_map):
  return hash(tuple(sorted(color_map[n] for n in v.neighbours)))

def get_color_classes(color_map):
  return sorted(Counter(color_map.values()).values())

def update_coloring_list(eq_coloring_list, color_map, color_classes, index, iteration):
  color_list = sorted(color_map.values())
  coloring = find_coloring(eq_coloring_list, color_list)

  if coloring:
    coloring.graphs.append(index)
  else:
    eq_coloring_list.append(
        Coloring(
            [index],
            color_list,
            [dict(Counter(color_classes))],
            iteration,
            all(x == 1 for x in color_classes)
        ))
  return eq_coloring_list

def find_coloring(coloring_list, color_list):
  for coloring in coloring_list:
    if coloring == color_list:
      return coloring

def main():
  benchmarks = ["Benchmark_instances/CrefBenchmark1.grl", "Benchmark_instances/CrefBenchmark2.grl",
                "Benchmark_instances/CrefBenchmark3.grl", "Benchmark_instances/CrefBenchmark4.grl",
                "Benchmark_instances/CrefBenchmark5.grl", "Benchmark_instances/CrefBenchmark6.grl"]
  solutions = [[([0, 2], [{1: 3, 2: 312}], 143, False), ([1, 3], [{1: 3, 2: 312}], 188, False)],
               [([0, 2, 4], [{1: 514}], 4, True), ([1, 3], [{1: 514}], 4, True)],
               [([0, 2, 3], [{1: 1026}], 4, True), ([1, 4], [{1: 1026}], 4, True)],
               [([0, 1], [{1: 2050}], 4, True), ([2, 3], [{1: 2050}], 4, True)],
               [([0, 9], [{3: 9}], 3, False), ([1, 6, 7], [{1: 9, 2: 9}], 6, False), ([2, 3, 4], [{3: 9}], 3, False), ([5, 8], [{1: 9, 2: 9}], 6, False)],
               [([0, 1], [{1: 3, 2: 632}], 287, False), ([2, 3, 4], [{1: 3, 2: 632}], 380, False)]]
  for i, benchmark in enumerate(benchmarks):
    start = time.time()
    result = basic_colorref(benchmark)
    elapsed = time.time() - start
    print(f'Benchmark {i + 1}\n{result}\n{result == solutions[i]}\n{elapsed}\n')

if __name__ == "__main__":
  main()
