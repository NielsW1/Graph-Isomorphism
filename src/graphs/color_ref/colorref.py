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
  coloring_list = []

  for index, graph in enumerate(graphs):
    color_map = {v: len(v.neighbours) for v in graph.vertices}
    color_classes = get_color_classes(color_map)

    stable = False
    iteration = 0

    while not stable:
      new_color_map = refine_color_map(color_map)
      new_color_classes = get_color_classes(new_color_map)

      stable = color_classes == new_color_classes

      color_map = new_color_map
      color_classes = new_color_classes
      iteration += 1

    if iteration == 1:
      iteration = 0

    coloring_list = update_coloring_list(coloring_list, color_map, color_classes, index, iteration)

  return [c.get_result() for c in coloring_list]

def load_graphs(g):
  with open(g) as f:
    G = load_graph(f, read_list=True)
  return G[0]

def refine_color_map(color_map):
  return {v: get_neighbourhood_hash(v, color_map) for v in color_map.keys()}

def get_neighbourhood_hash(v, color_map):
  return hash(tuple(sorted(color_map[n] for n in v.neighbours)))

def get_color_classes(color_map):
  return sorted(Counter(color_map.values()).values())

def update_coloring_list(coloring_list, color_map, color_classes, index, iteration):
  color_list = sorted(color_map.values())
  coloring = find_isomorphs(coloring_list, color_list)

  if coloring:
    coloring.graphs.append(index)
  else:
    coloring_list.append(
        Coloring(
            [index],
            color_list,
            color_classes,
            iteration,
            all(x == 1 for x in color_classes)
        ))
  return coloring_list

def find_isomorphs(coloring_list, color_list):
  for coloring in coloring_list:
    if coloring == color_list:
      return coloring

def main():
  current = time.time()
  # print(basic_colorref(
  #     "SampleGraphsBasicColorRefinement/colorref_smallexample_4_16.grl"))
  # print(basic_colorref("SampleGraphsBasicColorRefinement/colorref_largeexample_4_1026.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark1.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark2.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark3.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark4.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark5.grl"))
  print(basic_colorref("Benchmark_instances/CrefBenchmark6.grl"))
  print(time.time() - current)

if __name__ == "__main__":
  main()
