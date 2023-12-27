# `ifigures` API


::: ifigures.InteractiveFigure  

!!! question "Why use interactive figure?"
    This is discussed in Physics World blogpost and comment. In short, we want to allow exploration of many untold stories and edge cases. To build intuition, connections and maybe get even some inspiration for further work and extensions!

::: ifigures.InteractiveTimeline

!!! question "Why use timelines?"
    Scientific progress is huge community effort, often undertaken over many decades. Our timelines also have **thickness** since we recognize the importance of cross-breeding of ideas and insights from different "rivers" of thought and experimentation. Timeline format allows readers to explore and understand all the connection in historical development.

!!! example "Timeline for development of electromagnetism"


## Input controls for interactive figures

Inputs for interactive figures are range sliders (including specially coloured `RangeWidgetViridis` that we use extensively to mark time evolution in dynamics), drop-down select boxes, and radio buttons, in some combination.

::: ifigures.RadioWidget
::: ifigures.RangeWidget
::: ifigures.RangeWidgetViridis
::: ifigures.DropDownWidget

## Annotation features for Matplotlib plots
::: ifigures.blobAnnotate
::: ifigures.xAnnotate
::: ifigures.yAnnotate
::: ifigures.equation

## Additional LaTeX commands

Some special commands are defined by default for use in equation environment

- `\ketbra{A,B}` results in $| A \rangle\langle B |$
- `\braket{A,B}` results in $\langle A | B \rangle$
- **Highlighting:** parts of equation can be higlighted in purple `\hp{...}`, yellow `\hy{...}`, blue `\hb{...}`, gray `\hg{...}`, lighter gray `\hgg{...}`, golden `\ho{...}` and red background `\hr{...}`.
- **Frames** 

## Quantum state visualisations

::: ifigures.BlochSphere
::: ifigures.EnergyLevelsNew