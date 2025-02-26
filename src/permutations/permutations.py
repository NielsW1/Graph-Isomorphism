from src.permutations.permutations import *

# q = test_permutation(20)
# print(q)
#
# p = [1, 2, 3, 0, 5, 4, 6, 7, 8, 9]
# print(p)
# print_permutation(p)
# print(is_trivial(p))
# print(p[0])
# print(cycles(p))
# r = trivial_permutation(10)
# print(r)
#
# print_permutation(r)
# print(r[0])
# print(is_trivial(r))

# p = permutation_from_cycles(10, [[0, 1, 2, 3], [4, 5]])
# print(p)
# print_permutation(p)

def composition(p, q):
  if len(p) != len(q):
    raise ValueError("Permutations must have the same length")

  return [p[q[i]] for i in range(len(p))]

p = [1, 2, 3, 0, 5, 6, 4, 8, 7]
print_permutation(p)
q = composition(p, p)
print_permutation(q)

def inverse(p):
  n = len(p)
  inverse = [0] * n

  for i in range(n):
    inverse[p[i]] = i

  return inverse

inv = inverse(p)
print_permutation(inv)

def power(p, i):
  comp = list(range(len(p)))
  for _ in range(i):
    comp = composition(comp, p)

  return comp

powa = power(p, 5)
print_permutation(powa)

print_permutation(test_permutation(10))




