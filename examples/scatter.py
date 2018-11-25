import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import mpltikztext
figure, axis = plt.subplots(figsize=(6,6), dpi=150)
xs = np.random.rand(10000) + 1
ys = np.random.rand(10000) + 2
axis.scatter(xs, ys, alpha=0.1)
axis.set_title(r'Giant mess')
axis.set_xlabel(r'$x$')
axis.set_ylabel(r'$y$')
axis.set_aspect('equal')
figure.tight_layout()
mpltikztext.savefig(figure, 'scatter.jpg', path='plots')
figure.savefig('plots/raw_scatter.jpg')



