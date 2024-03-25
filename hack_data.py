pts = [
    (3, 2), (4.5, 2), (2, 4.5), (2, 3),
    (-2, 3), (-2, 4.5), (-4.5, 2), (-3, 2),
    (-3, -2), (-4.5, -2), (-2, -4.5), (-2, -3),
    (2, -3), (2, -4.5), (4.5, -2), (3, -2),
    (3, 2)
]

import matplotlib.pyplot as plt
plt.axis('equal')
plt.axis('off')
plt.plot([x for x, y in pts], [y for x, y in pts], c='k')
plt.show()
