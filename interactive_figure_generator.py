from ifigures import InteractiveFigure, RangeWidget, RadioWidget,DropDownWidget
import numpy as np
import matplotlib.pyplot as plt

def plot(amplitude, omega, color, f):
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
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Figure title. f(x) = amplitude * %s(omega*x)"
                 % (f))
    
    caption = "Figure caption. Amplitude = %.2f, omega = %.2f, color = %s, f(x) = amplitude * %s(omega*x)" % (amplitude, omega, color, f)
    return (fig, caption)


figure_example1 = InteractiveFigure(plot,
               amplitude=RangeWidget(0.1, 1.0, 0.2),
               omega=RangeWidget(1.0, 5.0, 2.0),
               color=RadioWidget(['blue', 'green', 'red']),
               f=DropDownWidget(["sin","cos"]))
figure_example1.saveStandaloneHTML("interactive_figure.html")
