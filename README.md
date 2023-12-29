Interactive text and figures
============================

This project provides quick starting point for anyone who wants to experiment
with **interactive text and figures** in their electronic publications
(EPUB3 / HTML5 + JavaScript). One possible reason why one would use interactive
text and figures is to **communicate many possible stories** to the audience,
instead of usual single story line. See [Physics World blogpost](https://physicsworld.com/a/do-interactive-figures-help-physicists-to-communicate-their-science/).

Two templates and corresponding tools are provided.
Tools generate HTML/Javascript output that can be seen in
web-browsers and e-readers.
Generated examples don't have any external dependencies that need to be
downloaded from the Internet. They are completely self contained,
and be seen on all devices (even without Internet access),
and they can be simply included in interactive texts/books in EPUB3 format,
as well as web-pages.

[**For detailed documentation and discussion of motivation and examples check here**](https://nikolasibalic.github.io/Interactive-Publishing/)

[![DOI](https://zenodo.org/badge/163100222.svg)](https://zenodo.org/badge/latestdoi/163100222)  [![PyPI version](https://badge.fury.io/py/Interactive-Publishing.svg)](https://badge.fury.io/py/Interactive-Publishing) 

---------


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
Overall license is BSD-3-Clause as outlined included in `LICENSE.md`.

This project uses [```TangleKit```](/TangleKit) package from this repository 
for creating interactive text. That package is based on 
on slightly modified and updated open-source
[Tangle.js](http://worrydream.com/Tangle/)
library of [Bret Victor](http://worrydream.com/ExplorableExplanations/).

Interactive figures use Matplotlib Python package and [```ifigures```](/ifigures)
package from this repository which is based
on updated and modified version of 
[ipywidgets-static](https://github.com/jakevdp/ipywidgets-static).
Compared to original package, dependency on IPython is removed,
Python 2 and 3 are supported now, and few bugs are fixed.

Licenses are inherited from the original projects mentioned above.
They are permissive, and allow reuse, with or without modification, but for
details check corresponding LICENSE files and code headers. 

