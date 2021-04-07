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
               amplitude=RangeWidget(0.1, 0.9, 0.42),
               omega=RangeWidget(1.0, 5.01, 2.0),
               time=RangeWidgetViridis(1,9,4),
               color=RadioWidget(['blue', 'green', 'red']),
               f=DropDownWidget(["sin","cos"]))
figure_example1.saveStandaloneHTML("interactive_figure.html")
