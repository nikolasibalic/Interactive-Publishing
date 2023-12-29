from .style import *
from .latex2png import latex2png
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pyvista as pv
from io import BytesIO
from PIL import Image


class EnergyLevels:
    """
    Generates energy level diagram with annotation.
    """

    def __init__(self):
        self.label = []
        self.locationX = []
        self.locationY = []
        self.state = None
        self.arrows = []
        self.state_color = []

    def add(self, label:str, locationX:float, locationY:float, color="k"):
        """
          Adds energy level

          Args:
            label: label of the energy level
            locationX: center position on plot axis
            locationY: center position on plot axis
        """
        self.label.append(label)
        self.locationX.append(locationX)
        self.locationY.append(locationY)
        self.state_color.append(color)

    def setState(self, state):
        """
            Adds current state representation to level diagram.

            State will be represented as blobs of different sizes and
            colors plotted on corresponding energy levels.
            Blobs size correspond to the amplitude of that basis state
            in the total state, while their colour is mapped based
            on the complex colour wheel scheme defined in my_plots.

            Args:
                state : complex number array decomposing state in the
                    basis of the previously added energy levels
        """
        assert len(state) == len(self.label), "state array lenght should be the same as number of states"
        self.state = np.array(state)

    def clearState(self):
        """
            Clears system state from the energy level diagram.
        """
        self.state = None

    def getTotalStates(self):
        """
            Total number of states on the energy level diagram.
        """
        return len(self.locationX)


    def addArrow(self, fromStateIndex:int, toStateIndex:int, label:str="", style="<->", color="k", strength:complex=1,
                 detuning:float = None):
        """
            Adds arrow to the energy level diagram.

            Args:
                fromStateIndex (int): index of the first state
                toStateIndex (int): index of the second state it points to
                style (string): style of arrow, accepted values are
                    '<-', '->' or '<->' . Default is '<->'
                detuning: None by default. Or  (relativeValue, "label") tuple
        """
        assert fromStateIndex < len(self.locationX), "fromStateIndex should be in range 0, getTotalStates - 1"
        assert toStateIndex < len(self.locationX), "toStateIndex should be in range 0, getTotalStates - 1"
        # if arrow exists, replace label; if it doesn't exist add new arrow
        for i in range(len(self.arrows)):
            if self.arrows[i][0] == fromStateIndex and self.arrows[i][1] == toStateIndex:
                self.arrows[i][2] = label
                self.arrows[i][3] = style
                self.arrows[i][4] = color
                self.arrows[i][5] = strength  
                self.arrows[i][6] = detuning
        self.arrows.append([fromStateIndex, toStateIndex, label, style, color,
                            strength, detuning])  # -1j is from evolution equtions


    def plot(self, axis:plt.axis, labels=True, linewidth=4, length=0.7, stateBlob=500, fontsize=14, arrowLabelSize=12,
             debug=False, dpi=100, drivingStrenghtToWidth=True, couplingBlob=0.3):
        """
            Plots energy level digram on the given figure axis.

            Args:
                linewidth (float): energy level line width
                length (float): energy level line length
                stateBlob (flaot): maximum blob size for a system state,
                    corresponding to the unit amplitude for the system to
                    be in a given energy level
                drivingStrenghtToWidth (bool): Should arrows correspond to
                    driving strengths. True by default.
                debug (bool): turns on and of plot axis, useful for precise
                    positioning.
        """
        if self.state is None:
            for i in range(len(self.label)):
                axis.plot([self.locationX[i] - length / 2,
                           self.locationX[i] + length / 2],
                        [self.locationY[i], self.locationY[i]],
                       "-",
                       color="k",
                       lw=linewidth,
                       solid_capstyle='round',
                       zorder=1)

        if labels:
            for i in range(len(self.label)):
                axis.text(self.locationX[i] + 0.55 * length, self.locationY[i],
                          self.label[i],
                          color=self.state_color[i],
                          fontsize = fontsize,
                          verticalalignment='center')

        if self.state is not None:
            for i in range(len(self.state)):
                amplitude = np.abs(self.state[i])
                color = getComplexColor(self.state[i], max(amplitude, 1e-15) * 1.00001)
                
                #color = getComplexColor(self.arrows[i][5], max(normArrows, 1e-15) * 1.00001)
                colors=[color]
                phase = np.angle(self.state[i])
                counterclock = True #phase >= 0
                sizes = [1]
                radius = couplingBlob*amplitude
                axis.pie(sizes, colors=["0.85"], shadow=False, counterclock=counterclock, startangle=0,
                        wedgeprops = {'linewidth': 0,"edgecolor":"0.5"},
                        center=(self.locationX[i], self.locationY[i]),
                        radius=couplingBlob)
                if amplitude>1e-10:
                    axis.pie(sizes, colors=colors, shadow=False, counterclock=counterclock, startangle=0,
                        wedgeprops = {'linewidth': 0,"edgecolor":"0.5"},
                        center=(self.locationX[i], self.locationY[i]),
                        radius=radius)
                axis.scatter([self.locationX[i]+radius*np.cos(phase)],
                             [self.locationY[i]+radius*np.sin(phase)],
                             s=[stateBlob/10],
                             c=[(0,0,0,0.5)],
                             linewidth=0,
                             zorder=2)

        normArrows = -1
        for i in range(len(self.arrows)):
            normArrows = max(abs(self.arrows[i][5]), normArrows)

        for i in range(len(self.arrows)):
            xStart = self.locationX[self.arrows[i][0]]
            yStart = self.locationY[self.arrows[i][0]]
            xEnd = self.locationX[self.arrows[i][1]]
            yEnd = self.locationY[self.arrows[i][1]]
            if self.arrows[i][6] is not None:
                detuning, label = self.arrows[i][6]
            else:
                detuning = 0
            yEnd += detuning
            vector = np.array([xEnd - xStart, yEnd - yStart])
            middle = np.array([xStart,yStart]) + vector/2
            unitVector = vector / np.linalg.norm(vector)
            dv = 0.5 * unitVector
            xStart += dv[0]
            yStart += dv[1]
            xEnd -= dv[0]
            yEnd -= dv[1]
            vector = vector - 2 * dv

            if drivingStrenghtToWidth:
                # map relative strenghts of driving fields to widths of the arrows
                width = 0.05 * abs(self.arrows[i][5]) / normArrows
            else:
                width = 0.05
            
            # for new plotting style overwrite user-specified color with one that
            # depends on the phase of the driving - adds -1j from evolution equations
            self.arrows[i][4] = '0.5'
            #getComplexColor(self.arrows[i][5], max(abs(self.arrows[i][5]), 1e-15) * 1.00001)
                
            if self.arrows[i][3] == "<->":
                axis.arrow(middle[0], middle[1], vector[0]/2, vector[1]/2,
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
                axis.arrow(middle[0], middle[1], -vector[0]/2, -vector[1]/2,
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
            elif self.arrows[i][3] == "->":
                axis.arrow(xStart, yStart, vector[0], vector[1],
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
            else:
                #  self.arrows[i][3] == "<-"
                axis.arrow(xEnd, yEnd, -vector[0], -vector[1],
                           length_includes_head=True,
                          width=width,
                          edgecolor=self.arrows[i][4],
                          facecolor=self.arrows[i][4],
                          capstyle="round")
                plt.annotate('',
                    xytext=(5,0),
                    xy=(9            ,0),
                    arrowprops=dict(arrowstyle="simple", color=self.arrows[i][4]),
                    size=width
                )

            # add annotation if existing
            if self.arrows[i][2] != "":
                generator = latex2png()
                file = generator.make_png(self.arrows[i][2], 
                                          fontsize=arrowLabelSize, dpi=dpi,
                                          border=[5,5,5,5])
                arr_image = plt.imread(file, format='png')

                imagebox = OffsetImage(arr_image)
                # axis.plot([middle[0]],[middle[1]], "bo")
                ab = AnnotationBbox(imagebox, xy=(middle[0], middle[1]), pad=0, frameon=debug)
                axis.add_artist(ab)
            else:
                
                color = getComplexColor(-1j*self.arrows[i][5], max(normArrows, 1e-15) * 1.00001)
                color = getComplexColor(-1j*self.arrows[i][5], abs(self.arrows[i][5]) * 1.00001)
                
                colors=['white', color]
                phase = np.angle(-1j*self.arrows[i][5])/(2*np.pi)
                counterclock = phase >= 0
                sizes= [abs(phase), 1-abs(phase)]
                plt.pie(sizes, colors=colors, shadow=False, counterclock=counterclock, startangle=0,
                    wedgeprops = {'linewidth': 0,"edgecolor":"0.1"},
                    center=(middle[0], middle[1]),
                    radius=1.2*couplingBlob*abs(self.arrows[i][5]) / normArrows)
                
                color = getComplexColor(-1j*np.conj(self.arrows[i][5]), max(normArrows, 1e-15) * 1.00001)
                color = getComplexColor(-1j*np.conj(self.arrows[i][5]), abs(self.arrows[i][5]) * 1.00001)
                colors=['white', color]
                phase = np.angle(-1j*np.conj(self.arrows[i][5]))/(2*np.pi)
                counterclock = phase >= 0
                sizes= [abs(phase), 1-abs(phase)]
                plt.pie(sizes, colors=colors, shadow=False, counterclock=counterclock, startangle=0,
                    wedgeprops = {'linewidth': 0,"edgecolor":"0.1"},
                    center=(middle[0], middle[1]),
                    radius=1.0*couplingBlob*abs(self.arrows[i][5]) / normArrows)

                colors=['white', 'white']
                counterclock = phase >= 0
                sizes= [1, 0]
                plt.pie(sizes, colors=colors, shadow=False, counterclock=counterclock, startangle=0,
                    wedgeprops = {'linewidth': 0,"edgecolor":"0.1"},
                    center=(middle[0], middle[1]),
                    radius=0.8*couplingBlob*abs(self.arrows[i][5]) / normArrows)

                

            # add detuning if existing
            if self.arrows[i][6] is not None:
                detuning, label = self.arrows[i][6]
                fromState = self.arrows[i][1]
                axis.plot([self.locationX[fromState] - length / 2,
                       self.locationX[fromState] + length / 2],
                    [self.locationY[fromState] + detuning,
                     self.locationY[fromState] + detuning],
                   ":",
                   color="k",
                   lw=linewidth,
                   solid_capstyle='round',
                   zorder=-1)

        axis.autoscale()
        if not debug:
            axis.set_axis_off()


class EnergyLevelsOld:
    """
    Generates energy level diagram with annotation.
    """

    def __init__(self):
        self.label = []
        self.locationX = []
        self.locationY = []
        self.state = None
        self.arrows = []

    def add(self, label, locationX, locationY):
        """
          Adds energy level

          Args:
            label: label of the energy level
            locationX: center position on plot axis
            locationY: center position on plot axis
        """
        self.label.append(label)
        self.locationX.append(locationX)
        self.locationY.append(locationY)

    def setState(self, state):
        """
            Adds current state representation to level diagram.

            State will be represented as blobs of different sizes and
            colors plotted on corresponding energy levels.
            Blobs size correspond to the amplitude of that basis state
            in the total state, while their colour is mapped based
            on the complex colour wheel scheme defined in my_plots.

            Args:
                state : complex number array decomposing state in the
                    basis of the previously added energy levels
        """
        assert len(state) == len(self.label), "state array lenght should be the same as number of states"
        self.state = np.array(state)

    def clearState(self):
        """
            Clears system state from the energy level diagram.
        """
        self.state = None

    def getTotalStates(self):
        """
            Total number of states on the energy level diagram.
        """
        return len(self.locationX)


    def addArrow(self, fromStateIndex, toStateIndex, label="", style="<->", color="k", strength=1,
                 detuning = None):
        """
            Adds arrow to the energy level diagram.

            Args:
                fromStateIndex (int): index of the first state
                toStateINdex (int): index of the second state it points to
                style (string): style of arrow, accepted values are
                    '<-', '->' or '<->' . Default is '<->'
                detuning: None by default. Or  (relativeValue, "label") tuple
        """
        assert fromStateIndex < len(self.locationX), "fromStateIndex should be in range 0, getTotalStates - 1"
        assert toStateIndex < len(self.locationX), "toStateIndex should be in range 0, getTotalStates - 1"
        # if arrow exists, replace label; if it doesn't exist add new arrow
        for i in range(len(self.arrows)):
            if self.arrows[i][0] == fromStateIndex and self.arrows[i][1] == toStateIndex:
                self.arrows[i][2] = label
                self.arrows[i][3] = style
                self.arrows[i][4] = color
                self.arrows[i][5] = strength
                self.arrows[i][6] = detuning
        self.arrows.append([fromStateIndex, toStateIndex, label, style, color,
                            strength, detuning])


    def plot(self, axis, labels=False, linewidth=4, length=0.7, stateBlob=500, fontsize=14, arrowLabelSize=12,
             debug=False, dpi=100, drivingStrenghtToWidth=True):
        """
            Plots energy level digram on the given figure axis.

            Args:
                linewidth (float): energy level line width
                length (float): energy level line length
                stateBlob (flaot): maximum blob size for a system state,
                    corresponding to the unit amplitude for the system to
                    be in a given energy level
                drivingStrenghtToWidth (bool): Should arrows correspond to
                    driving strengths. True by default.
                debug (bool): turns on and of plot axis, useful for precise
                    positioning.
        """
        for i in range(len(self.label)):
            axis.plot([self.locationX[i] - length / 2,
                       self.locationX[i] + length / 2],
                    [self.locationY[i], self.locationY[i]],
                   "-",
                   color="k",
                   lw=linewidth,
                   solid_capstyle='round',
                   zorder=1)

        if labels:
            for i in range(len(self.label)):
                axis.text(self.locationX[i] + 0.55 * length, self.locationY[i],
                          self.label[i],
                          fontsize = fontsize,
                          verticalalignment='center')

        if self.state is not None:
            for i in range(len(self.state)):
                amplitude = np.abs(self.state[i])
                color = getComplexColor(self.state[i], max(amplitude, 1e-15) * 1.00001)
                axis.scatter([self.locationX[i]],
                             [self.locationY[i]],
                             s=[amplitude * stateBlob],
                             c=[color],
                             zorder=2)

        normArrows = -1
        for i in range(len(self.arrows)):
            normArrows = max(self.arrows[i][5], normArrows)

        for i in range(len(self.arrows)):
            xStart = self.locationX[self.arrows[i][0]]
            yStart = self.locationY[self.arrows[i][0]]
            xEnd = self.locationX[self.arrows[i][1]]
            yEnd = self.locationY[self.arrows[i][1]]
            if self.arrows[i][6] is not None:
                detuning, label = self.arrows[i][6]
            else:
                detuning = 0
            yEnd += detuning
            vector = np.array([xEnd - xStart, yEnd - yStart])
            middle = np.array([xStart,yStart]) + vector/2
            unitVector = vector / np.linalg.norm(vector)
            dv = 0.5 * unitVector
            xStart += dv[0]
            yStart += dv[1]
            xEnd -= dv[0]
            yEnd -= dv[1]
            vector = vector - 2 * dv

            if drivingStrenghtToWidth:
                # map relative strenghts of driving fields to widths of the arrows
                width = 0.05 * self.arrows[i][5] / normArrows
            else:
                width = 0.05

            if self.arrows[i][3] == "<->":
                axis.arrow(middle[0], middle[1], vector[0]/2, vector[1]/2,
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
                axis.arrow(middle[0], middle[1], -vector[0]/2, -vector[1]/2,
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
            elif self.arrows[i][3] == "->":
                axis.arrow(xStart, yStart, vector[0], vector[1],
                           length_includes_head=True,
                           width=width,
                           edgecolor=self.arrows[i][4],
                           facecolor=self.arrows[i][4],
                           capstyle="round")
            else:
                #  self.arrows[i][3] == "<-"
                axis.arrow(xEnd, yEnd, -vector[0], -vector[1],
                           length_includes_head=True,
                          width=width,
                          edgecolor=self.arrows[i][4],
                          facecolor=self.arrows[i][4],
                          capstyle="round")
                plt.annotate('',
                    xytext=(5,0),
                    xy=(9            ,0),
                    arrowprops=dict(arrowstyle="simple", color=self.arrows[i][4]),
                    size=width
                )

            # add annotation if existing
            if self.arrows[i][2] != "":
                generator = latex2png()
                file = generator.make_png(self.arrows[i][2], 
                                          fontsize=arrowLabelSize, dpi=dpi,
                                          border=[5,5,5,5])
                arr_image = plt.imread(file, format='png')

                imagebox = OffsetImage(arr_image)
                # axis.plot([middle[0]],[middle[1]], "bo")
                ab = AnnotationBbox(imagebox, xy=(middle[0], middle[1]), pad=0, frameon=debug, fontsize=fontsize)
                axis.add_artist(ab)

            # add detuning if existing
            if self.arrows[i][6] is not None:
                detuning, label = self.arrows[i][6]
                fromState = self.arrows[i][1]
                axis.plot([self.locationX[fromState] - length / 2,
                       self.locationX[fromState] + length / 2],
                    [self.locationY[fromState] + detuning,
                     self.locationY[fromState] + detuning],
                   ":",
                   color="k",
                   lw=linewidth,
                   solid_capstyle='round',
                   zorder=-1)

        if not debug:
            axis.set_axis_off()

def blobAnnotate(axis: plt.axis,
                 blobX:float, blobY:float,
                 textX, textY,
                 text,
                 blobSize=100, linewidth=3, fontsize=12,
                 color=cDUbb, curvatureSign="+", zorder=-1):
    """
        Cartoon style blob annotation to highlight different parts of plot.

        Args:
            axis : figure axis where we do blob annotation
            blobX (float) : X position of blob highlight on axis
            blobY (float) : Y position of blob highlight on axis
            textX (float) : X position of corresponding annotation
            textY (float) : Y position of corresponding annotation
            text (string) : annotation
    """
    axis.scatter([blobX],[blobY], s=blobSize, c=color)
    axis.annotate(text, (blobX, blobY),(textX, textY),
                ha="center", va="center",
                size=fontsize,
                arrowprops=dict(arrowstyle="-",
                                fc=color, ec=color, lw=linewidth, zorder=zorder,
                                connectionstyle=("arc3,rad=%s0.05" % curvatureSign),
                                ),
                  zorder=zorder,
                  bbox=dict(boxstyle="round,pad=0.3", fc=color, ec=color, lw=2)
                  )


def xAnnotate(axis, fromX, toX, color=cDUy, zorder=-2):
    """_summary_

    Args:
        axis (_type_): _description_
        fromX (_type_): _description_
        toX (_type_): _description_
        color (_type_, optional): _description_. Defaults to cDUy.
        zorder (int, optional): _description_. Defaults to -2.
    """
    axis.axvspan(fromX, toX, color=color, zorder=zorder)


def yAnnotate(axis, fromY, toY, color=cDUy, zorder=-2):
    """_summary_

    Args:
        axis (_type_): _description_
        fromY (_type_): _description_
        toY (_type_): _description_
        color (_type_, optional): _description_. Defaults to cDUy.
        zorder (int, optional): _description_. Defaults to -2.
    """
    axis.axhspan(fromY, toY, color=color, zorder=zorder)


def equation(latex, axis,fontsize=10, dpi=100, border=[4,4,4,4], debug=False,
             x=0.1, y=1):
    """Adds equations on the given axis plot (and turns off axis).

    Args:
        latex (_type_): _description_
        axis (_type_): _description_
        fontsize (int, optional): _description_. Defaults to 10.
        dpi (int, optional): _description_. Defaults to 100.
        border (list, optional): _description_. Defaults to [4,4,4,4].
        debug (bool, optional): _description_. Defaults to False.
        x (float, optional): _description_. Defaults to 0.1.
        y (int, optional): _description_. Defaults to 1.
    """
    generator = latex2png()
    file = generator.make_png(latex, fontsize=fontsize, dpi=dpi, border=border)
    arr_image = plt.imread(file, format='png')

    imagebox = OffsetImage(arr_image)
    ab = AnnotationBbox(imagebox, xy=(x, y), pad=0, frameon=debug)

    axis.add_artist(ab)
    if not debug:
        axis.set_axis_off()

class BlochSphere:

    def __init__(self, r=3, resolution=3):
        """Utilities for plotting Bloch Sphere

        Args:
            r (int, optional): _description_. Defaults to 3.
            resolution (int, optional): _description_. Defaults to 3.
        """

        self.p = pv.Plotter(shape=(1, 1),
                     #  multi_samples=1,
                       window_size=(resolution * 600, resolution * 600),
                       off_screen=True,
                           notebook=False)
        self.p.set_background(cDUsky, top="white")
        
        self.resolution = resolution

        # draw cross section of sphere with three principal coordinate planes
        num = 50
        theta = np.linspace(-1 * np.pi, 1 * np.pi, num)
        self.r = r
        phi = 0 * np.pi / 60

        z = 0 * self.r * np.cos(theta)
        x = self.r * np.cos(theta)
        y = self.r * np.sin(theta)
        rpts = np.column_stack((x, y, z))
        spline = pv.Spline(rpts, 1000)
        rxy_tube = spline.tube(radius=0.05)

        z = self.r * np.cos(theta)
        x = self.r * np.sin(theta) * np.cos(phi - np.pi / 2)
        y = self.r * np.sin(theta) * np.sin(phi - np.pi / 2)
        rpts = np.column_stack((x, y, z))
        spline = pv.Spline(rpts, 1000)
        rxz_tube = spline.tube(radius=0.05)

        z = self.r * np.cos(theta)
        x = self.r * np.sin(theta) * np.cos(phi)
        y = self.r * np.sin(theta) * np.sin(phi)
        rpts = np.column_stack((x, y, z))
        spline = pv.Spline(rpts, 1000)
        ryz_tube = spline.tube(radius=0.05)

        # add sphere
        big = pv.Sphere(center=(0, 0, 0), radius=self.r)
        self.p.add_mesh(big, opacity=0.4,
                        color="w", specular=0.85, smooth_shading=True)

        # add cross-sections
        self.p.add_mesh(rxy_tube, opacity=0.1, smooth_shading=True, color=cDUkk)
        self.p.add_mesh(rxz_tube, opacity=0.1, smooth_shading=True, color=cDUkk)
        self.p.add_mesh(ryz_tube, opacity=0.1, smooth_shading=True, color=cDUkk)

    def state2XYZ(complexVectorState):
        # TO-Do
        #x =
        #y =
        #z =
        #return x,y,z
        pass

    def addStateBlob(self, x,y,z, color=cDUrr, radius=0.2):
        """Adds highlighted Blob on or inside the Bloch sphere.

        Args:
            x (_type_): _description_
            y (_type_): _description_
            z (_type_): _description_
            color (_type_, optional): _description_. Defaults to cDUrr.
            radius (float, optional): _description_. Defaults to 0.2.
        """
        small = pv.Sphere(center=np.array([x, y, z])*self.r,
                          radius=self.r / 3 * radius)
        self.p.add_mesh(small, opacity=1.0, color=color, smooth_shading=True)
        pass

    def addStateArrow(self, x,y,z, color=cDUbbbb):
        """Adds state arrow to the Bloch sphere, given the tip position.

        Args:
            x (_type_): _description_
            y (_type_): _description_
            z (_type_): _description_
            color (_type_, optional): _description_. Defaults to cDUbbbb.
        """
        length = np.sqrt(x*x + y*y + z*z)
        arrow=pv.Arrow(start=(0.0, 0.0, 0.0), direction=np.array([x,y,z]) * self.r,
                       tip_length=0.25, tip_radius=0.1, tip_resolution=20,
                       shaft_radius=0.05, shaft_resolution=20, scale=length * self.r)
        self.p.add_mesh(arrow, opacity=1.0, color=color, smooth_shading=True)

    def addTrajectory(self, trajectoryXYZ):
        """Adds trajectory in t, with t shown with viridis colouring.

        Args:
            trajectoryXYZ (_type_): _description_
        """
        spline = pv.Spline(trajectoryXYZ * self.r, 1000)
        spline["scalars"] = np.arange(spline.n_points)
        tubes=spline.tube(radius=0.1)
        self.p.add_mesh(tubes, smooth_shading=True, show_scalar_bar=False)

    def plot(self, axis=None, debug=False,
             cameraPosition=[(12.2, 4.0, 4.0),
                            (0.0, 0.0, 0.0),
                            (0.0, 0.0, 1)],
             labelAxis=True,
             labelSize=12,
             dpi=100,
             label=[r"$|e\rangle$",
                         r"$|g\rangle$",
                         r"$\frac{|e\rangle+|g\rangle}{\sqrt{2}}$",
                         r"$\frac{|e\rangle+i|g\rangle}{\sqrt{2}}$"
                        ],
              labelOffset=None
            ):
        """Plots Bloch sphere on the given axis.

        Args:
            axis (_type_, optional): _description_. Defaults to None.
            debug (bool, optional): _description_. Defaults to False.
            cameraPosition (list, optional): _description_. Defaults to [(12.2, 4.0, 4.0), (0.0, 0.0, 0.0), (0.0, 0.0, 1)].
            labelAxis (bool, optional): _description_. Defaults to True.
            labelSize (int, optional): _description_. Defaults to 12.
            dpi (int, optional): _description_. Defaults to 100.
            label (list, optional): _description_. Defaults to [r"$|e\rangle$", r"$|g\rangle$", r"$\frac{|e\rangle+|g\rangle}{\sqrt{2}}$", r"$\frac{|e\rangle+i|g\rangle}{\sqrt{2}}$" ].
            labelOffset (_type_, optional): _description_. Defaults to None.
        """
        self.p.enable_depth_peeling(10)
        self.p.camera_position = cameraPosition
        # [(13.0, 0.0, 1.0),
        #  (0.0, 0.0, 0.0),
        #  (0.1, 0.0, 0.1)]

        if axis==None:
            if labelAxis:
                print("Note: Bloch sphere axis are labeled only if axis"
                     " argument is passed to plot function")
            self.p.show()
        else:
            png_output = BytesIO()
            self.p.show(screenshot=png_output)

            if labelAxis:
                generator = latex2png()
                im = Image.fromarray(self.p.image)
                im = im.convert("RGBA")
                if labelOffset == None:
                    labelOffset = [(int(im.size[0]*0.53), 10),
                        (int(im.size[0]*0.53), int(im.size[1]*0.87)),
                        (int(im.size[0]*0.35), int(im.size[1]*0.6)),
                        (int(im.size[0]*0.86), int(im.size[1]*0.54))]

                for i in range(len(labelOffset)):
                    labelLatex = generator.make_png(label[i],
                                               fontsize=labelSize,
                                                dpi=dpi * self.resolution*2)
                    #white_to_transparency(Image.open(labelLatex))
                    l = Image.open(labelLatex)
                    im.paste(l, labelOffset[i], l.convert('RGBA'))

                axis.imshow(im)
            else:
                axis.imshow(self.p.image)

            if not debug:
                axis.set_axis_off()

class DensityMatrix:

    def __init__(self, with_grid=True):
        """Color mapping of Density Matrix

        Args:
            with_grid (bool, optional): _description_. Defaults to True.
        """
        self.with_grid = with_grid
        

    def plot (self, axis:plt.axis, rho, visualise="with dots"):
        """_summary_

        Args:
            axis (plt.axis): _description_
            rho (_type_): _description_
            visualise (str, optional): _description_. Defaults to "with dots".
        """
        
        mdim = len(rho) # matrix dimension
        
        R=np.zeros((mdim, mdim))
        G=np.zeros((mdim, mdim))
        B=np.zeros((mdim, mdim))
            
        dots = {"x":[],
                "y":[]}
        referenceDots = {"x":[],
                "y":[]}
    
        for col in range(0,mdim):
            for row in range(0,mdim):
                R[row,col]=getComplexColor(rho[row][col], 1.)[0]
                G[row,col]=getComplexColor(rho[row][col], 1.)[1]
                B[row,col]=getComplexColor(rho[row][col], 1.)[2]
                dots["x"].append(row + rho[row][col].real * 0.44)
                dots["y"].append(col + rho[row][col].imag * 0.44)
                referenceDots["x"].append(col)
                referenceDots["y"].append(row)

        RGB=np.dstack((R, G, B))
        axis.imshow(RGB)
                
        if (visualise == "with dots"):
            axis.plot(dots["x"],dots["y"], "o", markeredgecolor=cDUk, markerfacecolor = cDUk, markersize =3, zorder=3)

        if self.with_grid:
            # add grid
            for coord in np.arange(0,mdim+1,1):
                axis.axhline(coord-0.5, color=cDUggg, zorder=2,linewidth=3)
                axis.axvline(coord-0.5, color=cDUggg, zorder=2,linewidth=3)
            
        axis.set_xlim(-0.52, mdim-0.48)
        axis.set_ylim(mdim-0.48,-0.52)
        axis.set_axis_off() 
       