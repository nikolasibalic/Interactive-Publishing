# Interactive publishing
  
This is documentation page for [Interactive-Publishing GitHub repository](https://github.com/nikolasibalic/Interactive-publishing)
containing templates and tools for creating [interactive figures](#interactive-figure) and
[interactive text](#interactive-text) for publishing in EPUB3/HTML5.

This simple page incorporates interactive figure and
interactive text. For source and tools for creating your own interactive
resources for publishing in HTML and EPUB3, please see
[repository](https://github.com/nikolasibalic/Interactive-publishing).
Created interactive elements can be incorporated in eBooks, blogs, web pages...
or just uploaded online and shared with links.

??? question "How is this different compared to other widgets/interactive plots available?"
    This code strives to be as simple as possible, while providing key learning
    functionality. This means that generated plots are stand-alone web pages,
    with embedded minimal JavaScript code necessary for interactivity.
    For viewing interactive figures, no JavaScript is loaded from online, which
    means that everything can work in off-line environments.
    Also, no calculations are performed in the browser. Instead, everything is calculated,
    and interactive code just picks corrects static images. This ensures that
    assumed infrastructure can be dumb and very low performance. Goal is that
    it can work everywhere: from e-readers, to very old or very small computers.
    
    In short, in the words of Antoine de Saint-Exupery 
    >''A designer knows he has achieved perfection not when there is nothing left to add, but when there is nothing left to take away.''
    
    We tried to remove everything except minimum needed to achieve interactive
    learning. Focus is social outcome, not technological sophistication.
    [Click here to see more on motivation and goals](./example_gallery/#motivation-and-goals)

??? question "How to use interactive figures in presentations or online?"
    Since created figures are stand-alone `.html` pages, standard `iframe` support
    for embedding WebPages (remote or local `.html` files) in popular presentation 
    making software solutions is one way. Same goes if you want to embed them
    on your web-pages and blog posts.

    We do recommend also to checkout 
    [Caroline](https://github.com/nikolasibalic/Caroline),
    open-source Python framework
    for quick and simple creation of HTML presentations, that not only offers
    native support for inclusion of interactive figures, but also host of other
    features (including interaction with audience).

## Getting started

```
pip install interactive-publishing
```

**Optional dependancy** is LaTeX, that should be installed on the system and
available on command line interface for annotations.

## Examples

### Interactive text
Standalone interactive text can be seen
<a href="interactive_text.html">here</a> or as a part of the page bellow.
Purple elements can be changed by dragging or clicking, updating 
calculated values given in green.

<iframe src="./interactive_text.html" width="100%" height="200"></iframe>

### Interactive figure

  
Standalone interactive figure can be seen [here](interactive_figure.html)
 or as a part of the page bellow.

<iframe src="./interactive_figure.html" width="100%" height="780"></iframe>

Try creating your own interactive texts and figures for science teaching
and public communication. You can start by using templates from
<a href="https://github.com/nikolasibalic/Interactive-publishing">
Interactive-Publishing repository</a>.</p>

### Interactive timeline

[Click to see example](./timeline_electromagnetism.html)

## Domain packages

We provide some extensions useful for specific domains, in particular
quantum physics and atomic, molecular and optical (AMO) physics for visualising
quantum states and quantum dynamics. For more details [see here](../ifigures_api/#quantum-state-visualisations).



