# import numpy as np;
# import matplotlib.pyplot as plt;
l = [3, 0, 1]

l = l + l[:2]

m = l.sort()

l.pop()

print(m)