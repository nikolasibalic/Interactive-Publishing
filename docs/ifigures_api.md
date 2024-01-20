# API Documentation 


::: ifigures.InteractiveFigure  

!!! tip "Why use interactive figure?"
    This is discussed in [Physics World blogpost and comment](example_gallery.md/#motivation-and-goals). In short, we want to allow exploration of many untold stories and edge cases. To build intuition, connections and maybe get
    inspired for further work!

!!! Example "Simple interactive figure"
    ```python
    from ifigures import InteractiveFigure, RangeWidget, RangeWidgetViridis, RadioWidget,DropDownWidget
    import numpy as np
    import matplotlib.pyplot as plt

    def plot(amplitude, omega, time, color, f):
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.linspace(0, 10, 1000)
        if f=="sin":
            func = np.sin
        else:
            func = np.cos
        ax.plot(x, amplitude * func(omega*x), color=color,
                lw=5, alpha=0.4)
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel(r"Time, $t$")
        ax.set_ylabel(r"$f(t)$")
        ax.set_title("Figure title. f(x) = amplitude * %s(omega*x)"
                    % (f))
        ax.axvspan(time-0.1, time+0.1, color="0.9")
        
        caption = "Figure caption. Amplitude = %.2f, omega = %.2f, color = %s, f(t) = amplitude * %s(omega*x). Highlighted time = %.2f" % (amplitude, omega, color, f, time)
        return (fig, caption)


    figure_example1 = InteractiveFigure(plot,
                amplitude=RangeWidget(0.1, 0.9, 0.4),
                omega=RangeWidget(1.0, 5.01, 2.0),
                time=RangeWidgetViridis(1,9,4),
                color=RadioWidget(['blue', 'green', 'red']),
                f=DropDownWidget(["sin","cos"]))
    figure_example1.saveStandaloneHTML("interactive_figure.html")

    ```
    The above code generates

    <iframe src="../interactive_figure.html" width="100%" height="780"></iframe>

!!! example "Saving static version for printing"
    Even when we create interactive figures, sometimes we do need to provide also
    printed option. This can be easily done with `saveStaticFigure` method, which
    we demonstrate on the previous example
    ```python
    from ifigures import InteractiveFigure, RangeWidget, RangeWidgetViridis, RadioWidget,DropDownWidget
    import numpy as np
    import matplotlib.pyplot as plt

    def plot(amplitude, omega, time, color, f):
        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.linspace(0, 10, 1000)
        if f=="sin":
            func = np.sin
        else:
            func = np.cos
        ax.plot(x, amplitude * func(omega*x), color=color,
                lw=5, alpha=0.4)
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel(r"Time, $t$")
        ax.set_ylabel(r"$f(t)$")
        ax.set_title("Figure title. f(x) = amplitude * %s(omega*x)"
                    % (f))
        ax.axvspan(time-0.1, time+0.1, color="0.9")

        caption = "Figure caption. Amplitude = %.2f, omega = %.2f, color = %s, f(t) = amplitude * %s(omega*x). Highlighted time = %.2f" % (amplitude, omega, color, f, time)
        return (fig, caption)


    figure_example1 = InteractiveFigure(plot,
                amplitude=RangeWidget(0.1, 0.9, 0.4),
                omega=RangeWidget(1.0, 5.01, 2.0),
                time=RangeWidgetViridis(1,9,4),
                color=RadioWidget(['blue', 'green', 'red']),
                f=DropDownWidget(["sin","cos"]))
    figure_example1.saveStaticFigure("test.png",
                                    [[0.5,1,1.5,"red","sin"],[0.5,3,1.6,"blue","sin"],
                                    [0.5,1,1.5,"red","cos"],[0.5,3,1.6,"blue","cos"]])
    print(figure_example1.overallCaption)
    
    ```
    ![static figure example](assets/example_static.png)

    
    `(a) Amplitude = 0.50, omega = 1.00, color = red, f(t) = amplitude * sin(omega*x). Highlighted time = 1.50, (b) Amplitude = 0.50, omega = 3.00, color = blue, f(t) = amplitude * sin(omega*x). Highlighted time = 1.60, (c) Amplitude = 0.50, omega = 1.00, color = red, f(t) = amplitude * cos(omega*x). Highlighted time = 1.50, (d) Amplitude = 0.50, omega = 3.00, color = blue, f(t) = amplitude * cos(omega*x). Highlighted time = 1.60`
    

## Input controls for interactive figures

Inputs for interactive figures are range sliders (including specially coloured `RangeWidgetViridis` that we use extensively to mark time evolution in dynamics), drop-down select boxes, and radio buttons, in some combination.

::: ifigures.RangeWidget

!!! Example "Example: a static snapshot of input control widget"
    ![Range widget](assets/widget_range.png)

::: ifigures.RangeWidgetViridis

!!! Example "Example: a static snapshot of input control widget"
    ![Range widget viridis for time](assets/widget_range_viridis.png)

::: ifigures.RadioWidget

!!! Example "Example: a static snapshot of input control widget"
    ![Radio widget](assets/widget_radio_button.png)

::: ifigures.DropDownWidget

!!! Example "Example: a static snapshot of input control widget"
    ![Drop down widget](assets/widget_dropdown.png)

## Interactive timeline

::: ifigures.InteractiveTimeline

!!! tip "Why use timelines?"
    Scientific progress is huge community effort, often undertaken over many decades. Our timelines also have **thickness** since we recognize the importance of cross-breeding of ideas and insights from different "rivers" of thought and experimentation. Timeline format allows readers to explore and understand all the connection in historical development.

!!! example "Timeline for development of electromagnetism"
    [See example here.](./timeline_electromagnetism.html)



## Annotation features for Matplotlib plots
::: ifigures.blobAnnotate
::: ifigures.xAnnotate
::: ifigures.yAnnotate

!!! example "Example of annotations"
    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from ifigures import *
    from ifigures.style import *  # for color scheme

    fig, ax=plt.subplots(1,1,figsize=(3*1.6, 3))

    some_data = np.linspace(0,8,100)

    ax.plot(some_data, some_data, "-", color=cDUb)
    ax.plot(some_data, np.sqrt(some_data)+1.23, "-", color=cDUr)
    xAnnotate(ax, 0.5, 5.5, color=cDUy)
    blobAnnotate(ax,6,6, 6.5,1,"Nothing! $\Omega_2$", color=cDUggg)
    blobAnnotate(ax,3,3, 4,1,"Something", color=cDUbb, blobSize=100)

    plt.show()
    ```
    produces 

    ![Annotation example](assets/annotation_example.png)

!!! tip "Why should one use annotations?"
    Modern figures in reserach papers are often dense with information,
    and **presume substantial previous knowledge** in order to be able to
    focus the sight on few actually
    relevant and interesting points. When working with interactive figures
    we are not bound to one "dead" version of plot on the paper, but can
    show multiple layers of annotations to help final knowledge consumers
    digest important features first, **guiding their focus** in interpretation
    gently.
    More widely, teaching **plot literacy** to wider population is crucial for
    informed decision-making.

::: ifigures.equation

## Additional LaTeX commands

Some special commands are defined by default for use in equation environment

- `\ketbra{A,B}` results in $| A \rangle\langle B |$
- `\braket{A,B}` results in $\langle A | B \rangle$
- **Highlighting:** parts of equation can be higlighted in purple `\hp{...}`, yellow `\hy{...}`, blue `\hb{...}`, gray `\hg{...}`, darker gray `\hgg{...}`, golden `\ho{...}` and red background `\hr{...}`.
- **Frames:** parts of the equation can be framed in purple `fp{...}`, blue `\fb{...}`,
  gray `\fg{...}`, golden `\fg{...}`, and red `fr{...}` frames.

!!! example "Example of equation with additional LaTeX commands"
    ```python
    import matplotlib.pyplot as plt
    from ifigures import *

    fig, ax=plt.subplots(1,1)

    equation(r"""
    $\begin{matrix} \mathcal{H} &=& \hy{\frac{\Omega_1}{2}}~ \ketbra{e}{g}  +\hr{ \Omega_2/2}~ \ketbra{e}{m} \\
    \mathrm{highlight} &:& \hp{\textrm{hp}}~~~\hy{\textrm{hy}} ~~~\hb{\textrm{hb}} ~~~\hg{\textrm{hg}}
    ~~~\hgg{\textrm{hgg}} ~~~\ho{\textrm{ho}}~~~\hr{\textrm{hr}} \\
    \mathrm{frame}& : & \fp{\textrm{fp}}~~~\fb{\textrm{fb}}~~~ \fg{\textrm{fg}}~~~\fo{\textrm{fo}} ~~~\fr{\textrm{fr}}  \end{matrix}$
    """, ax,  fontsize=12, debug=False, x=0.5, y=0.5, dpi=300)

    plt.show()
    ```
    results in

    ![highlighted equations](assets/equation_example.png)

## Quantum state visualisations

::: ifigures.getComplexColor

!!! example "Mapping complex numbers to colors"
    ![Complex color mapping](assets/complex_color_mapping.png){width=300px  align=right}
    Mapping of complex number $A e^{i \phi}$ with amplitude $A$ and phase $\phi$
    to colours used by the library.
    Note that  complementary colours correspond
    to sign difference: green and red (like Italian flag), and yellow and blue.
    In the case the amplitude is zero, all colours are linearly approching white
    for amplitude $A \rightarrow 0$.


::: ifigures.BlochSphere

!!! Example "Bloch sphere example"
    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from ifigures.amoplots import *

    from scipy.linalg import kron, eig

        
    a = np.linspace(0,8,100)

    f = plt.figure(figsize=(6,8))

    ax1 = plt.subplot(1,1,1)

    def trajectory(gi):
        G=gi*2.0 #input parameter
        Omega=10.0
        Delta=10.0
        phiL=0.1*np.pi/2
        H=np.array([[Delta/2, (Omega/2)*np.exp(-1.j*phiL)],[(Omega/2)*np.exp(1.j*phiL), -Delta/2] ])
        I2=np.eye(2,2)
        Hrho=kron(H,I2)
        rhoH=kron(I2,np.conj(H))
        L=np.array([[0,0,0,G],[0,-G/2,0,0],[0,0,-G/2,0],[0,0,0,-G] ])
        evals, evecs = eig(-1.j*(Hrho-rhoH)+L)
        evecs=np.mat(evecs)
        rho0=np.zeros((4,1))
        rho0[0]=1.0
        npts=50
        tmax=2*np.pi/np.sqrt(Omega**2+Delta**2)
        t=np.linspace(0,tmax,npts)
        u=np.zeros(npts)
        v=np.zeros(npts)
        w=np.zeros(npts)
        for i in range(0,npts):
            rho=evecs*np.mat(np.diag(np.exp(evals*t[i])))*np.linalg.inv(evecs)*rho0
            u[i]=(rho[1]+rho[2]).real
            v[i]=(1.j*(rho[1]-rho[2])).real
            w[i]=(rho[0]-rho[3]).real
        return np.column_stack((u, v, w))
        
    bs = BlochSphere()
    bs.addStateBlob(0,0,1)
    dynamics = trajectory(3)
    bs.addTrajectory(dynamics)
    bs.addStateBlob(0,0,1)
    bs.addStateBlob(*dynamics[-1,:])
    bs.addStateArrow(*dynamics[-1,:],)
    bs.plot(axis=ax1)

    ```
    ![Bloch sphere example](assets/bs_example.png)

    Example above shows Bloch sphere, with annotated key points of the sphere,
    state trajectory in time shown as line with time encoded in viridis gradient,
    state arrow, and two blobs highlighting in this case start and end of the
    evolution. We also notice how trajectory of the system departs the
    surface of the Bloch sphere and dives into inside due to decoherence.
    Note that actual Bloch sphere plot is only last few lines of code, the rest
    is calculation of dynamics.

::: ifigures.DensityMatrix

!!! Example "Densitry matrix visualisation"
    ```python
    import matplotlib.pyplot as plt
    from ifigures.amoplots import *

    fig, ax=plt.subplots(1,1,figsize=(3, 3))

    dm = DensityMatrix()
    dm.plot(ax, [[1/2, 1j/2], [-1j/2, -1/2]])

    plt.show()
    ```
    ![tst](assets/dm_example.png)

!!! tip "Why use coloured density matrixes"
    They are capable of quickly conveying numerical results, arguably providing
    better grasp of underlying physics than 3D bar charts. And of course
    they work for multi-level systems.


::: ifigures.EnergyLevels

!!! example
    ```python    
    import matplotlib.pyplot as plt 
    import numpy as np
    from ifigures import *
    from ifigures.style import *

    fig, ax1=plt.subplots(1, 1, figsize=(3 * 1.6, 3))

    # Hamiltonian - driving
    omega_1 = np.pi/1.5
    omega_2 = np.pi * np.exp(1j * 0.5 * np.pi)

    # Current state in the basis defined in order given below
    state = [1/np.sqrt(2), -1j/2, -1/2]

    el = EnergyLevels()
    # basis - energy levels and their relative positions
    el.add(r"$|\mathrm{g}\rangle$", 0, 0)    # |g>
    el.add(r"$|\mathrm{m}\rangle$", 1, 2.9)  # |m>
    el.add(r"$|\mathrm{e}\rangle$", 2, 0.2)  # |e>

    el.addArrow(0,1,"",
                strength=omega_1,
                style="<->", color="red")
    el.addArrow(1,2,"",
                strength=omega_2,
                style="<->")

    el.setState([1/np.sqrt(2), -1j/2,-1/2])

    el.plot(ax1)


    plt.savefig("test1.png")
    plt.show()
    ```

    ![example of state with dynamics indicated](assets/example_state.png)

    - State blob with color and size correspond to phase and amplitude
    - small gray dot on the blobs indicates phasor tip, to allow also for colour blind readout
    - external arches correspond to rotation of the small amplitude contribution for
    amplitude going from lower to higher states, while inner circles arches correspond
    to rotation of the small amplitude contribution from higher states to lower states.
    - diameter of arched driving connection, and strength of the corresponding arrow, for
    the drivings is proportional to relative strengths of driving.

!!! tip "Why use this new energy level and state representation"
    It can show features even in 2 level systems that are not visible on
    Bloch sphere. Equally it can be generalized to many level and multi-partite
    systems directly. Representation is such that it allows "visual integration"
    of coherent dynamics. E.g. it is possible to directly see not only destructive
    interference responsible for Electromagnetically Induced Transparency, but
    also understand importance of laser phase. For many examples check the
    [*An Interactive Guide to Quantum Optics*](https://iopscience.iop.org/book/mono/978-0-7503-2628-5), Nikola Šibalić and C Stuart Adams, IOP Publishing (2024)