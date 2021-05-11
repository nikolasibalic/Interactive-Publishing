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
from .my_plots import white_to_transparency

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

def _get_encoded_png(image, maxWidth=5000):
    size = image.size;
    if (size[0]>maxWidth):
        newSize = (int(image.size[0] * maxWidth/size[0]),
                   int(image.size[1] * maxWidth/size[0]) )
        image = image.resize(newSize)
    in_mem_file = BytesIO()
    image.save(in_mem_file, format = "PNG")
    # reset file pointer to start
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    return "data:image/png;base64,{0}".format(base64.b64encode(img_bytes).decode("utf-8"))
        
 
class InteractiveTimeline(object):
    
    standalone_template = r"""
    <!doctype html>
    <head>
     <meta charset="utf-8">
     <title>{title}</title>

<script type="text/javascript">

function showEvent(blockName) {{
    var x = document.getElementById("userManual");
    x.style.display = "none";

    var elements = document.getElementsByClassName("eventBox")

    for (var i = 0; i < elements.length; i++){{
        elements[i].style.display = "none";
    }}

    var x = document.getElementById(blockName);
    if (x.style.display === "none") {{
        x.style.display = "block";
    }} else {{
        x.style.display = "none";
    }}
    return false;
}}
</script>
    {css}
    </head>

    <body>

<img src="{backgroundImage}" width="{imageWidth}" height="{imageHeight}" alt="history_timeline" usemap="#timeline_map">

<map name="timeline_map">
  {imagemap}
</map>

{introduction}

{events}

    </body>
    """
    
    css = r"""

    
<style>

    /* source-sans-pro-regular - latin-ext_latin */
@font-face {{
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
}}

/* source-sans-pro-600 - latin-ext_latin */
@font-face {{
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
}}

/* source-sans-pro-700 - latin-ext_latin */
@font-face {{
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
}}
     body{{
       font-family: 'Source Sans Pro', sans-serif;
       }}
div.eventBox{{
margin-top:5px;
padding:15px;
width:{eventBoxWidth}px;
height:300px;
display: none;
background-color:#CFDAD1;
border-radius: 15px;
}}
.event_image{{
max-width: 500px;
max-height: 300px;
float:right;
margin-left:10px;
border-radius:10px;
}}
.userManual{{
margin-top:5px;
padding:15px;
width:{eventBoxWidth}px;
height:300px;
background-color:#CFDAD1;
border-radius: 15px;
text-align:left;
}}
a{{
  text-decoration: underline solid 2px #7E317B;
  color:black;
}}
.credits{{
  font-size: 10pt;
}}
.interactivecolor{{
  color:#7E317B;
}}
</style>
    """
    
    subdiv_template = r"""
    <div id="{name}" style="display:{display}">
      {content}
      <div class="ifigurecaption">
      {caption}
      </div>
    </div>
    """
    
    event_template = r"""
    <div class="eventBox" id="{eventId}">
  <img src="{imageName}" alt="image" class="event_image">
  <p><b>{year}</b> - {title} </p>
  <p>{text}</p>
  <p class="credits">
     {credits}
  </p>
</div>
    """
    
    event_template_no_image = r"""
    <div class="eventBox" id="{eventId}">
  <p><b>{year}</b> - {title} </p>
  <p>{text}</p>
</div>
    """
    
    imagemap_template = r"""
    <area shape="circle" coords="{x},{y},{radius}" alt="event16" href="javascript:return false;"  onclick="showEvent('{eventId}');">
    """
    
    intro_template = r"""
    <div class="userManual" id="userManual">
  <img src="{introimage}" alt="introduction" class="event_image">
    {introtext}
    {credits}
</div>
"""
    
    intro_template_no_image = r"""
    <div class="userManual" id="userManual">
    {introtext}
</div>
"""
    
    def __init__(self, startYear=1900, endYear=2020, clickMarker=None, backgroundImage=None, title="",
                introText='<p><b>Interactive timeline</b>: To explore events <span class="interactivecolor"><b>click on circles</b></span>.</p>',
                introImage=None, 
                introCredits=""):
        self.startYear = startYear
        self.endYear = endYear
        self.backgroundImage = backgroundImage
        self.title = title
        self.introText = introText
        self.introImage = introImage
        self.introCredits = introCredits
        self.events = []
        self.fileName = None
        self.clickMarker = Image.open(clickMarker)
    
    def addEvent(self, year, title, text, image=None, credits="", offsetY=0):
        self.events.append({"year" : year,
                        "title" : title,
                        "text" : text,
                        "image" : image,
                        "credits" : credits,
                        "offsetY" : offsetY})
        return
    
    def saveStandaloneHTML(self, fileName):
        eventsHTML = []
        imageMap = []
        
        im = Image.open(self.backgroundImage)
        
        for i, e in enumerate(self.events):
            eid = "event%d" % i
            
            imageSize = im.size
            positionX = (e["year"]- self.startYear) / (self.endYear - self.startYear)
            positionX *= imageSize[0]
            positionY = imageSize[1]/2 + e["offsetY"]
            positionX = "%.0d" % positionX
            positionY = "%.0d" % positionY
            
            im.paste(self.clickMarker,
                     (int(positionX) - self.clickMarker.size[0] // 2,
                      int(positionY) - self.clickMarker.size[1] // 2), self.clickMarker)
            
            imageMap.append(self.imagemap_template.format(
                x=positionX, y=positionY, radius=15, eventId=eid))
            # add to image symbol
            
            if e["image"] != None:
                sideImage = Image.open(e["image"])
                eventsHTML.append(self.event_template.format(eventId = eid,
                                               title=e["title"],
                                               imageName=_get_encoded_png(sideImage, maxWidth=900),
                                               year=e["year"],
                                               text=e["text"],
                                               credits=e["credits"]))
            else:
                eventsHTML.append(self.event_template_no_image.format(eventId = eid,
                                               title=e["title"],
                                               year=e["year"],
                                               text=e["text"]))
            
        if self.introImage is not None:
            intro = self.intro_template.format(image=self.image,
                                               introtext=self.introText,
                                               credits=self.introCredits)
        else:
            intro = self.intro_template_no_image.format(introtext=self.introText)
            
        eventsHTML = "".join(eventsHTML)
        imageMap = "".join(imageMap)
        

        
        r = self.standalone_template.format(title=self.title,
                                       css=self.css.format(eventBoxWidth=im.size[0]-30),
                                       backgroundImage=_get_encoded_png(im),
                                       imagemap=imageMap,
                                       imageWidth=im.size[0],
                                       imageHeight=im.size[1],
                                       introduction=intro, 
                                       events=eventsHTML
                                      )
        file = open(fileName, "w")
        file.write(r)
        file.close()
        self.fileName = fileName

        return 
    
   
    def show(self, width=800, height=700):
        assert self.fileName is not None, "before calling show(), save timeline using saveStandaloneHTML"
        from IPython.display import IFrame
        return IFrame(src=self.fileName, width=width, height=height)
