# BSSD Midterm Project
# Scott Bing
# Image Analysis

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Fractals import *
from MandelRayBulb import *

TOGGLE_SLICE = False
TOLERENCE = False
RED = 183
GREEN = 198
BLUE = 144


class Application(Frame):
    """ GUI application that displays the image processing
        selections"""

    def __init__(self, master):
        """ Initialize Frame - application constructor"""
        super(Application, self).__init__(master)

        Frame.__init__(self, master)
        self.master = master

        # used when calling slideshow
        # pygame.init()

        # read mandelbrot colour schemes file
        # Read values from file
        self.schemes = []
        with open('schemes/schemes.txt') as inFile:
            self.schemes = [line.strip() for line in inFile]
            #self.schemes = [line for line in inFile]

        # reverse_btn = Button(self)
        self.color_to_change = None
        self.color1_to_change = None
        self.color2_to_change = None
        self.color3_to_change = None

        # Menu taken from:     https://www.tutorialspoint.com/python/tk_menu.htm
        # create menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label="New", command=self.donothing)
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.donothing)
        fileMenu.add_command(label="Save as...", command=self.donothing)
        fileMenu.add_command(label="Close", command=self.donothing)

        fileMenu.add_separator()

        fileMenu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=fileMenu)
        editMenu = Menu(menu, tearoff=0)
        editMenu.add_command(label="Undo", command=self.donothing)

        editMenu.add_separator()

        editMenu.add_command(label="Cut", command=self.donothing)
        editMenu.add_command(label="Copy", command=self.donothing)
        editMenu.add_command(label="Paste", command=self.donothing)
        editMenu.add_command(label="Delete", command=self.donothing)
        editMenu.add_command(label="Select All", command=self.donothing)

        menu.add_cascade(label="Edit", menu=editMenu)
        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="Help Index", command=self.donothing)
        helpMenu.add_command(label="About...", command=self.donothing)
        menu.add_cascade(label="Help", menu=helpMenu)

        self.selected_pixels = []  # list of tuples [()]

        self.grid()
        # open the application frame
        self.create_widgets()
        # self.create_initial_screen()

    # end application constructor

    def chomp(self, x):
        """Remove '\n' newline from string"""
        if x.endswith("\r\n"): return x[:-2]
        if x.endswith("\n") or x.endswith("\r"): return x[:-1]
        return x

    def openFile(self):
        """Process the Open File Menu"""
        self.fileName = askopenfilename(parent=self, initialdir="C:/", title='Choose an image.')
        print(self.fileName)

        self.putImage(self.fileName)

        # open the application frame
        self.create_widgets()

    # end def openFile(self):

    def donothing(self):
        """Placeholder for inactive menu items"""
        pass

    # end def donothing(self):

    def clearScreen(self):
        """Clears the screen"""
        # clear checkboxes
        self.is_mandlebrot.set(False)
        self.is_julia.set(False)
        self.is_cubistic.set(False)
        self.is_symcolored.set(False)
        self.is_tricircle.set(False)
        self.is_carpet.set(False)

        # clear text boxes
        self.height_ent.delete(0,END)
        self.width_ent.delete(0,END)

        # clear the colors
        # reverse_btn = Button(self)
        self.color_to_change = None
        self.color1_to_change = None
        self.color2_to_change = None
        self.color3_to_change = None

        # reset drop down box
        self.theme.set('Accent_r')

        # reset spin boxes
        self.iterspeed_sier.set(50)
        self.iterspeed_drgn.set(50)
        self.iterspeed_hlb.set(50)
        self.itercube.set(7)
        self.itersym.set(5)
        self.itercarp.set(5)
        self.itersier.set(5)
        self.iterdrgn.set(5)
        self.iterhlb.set(5)
        self.iterfrq.set(5)
        self.fill_sier.set(0)
        self.fill_dragon.set(0)
        self.fill_hilbert.set(0)

        # reset radio buttons
        self.fill_sier.set(0)
    # end def clearScreen(self):


    def create_widgets(self):
        """ Create and place screen widgets in the
        main application frame"""
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=20)

        Label(self,
              text="AMAZING FRACTALS",
              wraplength=300,
              font=self.lblFont
              ).grid(row=0, column=0, columnspan=2, sticky=NSEW, pady=7)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=1, column=0, columnspan=2, sticky=EW, pady=5, padx=5)

        animFont = font.Font(weight="bold")
        animFont = font.Font(size=21)

        Label(self,
              text="Static Fractals:",
              font=animFont
              ).grid(row=2, column=0, columnspan=2, sticky=W)

        # process mandlebrot set
        self.is_mandlebrot = BooleanVar()
        Checkbutton(self,
                    text="Mandelbrot Set",
                    variable=self.is_mandlebrot
                    ).grid(row=3, column=0, sticky=W)

        Label(self,
              text="Theme:"
              ).grid(row=3, column=1, sticky=W)

        self.theme = StringVar()
        self.themes = ttk.Combobox(self,
                                   width=10,
                                   textvariable=self.theme)

        # Adding combobox drop down list
        self.themes['values'] = tuple(self.schemes)
        self.themes.grid(row=3, column=1, padx=57, sticky=W)

        # Shows ocean as a default value
        self.themes.current(0)

        # process julia set
        self.is_julia = BooleanVar()
        Checkbutton(self,
                    text="Julia",
                    variable=self.is_julia
                    ).grid(row=4, column=0, sticky=W)

        # process Cubistic Sierpinski Synthesis
        self.is_cubistic = BooleanVar()
        Checkbutton(self,
                    text="Cubistic Sierpinski",
                    variable=self.is_cubistic
                    ).grid(row=5, column=0, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=5, column=1, padx=157, sticky=W)

        self.itercube = IntVar()
        self.itercube.set(7)
        self.iter = Spinbox(self,
                            from_=1,
                            to=7,
                            width=3,
                            textvariable=self.itercube
                            # variable=self.iterations
                            ).grid(row=5, column=1, padx=230, sticky=W)

        # Process Randomly Colored Sierpinski Triangle
        self.is_symcolored = BooleanVar()
        Checkbutton(self,
                    text="Sierpinski Triangle",
                    variable=self.is_symcolored
                    ).grid(row=6, column=0, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=6, column=1, padx=157, sticky=W)

        self.itersym = IntVar()
        self.itersym.set(5)
        self.iter = Spinbox(self,
                            from_=1,
                            to=7,
                            width=3,
                            textvariable=self.itersym
                            # variable=self.iterations
                            ).grid(row=6, column=1, padx=230, sticky=W)

        # process tricircle
        self.is_tricircle = BooleanVar()
        Checkbutton(self,
                    text="Tricircle",
                    variable=self.is_tricircle
                    ).grid(row=7, column=0, sticky=W)

        # process animated sierpinski color
        self.color_sierpinski_btn = Button(self,
                                           text="Select Circle Color",
                                           command=self.colorize,
                                           highlightbackground='#2E4149',
                                           ).grid(row=7, column=1, sticky=W)

        # Process carpet
        self.is_carpet = BooleanVar()
        Checkbutton(self,
                    text="Carpet",
                    variable=self.is_carpet
                    ).grid(row=8, column=0, sticky=W)

        # create a colorized image button
        self.color_carpet_btn = Button(self,
                                       text="Select Colors",
                                       command=self.three_colors,
                                       highlightbackground='#2E4149',
                                       ).grid(row=8, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=8, column=1, padx=157, sticky=W)

        self.itercarp = IntVar()
        self.itercarp.set(5)
        self.iter_sp_carp = Spinbox(self,
                                    from_=1,
                                    to=7,
                                    width=3,
                                    textvariable=self.itercarp
                                    ).grid(row=8, column=1, padx=230, sticky=W)

        btnFont = font.Font(weight="bold")
        btnFont = font.Font(size=19)

        # create a the generate button
        self.generate_btn = Button(self,
                                   text="Generate",
                                   command=self.processSelections,
                                   highlightbackground='#3E4149',
                                   font=btnFont
                                   ).grid(row=9, column=0, sticky=W, pady=10, padx=5)

        # create a the clear screen button
        self.clear_btn = Button(self,
                                text="Clear",
                                command=self.clearScreen,
                                highlightbackground='#2E4149',
                                font=btnFont
                                ).grid(row=9, column=1, sticky=W, pady=10, padx=5)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=10, column=0, columnspan=2, sticky=NSEW, pady=5, padx=5)

        animFont = font.Font(weight="bold")
        animFont = font.Font(size=21)

        Label(self,
              text="Animated Fractals:",
              font=animFont
              ).grid(row=11, column=0, columnspan=2, sticky=W)

        # create a the animate sierpinski button
        self.sierpinski_btn = Button(self,
                                     text="Sierpinski",
                                     command=self.goto_sierpinski,
                                     highlightbackground='#3E4149',
                                     ).grid(row=12, column=0, sticky=W, padx=20, pady=5)

        # process animated sierpinski color
        self.color_sierpinski_btn = Button(self,
                                           text="Select Color",
                                           command=self.colorize,
                                           highlightbackground='#2E4149',
                                           ).grid(row=12, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=12, column=1, padx=157, sticky=W)

        self.itersier = IntVar()
        self.itersier.set(5)
        self.iter_sp_sier = Spinbox(self,
                                    from_=1,
                                    to=8,
                                    width=3,
                                    textvariable=self.itersier
                                    ).grid(row=12, column=1, padx=230, sticky=W)

        Label(self,
              text="Speed:",
              ).grid(row=12, column=1, padx=300, sticky=W)

        self.iterspeed_sier = IntVar()
        self.iterspeed_sier.set(50)
        self.iter_sp_speed_sier = Spinbox(self,
                                     from_=0,
                                     to=500,
                                     width=3,
                                     textvariable=self.iterspeed_sier
                                     ).grid(row=12, column=1, padx=365, sticky=W)

        self.fill_sier = IntVar()
        self.is_open = Radiobutton(self,
                                   text='Open',
                                   variable=self.fill_sier, value=0
                                   ).grid(row=12, column=1, padx=430, sticky=W)

        self.is_filled = Radiobutton(self,
                                         text='Filled',
                                         variable=self.fill_sier, value=1
                                         ).grid(row=12, column=1, padx=490, sticky=W)

        self.fill_sier.set(0)

        # create a the animate dragon button
        self.dragon_btn = Button(self,
                                 text="Dragon",
                                 command=self.goto_dragon,
                                 highlightbackground='#3E4149',
                                 ).grid(row=13, column=0, sticky=W, padx=20, pady=5)

        # process animated dragon color
        self.color_dragon_btn = Button(self,
                                       text="Select Color",
                                       command=self.colorize,
                                       highlightbackground='#2E4149',
                                       ).grid(row=13, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=13, column=1, padx=157, sticky=W)

        self.iterdrgn = IntVar()
        self.iterdrgn.set(5)
        self.iter_sp_drgn = Spinbox(self,
                                    from_=1,
                                    to=10,
                                    width=3,
                                    textvariable=self.iterdrgn
                                    ).grid(row=13, column=1, padx=230, sticky=W)

        Label(self,
              text="Speed:",
              ).grid(row=13, column=1, padx=300, sticky=W)

        self.iterspeed_drgn = IntVar()
        self.iterspeed_drgn.set(50)
        self.iter_sp_speed_drgn = Spinbox(self,
                                     from_=0,
                                     to=500,
                                     width=3,
                                     textvariable=self.iterspeed_drgn
                                     ).grid(row=13, column=1, padx=365, sticky=W)

        self.fill_dragon = IntVar()
        self.is_open = Radiobutton(self,
                                   text='Open',
                                   variable=self.fill_dragon, value=0
                                   ).grid(row=13, column=1, padx=430, sticky=W)

        self.is_filled = Radiobutton(self,
                                     text='Filled',
                                     variable=self.fill_dragon, value=1
                                     ).grid(row=13, column=1, padx=490, sticky=W)

        self.fill_dragon.set(0)

        # create a the animate hilbert button
        self.hilbert_btn = Button(self,
                                  text="Hilbert Curve",
                                  command=self.goto_hilbert,
                                  highlightbackground='#3E4149',
                                  ).grid(row=14, column=0, sticky=W, padx=20, pady=5)

        # process animated hilbert color
        self.color_hilbert_btn = Button(self,
                                        text="Select Color",
                                        command=self.colorize,
                                        highlightbackground='#2E4149',
                                        ).grid(row=14, column=1, sticky=W)

        Label(self,
              text="Iterations:",
              ).grid(row=14, column=1, padx=157, sticky=W)

        self.iterhlb = IntVar()
        self.iterhlb.set(5)
        self.iter_sp_hlb = Spinbox(self,
                                   from_=1,
                                   to=6,
                                   width=3,
                                   textvariable=self.iterhlb
                                   ).grid(row=14, column=1, padx=230, sticky=W)

        Label(self,
              text="Speed:",
              ).grid(row=14, column=1, padx=300, sticky=W)

        self.iterspeed_hlb = IntVar()
        self.iterspeed_hlb.set(50)
        self.iter_sp_speed_hlb = Spinbox(self,
                                     from_=0,
                                     to=500,
                                     width=3,
                                     textvariable=self.iterspeed_hlb
                                     ).grid(row=14, column=1, padx=365, sticky=W)

        self.fill_hilbert = IntVar()
        self.is_open = Radiobutton(self,
                                   text='Open',
                                   variable=self.fill_hilbert, value=0
                                   ).grid(row=14, column=1, padx=430, sticky=W)

        self.is_filled = Radiobutton(self,
                                     text='Filled',
                                     variable=self.fill_hilbert, value=1
                                     ).grid(row=14, column=1, padx=490, sticky=W)

        self.fill_hilbert.set(0)


        # create a the animate slideshow button
        self.slideshow_btn = Button(self,
                                    text="Fractal Slide Show",
                                    command=self.goto_slideshow,
                                    highlightbackground='#3E4149',
                                    ).grid(row=15, column=0, sticky=W, padx=20, pady=5)

        Label(self,
              text="Height:"
              ).grid(row=15, column=1, sticky=W)
        self.height_ent = Entry(self, width=10)
        self.height_ent.grid(row=15, column=1, padx=55, sticky=W)
        Label(self,
              text="Width:"
              ).grid(row=15, column=1, padx=157, sticky=W)
        self.width_ent = Entry(self, width=10)
        self.width_ent.grid(row=15, column=1, padx=210, sticky=W)

        Label(self,
              text="Frequency:"
              ).grid(row=16, column=1, sticky=W)

        self.iterfrq = IntVar()
        self.iterfrq.set(5)
        self.iter_sp_frq = Spinbox(self,
                                   from_=1,
                                   to=20,
                                   width=3,
                                   textvariable=self.iterfrq
                                   ).grid(row=16, column=1, padx=75, sticky=W)

        Label(self,
              text="seconds"
              ).grid(row=16, column=1, padx=100, sticky=W)

        # create a the animate slideshow button
        self.harmon_btn = Button(self,
                                 text="Harmonograph",
                                 command=anim_harmon,
                                 highlightbackground='#3E4149',
                                 ).grid(row=17, column=0, sticky=W, padx=20, pady=5)

        # create a the animate slideshow button
        self.color_harmon_btn = Button(self,
                                 text="Colorful Harmonograph",
                                 command=anim_color_harmon,
                                 highlightbackground='#3E4149',
                                 ).grid(row=18, column=0, sticky=W, padx=20, pady=5)

        # create a the animate slideshow button
        self.random_btn = Button(self,
                                       text="Random Walk",
                                       command=anim_random,
                                       highlightbackground='#3E4149',
                                       ).grid(row=19, column=0, sticky=W, padx=20, pady=5)

        ttk.Separator(self,
                      orient=HORIZONTAL
                      ).grid(row=20, column=0, columnspan=2, sticky=NSEW, pady=5, padx=5)

        animFont = font.Font(weight="bold")
        animFont = font.Font(size=21)

        Label(self,
              text="3D Fractals:",
              font=animFont
              ).grid(row=21, column=0, columnspan=2, sticky=W)

        # create a the animate mandel ray bulb button
        self.mandelraybulb_btn = Button(self,
                                     text="Mandel Ray Bulb",
                                     command=self.goto_mandelraybulb,
                                     highlightbackground='#3E4149',
                                     ).grid(row=22, column=0, sticky=W, padx=20, pady=5)

        # create a the animate surface triangualtion button
        self.surfacetriangulation_btn = Button(self,
                                        text="Surface Triangualtion",
                                        command=anim_surfacetriangulation,
                                        highlightbackground='#3E4149',
                                        ).grid(row=23, column=0, sticky=W, padx=20, pady=5)

        # create a filler
        Label(self,
              text=" "
              ).grid(row=24, column=0, sticky=W)

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.err2show = StringVar()
        Label(self,
              textvariable=self.err2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=25, column=0, sticky=NSEW, pady=4)

    # end def create_widgets(self):

    # Check for numeric and -1-255
    # Taken from:
    # https://stackoverflow.com/questions/31684082/validate-if-input-string-is-a-number-between-0-255-using-regex
    # numeric validation
    def is_number(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    # end def is_number(n):

    def three_colors(self):
        '''process color selections'''
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        self.colorFrame = Toplevel(self)
        self.colorFrame.wm_title("Colorize Settings")

        Label(self.colorFrame,
              text="Select three colors using the RGB sliders and press Generate.",
              wraplength=200,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=W, columnspan=3, padx=10, pady=10)

        Label(self.colorFrame,
              text="Color #1",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=0, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value1,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
        self.red_value1.set(0)

        self.green_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value1,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
        self.green_value1.set(0)

        self.blue_value1 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value1,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
        self.blue_value1.set(0)

        Label(self.colorFrame,
              text="Color #2",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=1, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value2,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)
        self.red_value2.set(0)

        self.green_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value2,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=1, sticky=NSEW, padx=10, pady=10)
        self.green_value2.set(0)

        self.blue_value2 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value2,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=1, sticky=NSEW, padx=10, pady=10)
        self.blue_value2.set(0)

        Label(self.colorFrame,
              text="Color #3",
              wraplength=200,
              font=self.lblFont
              ).grid(row=1, column=2, sticky=W, columnspan=3, padx=10, pady=10)

        self.red_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value3,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=2, sticky=NSEW, padx=10, pady=10)
        self.red_value3.set(0)

        self.green_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value3,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=2, sticky=NSEW, padx=10, pady=10)
        self.green_value3.set(0)

        self.blue_value3 = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value3,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=2, sticky=NSEW, padx=10, pady=10)
        self.blue_value3.set(0)

        # create a the generate button
        self.gen_colorize_btn = Button(self.colorFrame,
                                       text="Generate",
                                       command=self.processThreeColors,
                                       highlightbackground='#3E4149',
                                       font=self.lblFont
                                       ).grid(row=5, column=0, sticky=E, pady=10, padx=5)

        self.cerr2show = StringVar()
        Label(self.colorFrame,
              textvariable=self.cerr2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=6, column=0, sticky=NSEW, pady=4)

    # end def three_colors(self):

    def processThreeColors(self):
        """ Gets three color values """
        # get color #1
        red1 = (int(self.red_value1.get()))
        green1 = (int(self.green_value1.get()))
        blue1 = (int(self.blue_value1.get()))

        # convert RGB color to hexadecimal value
        self.color1_to_change = '#{:02x}{:02x}{:02x}'.format(red1, green1, blue1)

        # get color #2
        red2 = (int(self.red_value2.get()))
        green2 = (int(self.green_value2.get()))
        blue2 = (int(self.blue_value2.get()))

        # convert RGB color to hexadecimal value
        self.color2_to_change = '#{:02x}{:02x}{:02x}'.format(red2, green2, blue2)

        # get color #3
        red3 = (int(self.red_value3.get()))
        green3 = (int(self.green_value3.get()))
        blue3 = (int(self.blue_value3.get()))

        # convert RGB color to hexadecimal value
        self.color3_to_change = '#{:02x}{:02x}{:02x}'.format(red3, green3, blue3)

        self.colorFrame.destroy()

    # end def processThreeColors(self):

    def colorize(self):
        '''process color selections'''
        self.lblFont = font.Font(weight="bold")
        self.lblFont = font.Font(size=16)

        self.colorFrame = Toplevel(self)
        self.colorFrame.wm_title("Colorize Settings")

        Label(self.colorFrame,
              text="Select a color using the RGB sliders and press Generate.",
              wraplength=200,
              font=self.lblFont
              ).grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.red_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.red_value,
              from_=0, to=255,
              resolution=1,
              label="Red",
              orient=HORIZONTAL
              ).grid(row=2, column=0, sticky=NSEW, padx=10, pady=10)
        self.red_value.set(0)

        self.green_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.green_value,
              from_=0, to=255,
              resolution=1,
              label="Green",
              orient=HORIZONTAL
              ).grid(row=3, column=0, sticky=NSEW, padx=10, pady=10)
        self.green_value.set(0)

        self.blue_value = DoubleVar()
        Scale(self.colorFrame,
              variable=self.blue_value,
              from_=0, to=255,
              resolution=1,
              label="Blue",
              orient=HORIZONTAL
              ).grid(row=4, column=0, sticky=NSEW, padx=10, pady=10)
        self.blue_value.set(0)

        # create a the generate button
        self.gen_colorize_btn = Button(self.colorFrame,
                                       text="Generate",
                                       command=self.processColorize,
                                       highlightbackground='#3E4149',
                                       font=self.lblFont
                                       ).grid(row=5, column=0, sticky=E, pady=10, padx=5)

        self.errFont = font.Font(weight="bold")
        self.errFont = font.Font(size=20)
        self.cerr2show = StringVar()
        Label(self.colorFrame,
              textvariable=self.cerr2show,
              foreground="red",
              font=self.errFont,
              wraplength=200
              ).grid(row=6, column=0, sticky=NSEW, pady=4)

    # end def colorize(self):

    def processColorize(self):
        """ Adds a user selected color to the image """
        # get select color
        red = (int(self.red_value.get()))
        green = (int(self.green_value.get()))
        blue = (int(self.blue_value.get()))

        # convert RGB color to hexadecimal value
        self.color_to_change = '#{:02x}{:02x}{:02x}'.format(red, green, blue)

        self.colorFrame.destroy()

    # end def processColorize(self):

    def goto_slideshow(self):
        anim_slideshow(self)
        self.clearScreen()
    #end goto_slideshow(self):

    def goto_sierpinski(self):
        anim_sierpinski(self)
        self.clearScreen()
    #end goto_sierpinski(self):

    def goto_dragon(self):
        anim_dragon(self)
    #end goto_dragon(self):

    def goto_hilbert(self):
        anim_hilbert(self)
    #end goto_hilbert(self):

    def goto_mandelraybulb(self):
        mandelraybulb()
    #end goto_hilbert(self):

    # process user selections
    def processSelections(self):
        """Processes user screen selections"""
        # Mandelbrot Set
        if self.is_mandlebrot.get() == True:
            theme = self.theme.get()
            manderbrot(self,theme)
        elif self.is_julia.get() == True:
            julia()
            self.clearScreen()
        elif self.is_cubistic.get() == True:
            rectSierpinski(self)
        elif self.is_symcolored.get() == True:
            symcoloredsierpinski(self)
        elif self.is_tricircle.get() == True:
            tricircle(self)
        elif self.is_carpet.get() == True:
            make_carpet(self)
    # end def processSelections(self):


# main
"""Application Entry Point - the main
driver code for the BSSD5410 Midterm Project"""
root = Tk()
root.resizable(height=None, width=None)
root.title("BSSD 5410 Midterm Scott Bing")
app = Application(root)
root.mainloop()
