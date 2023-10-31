import numpy as np

a = np.array([[i, i+1] for i in range(0, 10, 2)])
v1 = a[[0, 1, 2],:]
print(v1)