import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import mpltikztext
figure, axis = plt.subplots()
xs = np.random.rand(10000)
ys = np.random.rand(10000)
axis.scatter(xs, ys, alpha=0.1)
axis.set_title(r'Giant mess')
axis.set_xlabel(r'$x$')
axis.set_ylabel(r'$y$')
figure.tight_layout()
mpltikztext.savefig(figure, 'scatter.png', path='plots')
figure.savefig('plots/raw_scatter.png')



