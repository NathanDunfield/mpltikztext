""" 
Saving Matplotlib figures so that all text becomes a TikZ overlay, and
hence is easily editable from within LaTeX to match the document style.
"""

import matplotlib as mpl
import numpy as np
from collections import Counter, defaultdict
import os

def active_texts(figure):
    """ 
    Return all nonempty Texts that are actually being drawn. When
    making axis labels, matplotlib throws in labels beyond the current
    x/y-bounds and for sides of the axes that are not currently
    labeled, but disables them so they are not shown.
    """
    texts = figure.findobj(mpl.text.Text)
    return [T for T in texts if T.get_text() and T._renderer is not None]

def display_to_tikz(figure):
    """ 
    In the TikZ overlay, the horizontal coordinate ranges from 0 to
    100 and the vertical coordinate ranges from 0 to 100/A where A is
    the aspect ratio (width/height). This function returns the
    tranformation *from* the display coordinates of the matplotlib
    figure *to* the TikZ overlay coordinates.
    """
    D = figure.transFigure  # figure -> display
    assert all(D.transform([0, 0]) == 0)
    width, height = D.transform([1, 1])
    A = 100.0/width
    return mpl.transforms.Affine2D(np.diag([A, A, 1.0]))

def tikz_position(artist):
    """
    Returns the position of the artist in the TikZ coordinate system.
    """
    figure = artist.get_figure() 
    artist_to_tikz = artist.get_transform() + display_to_tikz(figure)
    return artist_to_tikz.transform(artist.get_position())

def convert_text_to_tikz(text):
    # Get TikZ node options
    horizontal = {'left':'right',
                  'center':'',
                  'right':'left'}[text.get_horizontalalignment()]
    vertical = {'top':'below',
                'bottom':'above',
                'center':'',
                'baseline':'',
                'center_baseline':''}[text.get_verticalalignment()]
    horvert = vertical + ' ' + horizontal
    if text.get_rotation():
        horvert = 'rotate=%.1f' % text.get_rotation()
    # Clean up the string itself.
    text_str = text.get_text().replace(r'\mathdefault', '').replace(u'\u2212', '-')
    try:  # Make tick labels in mathmode.
        float(text_str)
        text_str = '$' + text_str + '$'
    except ValueError:
        pass
    # Get the TikZ coordinates
    x, y = tikz_position(text)
    return "  \\draw (%.6f, %.6f) node[%s] {%s};" % (x, y, horvert.strip(), text_str)

def save_without_text(figure, filename):
    """
    Saves the figure with all the text removed. It does so by setting
    the opacity alpha to 0 for each Text artist.  I also tried
    "set_visible(False)" which mostly works but things can move
    slightly.
    """
    figure.savefig(filename)  # Hack to finalize the figure. 
    texts = active_texts(figure)
    alphas = dict()
    for text in texts:
        alphas[text] = text.get_alpha()
        text.set_alpha(0.0)
    figure.savefig(filename)
    for text in texts:
        text.set_alpha(alphas[text])

def save_matplotlib_for_paper(figure, file_name, path='plots/'):
    """
    Saving a matplotlib figure for use in a paper.  The given filename
    can be of type ".pdf" or ".png" as appropriate.  The graphics
    are saved in the subdirectory "images" of the given "path" with 
    the TikZ code itself is saved in a corresponding ".tex" file in "path".  
    """
    # Setup paths
    image_path = os.path.join(path, 'images')
    base_name = os.path.splitext(file_name)[0]
    image_file = os.path.join(image_path, file_name)

    # Create target directories if they do not exist
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(image_path):
        print('Creating directory "%s"' % os.path.abspath(image_path))
        os.mkdir(image_path)

    # Save the image
    save_without_text(figure, image_file)

    # Make TikZ overlay
    contents =  "\\begin{tikzoverlay}[width=\\matplotlibfigurewidth]{%s}[\\matplotlibfigurefont]\n" % (image_file,)
    contents += "\n".join([convert_text_to_tikz(text) for text in active_texts(figure)])
    contents += "\n\\end{tikzoverlay}\n"

    # Save to TeX file.
    texname = os.path.join(path, base_name + '.tex')
    texfile = open(texname, 'w')
    texfile.write(contents + '\n')
    texfile.close()

def matplotlib_with_opts_matching_save(sage_graphic, **kwds):
    """
    SageMath only: The method Graphics.matplotlib doesn't produce the same
    matplotlib.Figure as is used in Graphics.save/Graphics.show.  This
    function matches what Graphics.save does.  It hasn't been tested
    in some time.
    """
    options = sage_graphic.SHOW_OPTIONS.copy()
    options.update(sage_graphic._extra_kwds)
    options.update(kwds)
    for opt in ['dpi', 'transparent', 'fig_tight']:
        options.pop(opt)
    figure = sage_graphic.matplotlib(**options)
    figure.set_canvas(FigureCanvasAgg(figure))
    figure.tight_layout()
    return figure
              
    
    


