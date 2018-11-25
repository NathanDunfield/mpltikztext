import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import mpltikztext

figure, axis = plt.subplots()
t = np.arange(0.0,3.0,0.01)
axis.plot(t, np.sin(2*np.pi*t))
axis.set_title(r'Plot of $\sin(t)$')
axis.set_xlabel(r'$t$')
axis.set_ylabel(r'$\sin(t)$')
figure.tight_layout()
mpltikztext.savefig(figure, 'sine_wave.pdf', path='plots')
figure.savefig('plots/raw_figure.pdf')

