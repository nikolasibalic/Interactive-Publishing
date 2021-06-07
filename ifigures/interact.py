from collections import OrderedDict
import itertools
import base64
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import binascii
from html import escape

from PIL import Image
import numpy as np

from string import ascii_lowercase
from .latex2png import latex2png

import matplotlib as mpl
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['xtick.major.size'] = 8
mpl.rcParams['ytick.major.size'] = 8
mpl.rcParams['xtick.minor.size'] = 4
mpl.rcParams['ytick.minor.size'] = 4
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['axes.facecolor'] = 'None'
mpl.rcParams['figure.facecolor']= 'None'

def _get_png(obj):
    if isinstance(obj, mpl.figure.Figure):
        canvas = FigureCanvas(obj)
        png_output = BytesIO()
        canvas.print_png(png_output)
        png_rep = png_output.getvalue()
    else:
        # assume it's png
        png_rep = obj
    if png_rep is not None:
        if isinstance(obj, plt.Figure):
            plt.close(obj)  # keep from displaying twice
    return png_rep


def _get_html(obj):
    """Get the HTML representation of an object"""

    png_rep = _get_png(obj)

    if png_rep is not None:
        return ('<img alt="figure" src="data:image/png;'
                'base64,{0}"/>'.format(base64.b64encode(png_rep).decode("utf-8") ))
    else:
        return "<p> {0} </p>".format(str(obj))

def _eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))

class InteractiveFigure(object):
    """Interactive Figure Object"""

    css_beatify = """
    <style type="text/css">

    /* source-sans-pro-regular - latin-ext_latin */
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 400;
  src: url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.eot'); /* IE9 Compat Modes */
  src: local(''),
       url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.woff2') format('woff2'), /* Super Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.woff') format('woff'), /* Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.ttf') format('truetype'), /* Safari, Android, iOS */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-regular.svg#SourceSansPro') format('svg'); /* Legacy iOS */
}

/* source-sans-pro-600 - latin-ext_latin */
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 600;
  src: url('./fonts/source-sans-pro-v14-latin-ext_latin-600.eot'); /* IE9 Compat Modes */
  src: local(''),
       url('./fonts/source-sans-pro-v14-latin-ext_latin-600.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-600.woff2') format('woff2'), /* Super Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-600.woff') format('woff'), /* Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-600.ttf') format('truetype'), /* Safari, Android, iOS */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-600.svg#SourceSansPro') format('svg'); /* Legacy iOS */
}

/* source-sans-pro-700 - latin-ext_latin */
@font-face {
  font-family: 'Source Sans Pro';
  font-style: normal;
  font-weight: 700;
  src: url('./fonts/source-sans-pro-v14-latin-ext_latin-700.eot'); /* IE9 Compat Modes */
  src: local(''),
       url('./fonts/source-sans-pro-v14-latin-ext_latin-700.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-700.woff2') format('woff2'), /* Super Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-700.woff') format('woff'), /* Modern Browsers */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-700.ttf') format('truetype'), /* Safari, Android, iOS */
       url('./fonts/source-sans-pro-v14-latin-ext_latin-700.svg#SourceSansPro') format('svg'); /* Legacy iOS */
}
     body{
       font-family: 'Source Sans Pro', sans-serif;
       }
    select{
        padding: 5px 10px;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        background-color: transparent;
        border: 4px solid #7E317B;
        border-radius: 10px;
    }
    </style>

    """

    css_style = """
    <style type="text/css">
div.left{
margin-left:10px;
float:left;
width:300px;
vertical-align: middle;
}
div.right{
float:left;
width:300px;
}
div.wrap{
display:inline-block;
}

input[type=range] {
  height: 34px;
  -webkit-appearance: none;
  margin: 10px 0;
  width: 100%;
  background-color:inherit;
}
input[type=range]:focus {
  outline: none;
}
input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 0px 0px 0px #000000;
  background: #968E85;
  border-radius: 8px;
  border: 2px solid #FFFFFF;
}
input[type=range]::-webkit-slider-thumb {
  box-shadow: 1px 1px 0px #FFFFFF;
  border: 6px solid #7E317B;
  height: 21px;
  width: 21px;
  border-radius: 19px;
  background: #FFFFFF;
  cursor: pointer;
  -webkit-appearance: none;
  margin-top: -10.5px;
}
input[type=range]:focus::-webkit-slider-runnable-track {
  background: #968E85;
}
input[type=range]::-moz-range-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 0px 0px 0px #000000;
  background: #968E85;
  border-radius: 8px;
  border: 2px solid #FFFFFF;
}
input[type=range]::-moz-range-thumb {
  box-shadow: 1px 1px 0px #FFFFFF;
  border: 6px solid #7E317B;
  height: 21px;
  width: 21px;
  border-radius: 19px;
  background: #FFFFFF;
  cursor: pointer;
}
input[type=range]::-ms-track {
  width: 100%;
  height: 8px;
  cursor: pointer;
  animate: 0.2s;
  background: transparent;
  border-color: transparent;
  color: transparent;
}
input[type=range]::-ms-fill-lower {
  background: #968E85;
  border: 2px solid #FFFFFF;
  border-radius: 16px;
  box-shadow: 0px 0px 0px #000000;
}
input[type=range]::-ms-fill-upper {
  background: #968E85;
  border: 2px solid #FFFFFF;
  border-radius: 16px;
  box-shadow: 0px 0px 0px #000000;
}
input[type=range]::-ms-thumb {
  margin-top: 1px;
  box-shadow: 1px 1px 0px #FFFFFF;
  border: 6px solid #7E317B;
  height: 21px;
  width: 21px;
  border-radius: 19px;
  background: #FFFFFF;
  cursor: pointer;
}
input[type=range]:focus::-ms-fill-lower {
  background: #968E85;
}
input[type=range]:focus::-ms-fill-upper {
  background: #968E85;
}
span.cbseparator{
display:inline-block;
margin:0px;
padding:0px;
height:10px;
width:30px;
}

input[type=range].viridisrange::-moz-range-track {
  -moz-appearance: none;
  background: rgba(59,173,227,1);
  background: -moz-linear-gradient(45deg,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -webkit-gradient(left bottom, right top,color-stop(0%, rgba(68,1,84,1),color-stop(5%, rgba(71,22,105,1),color-stop(11%, rgba(71,42,121,1),color-stop(17%, rgba(67,60,132,1),color-stop(23%, rgba(60,77,138,1),color-stop(29%, rgba(53,93,140,1),color-stop(35%, rgba(46,108,142,1),color-stop(41%, rgba(40,122,142,1),color-stop(47%, rgba(35,137,141,1),color-stop(52%, rgba(30,151,138,1),color-stop(58%, rgba(32,165,133,1),color-stop(64%, rgba(46,178,124,1),color-stop(70%, rgba(69,191,111,1),color-stop(76%, rgba(100,203,93,1),color-stop(82%, rgba(136,213,71,1),color-stop(88%, rgba(175,220,46,1),color-stop(94%, rgba(215,226,25,1),color-stop(100%, rgba(253,231,36,1)
);
  background: -webkit-linear-gradient(45deg,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -o-linear-gradient(45deg,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -ms-linear-gradient(45deg,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: linear-gradient(45deg,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  height: 8px;
}
input[type=range].viridisrange::-webkit-slider-runnable-track {
  -webkit-appearance: none;
  background: rgba(59,173,227,1);
  background: -moz-linear-gradient(45deg, ,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -webkit-gradient(left bottom, right top, color-stop(0%, rgba(68,1,84,1),color-stop(5%, rgba(71,22,105,1),color-stop(11%, rgba(71,42,121,1),color-stop(17%, rgba(67,60,132,1),color-stop(23%, rgba(60,77,138,1),color-stop(29%, rgba(53,93,140,1),color-stop(35%, rgba(46,108,142,1),color-stop(41%, rgba(40,122,142,1),color-stop(47%, rgba(35,137,141,1),color-stop(52%, rgba(30,151,138,1),color-stop(58%, rgba(32,165,133,1),color-stop(64%, rgba(46,178,124,1),color-stop(70%, rgba(69,191,111,1),color-stop(76%, rgba(100,203,93,1),color-stop(82%, rgba(136,213,71,1),color-stop(88%, rgba(175,220,46,1),color-stop(94%, rgba(215,226,25,1),color-stop(100%, rgba(253,231,36,1)

);
  background: -webkit-linear-gradient(45deg, ,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -o-linear-gradient(45deg, ,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: -ms-linear-gradient(45deg, ,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  background: linear-gradient(45deg, ,rgba(68,1,84,1) 0%,rgba(71,22,105,1) 5%,rgba(71,42,121,1) 11%,rgba(67,60,132,1) 17%,rgba(60,77,138,1) 23%,rgba(53,93,140,1) 29%,rgba(46,108,142,1) 35%,rgba(40,122,142,1) 41%,rgba(35,137,141,1) 47%,rgba(30,151,138,1) 52%,rgba(32,165,133,1) 58%,rgba(46,178,124,1) 64%,rgba(69,191,111,1) 70%,rgba(100,203,93,1) 76%,rgba(136,213,71,1) 82%,rgba(175,220,46,1) 88%,rgba(215,226,25,1) 94%,rgba(253,231,36,1) 100%
);
  height: 8px;
}
</style>
    """

    standalone_template = """
    <!doctype html>
    <head>
     <meta charset="utf-8">
     <title>Interactive figure</title>

    <script type="text/javascript">
      var mergeNodes = function(a, b) {{
        return [].slice.call(a).concat([].slice.call(b));
      }}; // http://stackoverflow.com/questions/914783/javascript-nodelist/17262552#17262552
      function interactUpdate(div){{
         div = div.parentNode.parentNode;
         var outputs = document.getElementById("outputs").children;

         //var controls = div.getElementsByTagName("input");
         var controls = mergeNodes(div.getElementsByTagName("input"), div.getElementsByTagName("select"));
         function nameCompare(a,b) {{
            return a.getAttribute("name").localeCompare(b.getAttribute("name"));
         }}
         controls.sort(nameCompare);
         var value = "";
         for(i=0; i<controls.length; i++){{
           if((controls[i].type == "range") || controls[i].checked){{
             var controlValue = controls[i].value;
             if (!isNaN(parseFloat(controlValue))){{
                 controlValue = parseFloat(controlValue).toExponential(6);
             }}
             value = value + controls[i].getAttribute("name") + controlValue;
           }}
           if(controls[i].type == "select-one"){{
             value = value + controls[i].getAttribute("name") + controls[i][controls[i].selectedIndex].value;
           }}
         }}
         for(i=0; i<outputs.length; i++){{
           var name = outputs[i].getAttribute("id");
           if(name == value){{
              outputs[i].style.display = 'block';
           }} else if(name != "controls"){{
              outputs[i].style.display = 'none';
           }}
         }}
      }}
    </script>
    {css}
    </head>

    <body>

    <div>
      <div id="outputs">
          {outputs}
      </div>
      {widgets}
    </div>
    </body>
    """

    subdiv_template = """
    <div id="{name}" style="display:{display}">
      {content}
      <div class="ifigurecaption">
      {caption}
      </div>
    </div>
    """

    @staticmethod
    def _get_strrep(val):
        """Need to match javascript string rep"""
        # TODO: is there a better way to do this?
        if isinstance(val, str):
            return val
        else:
            return _eformat(val, 6, 1)

    def __init__(self, function, **kwargs):
        # TODO: implement *args (difficult because of the name thing)
        # update names
        for name in kwargs:
            kwargs[name] = kwargs[name].renamed(name)

        self.widgets = OrderedDict(kwargs)
        self.function = function
        self.fileName = None
        self.overallCaption = ""

    def _output_html(self):
        names = [name for name in self.widgets]
        values = [widget.values() for widget in self.widgets.values()]
        defaults = tuple([widget.default for widget in self.widgets.values()])

        #Now reorder alphabetically by names so divnames match javascript
        names,values,defaults = zip(*sorted(zip(names,values,defaults),
                                            key=lambda tup: tup[0].lower()))

        divnames = [''.join(['{0}{1}'.format(n, self._get_strrep(v))
                             for n, v in zip(names, vals)])
                    for vals in itertools.product(*values)]
        display = [vals == defaults for vals in itertools.product(*values)]

        tmplt = self.subdiv_template

        r = []
        i = 0
        for vals in itertools.product(*values):
            figure = self.function(**dict(zip(names, vals)))
            r.append(tmplt.format(name=divnames[i],
                                    display="block" if display[i] else "none",
                                    content=_get_html(figure[0]),
                                    caption=escape(figure[1])))
            i += 1
        return "".join(r)


    def _widget_html(self):
        return "\n<br>\n".join([widget.html()
                                for name, widget in sorted(self.widgets.items())])

    def html(self, beautify=True):
        return self.standalone_template.format(css=self.css_style + (self.css_beatify if beautify else ""),
                                                   outputs=self._output_html(),
                                                   widgets=self._widget_html())

    def saveStandaloneHTML(self, fileName):
        self.fileName = fileName
        file = open(fileName, "w")
        file.write(self.html())
        file.close()
        self.overallCaption = ""
        return("Interactive figure saved in file %s" % fileName)


    def saveStaticFigure(self, fileName, values=None, figuresPerRow=2,
                        labelPanels=True, dpi=300, labelSize=10,
                        labelOffset=(10,10), labelGenerator=None):
        names = [name for name in self.widgets]

        if values == None:
            valueRanges = [widget.values() for widget in self.widgets.values()]
            values = [vals for vals in itertools.product(*valueRanges)]

        figureIndex = 0
        rowIndex = 0
        rows = []
        overallCaption = ""

        generator = latex2png()

        while (figureIndex < len(values)):
            imgs = []
            rowIndex = 0

            while (figureIndex < len(values) and rowIndex < figuresPerRow):
                if (labelGenerator is None):
                    if (len(values) <= 25):
                        label = "(" + ascii_lowercase[figureIndex] + ")"
                    else:
                        label = "(%d)" % figureIndex
                    if (labelPanels):
                        labelLatex = generator.make_png(label,
                                                   fontsize=labelSize, dpi=dpi)
                else:
                    label, labelLatex = labelGenerator(figureIndex,
                                                       dict(zip(names, values[figureIndex])))

                fig, caption = self.function(**dict(zip(names, values[figureIndex])))

                if figureIndex != 0: overallCaption += ", "
                overallCaption +=  label + " " + caption

                png = _get_png(fig)
                imgs.append(Image.open(BytesIO(png)))

                if labelPanels:
                    l = Image.open(labelLatex)
                    imgs[-1].paste(l, labelOffset,l.convert('RGBA'))

                figureIndex += 1
                rowIndex += 1

            if rowIndex < figuresPerRow:
                imageSize = imgs[0].size
                fill = Image.new('RGBA',
                                imageSize,
                                (255, 255, 255,0))  # White
                while (rowIndex < figuresPerRow):
                    imgs.append(fill)
                    rowIndex += 1

            r = [np.asarray(i) for i in imgs]

            combined = Image.fromarray(np.hstack(r))
            rows.append(np.asarray(combined))


        image = Image.fromarray(np.vstack(rows))
        image.save(fileName, dpi=(dpi,dpi))

        self.fileName = fileName
        self.overallCaption = overallCaption
        return



    def show(self, width=800, height=700):
        """
        Shows static png or interactive html figure in Jupyter notebook
        """
        assert self.fileName is not None, "before calling show(), save figure using saveStandaloneHTML  or  saveStaticFigure"
        if (self.overallCaption != ""): print(self.overallCaption)
        from IPython.display import IFrame
        return IFrame(src=self.fileName, width=width, height=height)

    def _repr_html_(self):
        return self.html()
