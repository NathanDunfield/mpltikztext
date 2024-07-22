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
    if not text.get_visible():
        return ''
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
    if '\n' in text_str:
        horvert = ','.join([horvert,
                            'align=' + text.get_horizontalalignment()])
        text_str = text_str.replace('\n', ' \\\\\n')
    return "  \\draw (%.6f, %.6f) node[%s] {%s};" % (x, y,
                                                     horvert.strip(),
                                                     text_str)

def save_without_text(figure, filename, **kwargs):
    """
    Saves the figure with all the text removed. It does so by setting
    the opacity alpha to 0 for each Text artist.  I also tried
    "set_visible(False)" which mostly works but things can move
    slightly.
    """
    kwargs['transparent'] = True
    figure.savefig(filename, **kwargs)  # Hack to finalize the figure.
    texts = active_texts(figure)
    alphas = dict()
    for text in texts:
        alphas[text] = text.get_alpha()
        text.set_alpha(0.0)
    figure.savefig(filename, **kwargs)
    for text in texts:
        text.set_alpha(alphas[text])

def record_data_coor_sys_for_tikz(axis):
    if axis.xaxis.get_scale() == 'log' or axis.yaxis.get_scale() == 'log':
        return "  % No internal axis coordinate system as there is a log scale."
    data_to_tikz = axis.transData + display_to_tikz(axis.figure)
    shift = data_to_tikz.transform([0.0, 0.0])
    delta = data_to_tikz.transform([1.0, 1.0]) - shift
    dL = axis.dataLim
    data_rect = (dL.x0, dL.y0, dL.x1, dL.y1)
    content =  "  % Internal axis coordinate system\n"
    content += "  \\begin{scope}[shift={(%.8f, %.8f)},\n" % tuple(shift)
    content += "                xscale=%.8f, yscale=%.8f]\n" % tuple(delta)
    content += "      %"
    content += "\\draw[red] (%.6f, %.6f) rectangle (%.6f, %.6f);\n" % data_rect
    content += "  \\end{scope}"
    return content


def save_matplotlib_for_paper(figure, file_name, path='plots/', image_only=False, **kwargs):
    """
    Saving a matplotlib figure for use in a paper.  The given filename
    can be of type ".pdf" or ".png" as appropriate.  The graphics
    are saved in the subdirectory "images" of the given "path" with
    the TikZ code itself is saved in a corresponding ".tex" file in "path".

    If image_only==True, then it doesn't save the TikZ overlay file,
    just underlying image.  This is useful if you have hand-edited the
    TikZ file already but want to (slightly) tweak the matplotlib
    figure.
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
    save_without_text(figure, image_file, **kwargs)

    # Make TikZ overlay
    contents = "%Set \graphicspath{{plots/images/}} to include the image files\n"
    contents += "\\begin{tikzoverlay*}[width=0.8\\textwidth]{%s}\n" % (file_name,)
    tikz_commands = [convert_text_to_tikz(text) for text in active_texts(figure)]
    tikz_commands += [record_data_coor_sys_for_tikz(axis) for axis in figure.axes]
    contents += "\n".join(tikz_commands)
    contents += "\n\\end{tikzoverlay*}"
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
