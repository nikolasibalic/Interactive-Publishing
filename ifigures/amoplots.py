from .my_plots import *
from .latex2png import latex2png
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import pyvista as pv
from io import BytesIO
from PIL import Image

class EnergyLevels:
    
    def __init__(self):
        self.label = []
        self.locationX = []
        self.locationY = []
        self.state = None
        self.arrows = []
    
    def add(self, label, locationX, locationY):
        self.label.append(label)
        self.locationX.append(locationX)
        self.locationY.append(locationY)
        
    def setState(self, state):
        assert len(state) == len(self.label), "state array lenght should be the same as number of states"
        self.state = np.array(state)
        
    def clearState(self):
        self.state = None
        
    def getTotalStates(self):
        return len(self.locationX)
    
    
    def addArrow(self, fromStateIndex, toStateIndex, label="", style="<->", color="k", strength=1,
                 detuning = None):
        """
            Args:
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
        
    
    def plot(self, axis, labels=False, linewidth=4, length=0.7, stateBlob=500, fontsize=14,
             debug=False, dpi=70, drivingStrenghtToWidth=True):
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
                file = generator.make_png(self.arrows[i][2], fontsize=fontsize, dpi=dpi, border=[5,5,5,5])
                arr_image = plt.imread(file, format='png')

                imagebox = OffsetImage(arr_image)
                # axis.plot([middle[0]],[middle[1]], "bo")
                ab = AnnotationBbox(imagebox, xy=(middle[0], middle[1]), pad=0, frameon=debug)
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
            
def blobAnnotate(axis,
                 blobX, blobY,
                 textX, textY,
                 text,
                 blobSize=100, linewidth=3, fontsize=12,
                 color=cDUbb, curvatureSign="+", zorder=-1):
    axis.scatter([blobX],[blobY], s=blobSize, c=color)
    curvatureSign = "+"
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
    axis.axvspan(fromX, toX, color=color, zorder=zorder)
    

def yAnnotate(axis, fromY, toY, color=cDUy, zorder=-2):
    axis.axhspan(fromY, toY, color=color, zorder=zorder)
    
        
def equation(latex, axis,fontsize=10, dpi=100, border=[4,4,4,4], debug=False,
             x=0.1, y=1):
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

        self.p = pv.Plotter(shape=(1, 1),
                       multi_samples=1,
                       window_size=(resolution * 600, resolution * 600),
                       off_screen=True,
                           notebook=False)
        self.p.set_background(cDUsky, top="white")
        
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
    
    def addStateBlob(self, x,y,z, color=cDUrr):
        small = pv.Sphere(center=np.array([x, y, z])*self.r, radius=self.r / 3 * 0.2)
        self.p.add_mesh(small, opacity=1.0, color=color, smooth_shading=True)
        pass
    
    def addStateArrow(self, x,y,z, color=cDUbbbb):
        arrow=pv.Arrow(start=(0.0, 0.0, 0.0), direction=np.array([x,y,z]) * self.r,
                       tip_length=0.25, tip_radius=0.1, tip_resolution=20, shaft_radius=0.05, 
                       shaft_resolution=20, scale=self.r)
        self.p.add_mesh(arrow, opacity=1.0, color=color, smooth_shading=True)
    
    def addTrajectory(self, trajectoryXYZ):
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
             labelDPI=600,
             label=[r"$|e\rangle$",
                         r"$|g\rangle$",
                         r"$\frac{|e\rangle+|g\rangle}{\sqrt{2}}$",
                         r"$\frac{|e\rangle+i|g\rangle}{\sqrt{2}}$"
                        ],
              labelOffset=None
            ):
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
                                                dpi=labelDPI)
                    l = white_to_transparency(Image.open(labelLatex))
                    im.paste(l, labelOffset[i], l)
                    
                axis.imshow(im)
            else:            
                axis.imshow(self.p.image)
                
            if not debug:   
                axis.set_axis_off()
            

    