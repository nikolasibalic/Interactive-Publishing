"""
    Specifies figure design, colour scheme, and provides functions
    for representing complex numbers (phase-amplitude mapps to color-intensity).
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import numpy as np
import colorsys
from PIL import Image

mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['xtick.major.size'] = 8
mpl.rcParams['ytick.major.size'] = 8
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['savefig.transparent'] = True

mpl.rcParams["text.latex.preamble"]  = r"\usepackage{amsmath} \usepackage{amssymb} \usepackage{color} \usepackage[bitstream-charter]{mathdesign}"
mpl.rcParams["text.usetex"] = True

def presentationMode(switch, fontsize=10, linewidth=1.5):
    if switch:
        c1 = "black"
        c2 = "white"
        mpl.rcParams['font.family'] = 'sans-serif'
    else:
        c1 = "white"
        c2 = "black"
    mpl.rcParams['axes.facecolor'] = c1
    mpl.rcParams['axes.edgecolor'] = c2
    mpl.rcParams['axes.labelcolor'] = c2
    mpl.rcParams['xtick.color'] = c2
    mpl.rcParams['ytick.color'] = c2
    mpl.rcParams['figure.facecolor'] = c1
    mpl.rcParams['font.size'] = fontsize
    mpl.rcParams['lines.linewidth'] = linewidth
    mpl.rcParams['axes.linewidth'] = linewidth * 0.8 / 1.5
    mpl.rcParams['xtick.major.width'] = linewidth * 0.8 / 1.5
    mpl.rcParams['xtick.minor.width'] = linewidth * 0.6 / 1.5
    mpl.rcParams['ytick.major.width'] = linewidth * 0.8 / 1.5
    mpl.rcParams['ytick.minor.width'] = linewidth * 0.6 / 1.5

#: Durham colour scheme
cDUp = "#7E317B"  # Palatinate Purple
cDUpp =  "#D8ACF4"  # Light purple

cDUb = "#006388"  # Blue
cDUbb = "#91B8BD"  # Mid Blue
cDUbbb = "#C4E5FA"  # Light Blue
cDUbbbb = "#00AEEF"

cDUsky = "#A5C8D0"  # sky blue

cDUo = "#9FA161"  # Olive Green

cDUr = "#AA2B4A"  # Red
cDUrr = "#BE1E2D"
cDUy = "#E8E391" #  Yellow

cDUp = "#C43B8E" # Pink

cDUk = "#231F20"  # Black
cDUkk = "#002A41" # ink

cDUggg = "#CFDAD1"  # Near White/L. Grey
cDUgg = "#968E85"  # Warm Grey
cDUg = "#6E6464"  # midgrey


#: Aarhus color scheme from
# http://medarbejdere.au.dk/en/administration/communication/guidelines/guidelinesforcolours/
cAUn = "#003d73"
cAUnn = "#002546"
cAUb = "#003d73"
cAUbb = "#003e5c"
cAUv = "#655a9f"
cAUvv = "#281c41"
cAUt = "#00aba4"
cAUtt = "#004543"
cAUg = "#8bad3f"
cAUgg = "#425821"
cAUy = "#fabb00"
cAUyy = "#634b03"
cAUo = "#ee7f00"
cAUoo = "#5f3408"
cAUr = "#e2001a"
cAUrr = "#5b0c0c"
cAUv = "#e2007a"
cAUvv = "#5f0030"
cAUg = "#878787"
cAUgg = "#4b4b4a"


def make_colormap(seq):
    """
        Args:
            seq: a sequence of floats and RGB-tuples. The floats should be
                increasing and in the interval (0,1).

        Returns:
            a LinearSegmentedColormap
    """
    seq = [(None, ) * 3, 0.0] + list(seq) + [1.0, (None, ) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


c = mcolors.ColorConverter().to_rgb
rvb = make_colormap([
    c('#b20000'),
    c('#fe7600'), 0.125,
    c('#fe7600'),
    c('#feca00'), 0.25,
    c('#feca00'),
    c('#bcfd00'), 0.375,
    c('#bcfd00'),
    c('#06a133'), 0.5,
    c('#06a133'),
    c('#00f6fd'), 0.625,
    c('#00f6fd'),
    c('#000cfe'), 0.75,
    c('#000cfe'),
    c('#e404fe'), 0.875,
    c('#e404fe'),
    c('#b20000')
])

# 321F20  968E85


def getColor(amplitude, phase, maxAmplitude):
    c = rvb(phase / (2. * np.pi))
    scale = amplitude / maxAmplitude
    if scale > 1:
        raise ValueError(
            'Amplitude of the passed complex number is bigger than the'
            ' maximal set amplitudeyter not')
    cc = colorsys.rgb_to_hls(c[0], c[1], c[2])
    c = colorsys.hls_to_rgb(cc[0], cc[1] + (1. - scale) * (1. - cc[1]), cc[2])
    return (c[0], c[1], c[2], 1.0)


def getComplexColor(complexNo:complex, maxAmplitude:float):
    """
    Get color for a complex numbers

    Represents phase as continuous colour wheel, and amplitude as intensity
    of color (zero amplitude = white color), with linear mapping in between.

    Args:
        complexNo (complex float): complex number
        maxAmplitude (float): maximum amplitude in the data set we want to
            represent as colour mapped dots. This is used for normalizing color
            intensity, going from maximal saturation or `maxAmplitude` to
            white color for zero amplitude.

    Returns:
        color as [red, green, blue, alpha]
    """
    angle = np.angle(complexNo)
    if angle < 0:
        angle += 2 * np.pi
    return getColor(np.absolute(complexNo), angle, maxAmplitude)

def white_to_transparency(img):
    """
        Converts white areas of image to transparency.
    """
    x = np.asarray(img.convert('RGBA')).copy()

    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)
