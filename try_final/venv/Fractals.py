from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageEnhance, ImageFont
import matplotlib.pyplot as plt
from MandlebrotSet import *
from harmonograph import *
from colorharmon import *
from Julia import *
from RectSierpinski import *
from Tricircle import *
from Carpet import *
from SlideShow import *
from AnimateSierpinski import *
from AnimateDragon import *
from HilbertCurve import *
from MandelRayBulb import *
from SurfaceTriangulation import *
import tkinter.font as font
from turtle import *
from random import randint
from colorsys import hsv_to_rgb
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from numba import jit
import plotly
from plotly.offline import init_notebook_mode
import colorsys
import os


def anim_surfacetriangulation():
    xs = []
    ys = []
    zs = []
    data_test = []
    for angle in [[3, 0, 0], [0, 3, 0], [0, 0, 3], [-3, 0, 0], [0, -3, 0], [0, 0, -3]]:
        xs_, ys_, zs_ = plot_mandelbulb(degree=9, height=100, width=100, observer_position=np.array(angle))
        xs.extend(xs_)
        ys.extend(ys_)
        zs.extend(zs_)

    pd.set_option('display.max_rows', None)
    df = pd.DataFrame({'X': xs, 'Y': ys, 'Z': zs}).sort_values(by=['Z'])

    pts = df.values
    print(np.shape(pts))

    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)

    # https://plot.ly/python/reference/#mesh3d
    mesh = go.Mesh3d(x=xs,
                     y=ys,
                     z=zs,
                     alphahull=25,
                     opacity=0.9,
                     colorscale='Viridis'
                     # color='#00FFFF'
                     )

    data = [mesh]
    fig = go.Figure(data=data)
    plot(fig, filename='Alphahull.html', auto_open=True)
# end def animSurfaceTriangulation():

def anim_mandelraybulb():
    np.array(plot_mandelbulb())

    plotly_trace = go.Heatmap(z=np.array(plot_mandelbulb()))

    data = [plotly_trace]

    layout = go.Layout(
        title='Mandelbrot Plot',
        width=1250,
        height=1250,
    )

    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="MandelBulb.html")
# end anim_mandelraybulb():

def anim_random():
    #   Random Walk, in glorious Technicolour
    #   https://docs.python.org/3/library/turtle.html
    #   Authour: Alan Richmond, Python3.codes

    step = 30  # length of each step
    nsteps = 2000  # number of steps
    hinc = 1.0 / nsteps  # hue increment
    width(2)  # width of line

    (w, h) = screensize()  # boundaries of walk
    speed('fastest')
    colormode(1.0)  # colours 0:1 instead of 0:255
    bgcolor('black')  # black background
    hue = 0.0
    for i in range(nsteps):
        setheading(randint(0, 359))
        #   https://docs.python.org/2/library/colorsys.html
        color(hsv_to_rgb(hue, 1.0, 1.0))  # pen colour in RGB
        hue += hinc  # change colour
        forward(step)  # step along!
        (x, y) = pos()  # where are we?
        if abs(x) > w or abs(y) > h:  # if at boundary
            backward(step)  # step back
    done()

    self.clearScreen()
# end anim_random():

def anim_color_harmon():
    """Call the harmongraph script"""
    color_harmon()
    self.clearScreen()
# end anim_color_harmon():

def anim_harmon():
    """Call the harmongraph script"""
    harmon()
    self.clearScreen()


# end anim_harmon():

def anim_slideshow(self):
    # taken from: https://github.com/Tikolu/fractal.py

    # check height
    try:
        h = int(self.height_ent.get())
    except Exception as e:
        err = True
        self.err2show.set("Resize Height value is missing or invalid")

    # check width
    try:
        w = int(self.width_ent.get())
    except Exception as e:
        err = True
        self.err2show.set("Resize Width value is missing or invalid")

    # get user input
    h = self.height_ent.get()
    w = self.width_ent.get()
    um = self.iterfrq.get()

    # set default values
    h = 300 if h == "" else int(h)
    w = 300 if w == "" else int(w)
    um = 300 if um == "" else int(um)

    # call the slideshow
    tikolu(h,
           w,
           um)

    self.clearScreen()


# end def anim_slideshow():

def anim_hilbert(self):
    # Global parameters

    width = 450

    title = "Hilbert-Curve-II"
    axiom = "X"
    rules = {"X": "XFYFX+F+YFXFY-F-XFYFX", "Y": "YFXFY-F-XFYFX+F+YFXFY"}
    iterations = self.iterhlb.get()
    angle = 90
    y_offset = -190
    angle_offset = 0
    speed = self.iterspeed_hlb.get()

    if self.color_to_change == None:
        self.color_to_change = 'maroon'

    hilbert_curve(iterations, axiom, rules, angle, speed, aspect_ratio=1, width=width,
                  offset_angle=angle_offset, y_offset=y_offset, color=self.color_to_change)

    self.clearScreen()


# end def anim_hilbert():

def anim_dragon(self):
    # Global parameters

    width = 450

    title = "TerDragon-Curve"
    axiom = "F"
    rules = {"F": "F-F+F"}
    iterations = self.iterdrgn.get()
    angle = 120
    # c = 'purple'
    speed=self.iterdrgn.get()
    fill = self.fill_dragon.get()

    offset_angle = 90 - 30 * iterations
    correction_angle = 180 - 30 * iterations

    if self.color_to_change == None:
        self.color_to_change = 'magenta'

    animate_dragon(iterations, axiom, rules, angle, speed, fill, correction_angle=correction_angle,
                   offset_angle=offset_angle, width=width, height=width, color=self.color_to_change)

    self.clearScreen()
# end def anim_dragon():

def anim_sierpinski(self):
    # Global parameters

    width = 450

    title = "Siepinski-Sieve"
    axiom = "FXF--FF--FF"
    rules = {"F": "FF", "X": "--FXF++FXF++FXF--"}
    iterations = self.itersier.get()  # TOP: 8
    angle = 60
    speed = self.iterspeed_sier.get()
    fill = self.fill_sier.get()

    if self.color_to_change == None:
        self.color_to_change = 'navy'

    animate_sierpinski(iterations, axiom, rules, angle, speed, fill, aspect_ratio=1, width=width, color=self.color_to_change)

    self.clearScreen()


# end anim_sierpinski():

def make_carpet(self):
    a = np.array([0, 0])
    b = np.array([3, 0])
    c = np.array([3, 3])
    d = np.array([0, 3])

    # set the iterations
    iterations = self.itercarp.get()

    # set the colors
    if self.color1_to_change is None:
        c1 = 'maroon'
    else:
        c1 = self.color1_to_change

    if self.color2_to_change is None:
        c2 = (random.random(), random.random(), random.random())
    else:
        c2 = self.color2_to_change

    if self.color3_to_change is None:
        c3 = (random.random(), random.random(), random.random())
    else:
        c3 = self.color3_to_change

    plt.figure(figsize=(20, 20))

    plt.fill([a[0], b[0], c[0], d[0]], [a[1], b[1], c[1], d[1]], color=c1, alpha=0.8)
    # plt.hold(True)

    carpet(a, b, c, d, iterations, c2, c3)

    plt.title("Randomly Colored Sierpinski Carpet (iterations = " + str(iterations) + ")")
    plt.axis('equal')
    plt.axis('off')
    plt.show()
    self.clearScreen()
# end def carpet():

def tricircle(self):
    triangle = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2.)]  # [(-2,-2),(0,2),(2,0)]

    # triangle = [(0,0), (1,0), (0,1)]

    radius_limit = 0.005
    fig = plt.figure(figsize=(18, 18))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim((0, 1))  # ((-3,3))
    ax.set_ylim((0, 1))  # ((-3,3))

    if self.color_to_change == None:
        self.color_to_change = 'r'

    draw_triangle_fractal(ax, triangle, radius_limit, 'w', self.color_to_change, 2)

    plt.title(
        "Randomly Colored Sierpinski Triangle With Embedded Circles")
    plt.axis('off')
    plt.show()
    self.clearScreen()
# end def tricircle():

def symcoloredsierpinski(self):
    a = np.array([0, 0])
    b = np.array([1, 0])
    c = np.array([0.5, np.sqrt(3) / 2.])

    k = 5

    plt.figure(figsize=(15, 15))

    iterations = self.itersym.get()

    Sierpinski(a, b, c, k, iterations)

    plt.title(
        "Asymmetrical (cut at 1/5) Randomly Colored Sierpinski Triangle (iterations = " + str(iterations) + ")")
    plt.axis('equal')
    plt.axis('off')
    plt.show()
    self.clearScreen()
# end def symcoloredsierpinski():

def rectSierpinski(self):
    h = np.sqrt(3)

    a1 = np.array([0, 0])
    b1 = np.array([3, 0])
    c1 = np.array([1.5, h])
    a1u = np.array([0, 2 * h])
    b1u = np.array([3, 2 * h])
    c1u = np.array([1.5, h])

    a2 = np.array([0, 0])
    b2 = np.array([0, 2 * h])
    c2 = np.array([1.5, h])
    a2r = np.array([3, 0])
    b2r = np.array([3, 2 * h])
    c2r = np.array([1.5, h])

    k1 = 3
    k1u = 5
    k2 = 4
    k2r = 6

    fig, ax = plt.subplots(1, figsize=(15, 15))

    iter = self.itercube.get()
    Sierpinski(a1, b1, c1, k1, iteration=iter)
    # plt.hold(True)
    Sierpinski(a1u, b1u, c1u, k1u, iteration=iter)
    # plt.hold(True)
    Sierpinski(a2, b2, c2, k2, iteration=iter)
    # plt.hold(True)
    Sierpinski(a2r, b2r, c2r, k2r, iteration=iter)
    # plt.hold(True)

    plt.title("Randomly Colored Cubistic Sierpinski Synthesis (iterations = " + str(iter) + ")")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.axis('equal')
    plt.axis('off')
    plt.show()
    self.clearScreen()
    # end def rectSierpinski():

def manderbrot(self, theme):
    n = 1000
    img = plotter(n, thresh=4, max_steps=50)
    # plt.imshow(img, cmap="inferno")
    plt.imshow(img, self.theme.get())
    plt.axis("off")
    plt.show()
    self.clearScreen()
# end def manderbrot():
