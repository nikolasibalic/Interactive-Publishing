Interactive text and figures
============================

This project provides quick starting point for anyone who wants to experiment
with **interactive text and figures** in their electronic publications
(EPUB3 / HTML5 + JavaScript). One possible reason why one would use interactive
text and figures is to **communicate many possible stories** to the audience,
instead of usual single story line.

Two templates and corresponding tools are provided.
Tools generate HTML/Javascript output that can be seen in
web-browsers and e-readers.
Generated examples don't have any external dependencies that would require
viewing only for devices connected on Internet. Instead, the all-including
examples can be seen on all devices, and they can be simply included in
interactive texts/books in EPUB3 format.

Interactive text
----------------

For interactive text template see
[```interactive_text.html```](interactive_text.html).
To ship your figure, provide to users .html file (with embedded JavaScript
calculations), together with TangleKit folder and Tangle.js accessible in
root folder of the figure .html.

You can start by changing text and calculation code in
[```interactive_text.html```](interactive_text.html).
Explore in-line documentation of [```TangleKit```](/TangleKit) for
more details.

This uses [```TangleKit```](/TangleKit) package from this repository that
is based on slightly modified and updated
[Tangle.js](http://worrydream.com/Tangle/)
library of [Bret Victor](http://worrydream.com/ExplorableExplanations/).

Interactive figures
-------------------

For interactive figure example see
[```interactive_figure.html```](interactive_figure.html). It is generated
by the provided Python file
```
python interactive_figure_generator.py
```

You can start building your own example by changing code in
[```interactive_figure_generator.py ```](interactive_figure_generator.py),
running Python to generate new
interactive figure, and observe results by realoading
[```interactive_figure.html```](interactive_figure.html) in any web-browser.

Example above uses Matplotlib Python package and [```ifigures```](/ifigures)
package from this repository which is based
on updated and modified version of 
[ipywidgets-static](https://github.com/jakevdp/ipywidgets-static)
(dependency on IPython from original
package is removed, and Python 2 and 3 are supported now).

Note on implementation
----------------------
Interactive text example implements simple calculations in JavaScript. More
complex calculations should be precalculated and provided as look-up tables.

Interactive figures generate figures for all possible combinations of the
input. Control JavaScripts then displays just images corresponding to
selected combination of input parameters, while all other images are hidden.
This can make files relatively large, but it allows their viewing on devices
with minimal computational resources, like ereaders, and old phones.

License
-------
Licenses are inherited from the original projects mentioned above.
They are permissive, and allow reuse, with or without modification, but for
details check corresponding LICENSE files and code headers.
