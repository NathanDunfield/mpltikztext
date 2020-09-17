import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import mpltikztext
figure, axis = plt.subplots(figsize=(6,6), dpi=150)
xs = 10*np.random.rand(100)
ys = np.exp(xs + np.random.rand(100))
axis.scatter(xs, ys, alpha=0.1)
axis.set_title(r'Giant mess')
axis.set_xlabel(r'$x$')
axis.set_ylabel(r'$y$')
axis.set_yscale('log')
figure.tight_layout()
mpltikztext.savefig(figure, 'log_plot.pdf', path='plots')
figure.savefig('plots/raw_log_plot.pdf')
