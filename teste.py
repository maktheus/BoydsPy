from numpy.random import default_rng
rng = default_rng()
print(rng)
vals = rng.integers(low=0, high=100)
print(vals)

more_vals = rng.standard_normal(10)
print(more_vals)