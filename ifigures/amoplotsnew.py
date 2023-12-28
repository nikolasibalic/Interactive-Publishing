from .my_plots import *
from .latex2png import latex2png
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


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


    def addArrow(self, fromStateIndex:int, toStateIndex:int, label:str="", style="<->", color="k", strength:float=1,
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


    def plot(self, axis, labels=False, linewidth=4, length=0.7, stateBlob=500, fontsize=14, arrowLabelSize=12,
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
                plt.pie(sizes, colors=["0.85"], shadow=False, counterclock=counterclock, startangle=0,
                        wedgeprops = {'linewidth': 0,"edgecolor":"0.5"},
                        center=(self.locationX[i], self.locationY[i]),
                        radius=couplingBlob)
                if amplitude>1e-10:
                    plt.pie(sizes, colors=colors, shadow=False, counterclock=counterclock, startangle=0,
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
                
                color = getComplexColor(-1j*self.arrows[i][5].conj(), max(normArrows, 1e-15) * 1.00001)
                color = getComplexColor(-1j*self.arrows[i][5].conj(), abs(self.arrows[i][5]) * 1.00001)
                colors=['white', color]
                phase = np.angle(-1j*self.arrows[i][5].conj())/(2*np.pi)
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

        if not debug:
            axis.set_axis_off()

