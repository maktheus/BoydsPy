from numpy.random import default_rng
rng = default_rng()
print(rng)
vals = rng.integers(low=0, high=100)
vals2 = rng.integers(low=0, high=100)

print(vals)
print(vals2)

more_vals = rng.standard_normal(10)
print(more_vals)