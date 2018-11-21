# pylcg

#### A new (late 2018) python 3 replacement for AAVSO's venerable but doomed Light Curve Generator "LCG V1".

_Currently: version 0.31 Beta, November 21, 2018_

Mid-2018, the [AAVSO](http://www.aavso.org) (American Association of Variable Star Observers) decided that it must retire its original Light Curve Generator [LCG V1](https://www.aavso.org/lcg). For years it has been AAVSO's main web service for plotting variable-star "light curves". But LCG V1 will probably disappear late 2018. 
While AAVSO's newer light-curve plotting tool [LCG V2](https://www.aavso.org/LCGv2/) is indeed in place, a number of high-volume CCD variable-star observers (including the one writing this) want speed and a more straightforward visual interface.    

So, this author wrote this pylcg software as a lightweight, streamlined, but full-featured light curve plotting tool. Unlike AAVSO's LCG V1 and LCG V2, which are run on AAVSO's servers as web services, pylcg is offered as a Windows executable to run on one's own PC.

>A pylcg [screenshot](https://github.com/edose/pylcg/blob/master/screenshot_pylcg_03beta.png) is available here on this repository. Users of LCG V1 will get it right away and won't need much help.

### Installing pylcg version 0.31 BETA

_Pylcg has been tested on Windows 7 and 10, presumed to work on Windown 8 as well._

1. Download the zip file (instructions on AAVSO forum). Unzip that file to wherever you'd like (under Program Files or Program File (x86) not recommended.)
2. In Windows Explorer, double-click on the app.exe file to run pylcg and make sure it opens. For repeated use, you'll probably want to make a shortcut to this file.
3. Enjoy! 

### How to use pylcg version 0.31 BETA

To plot one target star at a time:
1. Start pylcg (double-click on app.exe, or make a shortcut for it).
2. In the Star box at right, enter a target name, as any identifier that AAVSO's AID database can recognize, e.g., UZ Cam.
3. Optionally enter a End JD or calendar date. Pylcg launches with the JD (Julian date) of right now (the usual case).
4. Enter either a number of days to plot (the usual case), or a beginning JD or calendar date.
5. Ensure the bands you want are selected.
6. Click "Plot this star". Pylcg goes out to AAVSO, downloads the needed data, plots it.

To plot all targets in a AAVSO Enhanced (CCD) or Visual Upload file (very useful to review data _in context_ that you've just submitted):
1. In the Star box at right, click "From upload file..." and select the upload file.
2. Enter date range and select/deselect bands just as in steps 3-5 above.
3. The first target is downloaded and plotted immediately. Use the Prev and Next buttons to click through all the targets in the file, in order. 
4. You can enter a target name at any time, and the name will be submitted in the target list as though it had been part of your upload file.

**Settings**: You can change any settings at any time. The plot updates, and the settings carry over to the next plots.
* Bands.
* Grid: select to show a grid over the plot.
* Error bars: select to show error bars on each point, as submitted by the observer.
* plot in JD: select for Julian Data on the horizontal axis, deselect for calendar dates (will be prettified in next pylcg release).
* less-thans: select to show observations marked by the observer as a less-than magnitude, deselect to hide them.
* Observer code box: When you've entered an AAVSO observer code (usually your own) in this box, selecting "Highlight" will highlight each point submitted by that observer, and "Plot only" will plot only the points from that observer (subject to the Bands selections, mind you).

**Buttons**: Each buttons at bottom right triggers an action you might find useful:
* "Preferences..." is disabled until release 1.0.
* "VSX" launches your browser in the VSX Search window for the current target star.
* "List Observers" shows a pop-up box with a summary of the observers that submitted observations for the current target star in the current date range (is not limited by Bands; let me know if you think they should be).
* "Observations" launches your browser in the WebObs window populated with the target star's observations.

**Also note**:
* Check marks on the right of the Start, End, and Days entry boxes mean that pylcg understands what's in the box. An X mark means it doesn't understand, and a dash means the entry box appears to be empty. When the check mark is highlighted green, that means that data has been loaded and plotted using those values.
* Plots are resizeable. Drag and drop the (say) right bottom corner of the whole window to resize the plot. You can shrink it small enough to fit easily in a laptop screen, or make it as large as you can stand (but note: the axes and data points don't grow with the screen).
* Zoom and pan now work! Use the magnifying glass and 4-arrow buttons in the toolbar at bottom.
* Save a plot using the disk button in the toolbar.
* When you change settings, any zooming gets undone. This won't matter for most users most of the time, but retaining zoom/pan on settings change will require some research and considerable rewriting, so will wait until 2019.

### Changes in Version 0.31 (vs 0.3 Beta):
* Size of initial window is smaller, to accommodate Windows 10's weird rescaling of GUIs on laptops. Vertical size is now 772 pixels; I don't think I can make it smaller than this. Don't forget that you can always size the plot larger by dragging a window corner. Initial window size will be a persistent Preference (small-for-laptop vs. normal-for-desktop) in release 1.0.  

### Changes in Version 0.3 (vs 0.2 Beta):
* Dates (horizontal axis) may be in Julian date or calendar date. (This will be improved in release 1.0.)
* Observer codes may be highlighted and/or may limit the set of points plotted.
* List Observers button gives a summary table of the observers.
* The cursor's current position in JD, calendar date, and magnitude is now presented instantaneously just to the right of the toolbar buttons, at plot bottom.
* A considerable number of other small improvements in speed and stability, especially in parsing downloaded data (thanks, George!). 

### Expected in first full release 1.0 (mid-January 2019):
* Preferences will automatically be saved from session to session.
* Help tooltips when hovering over most buttons and entry fields.
* Improvements in calendar date formatting.
* Note: official current list of pylcg Issues is maintained at https://github.com/edose/pylcg/issues .
* (uncertain for 1.0) Settings changes will not cause full zoom out, as currently the case.

### Beyond that ... What do \*you\* want pylcg's future to be?
 
 _Please let me know:_
* on the AAVSO Forum (best for AAVSO-public comments), or
* via AAVSO private message (for comments you'd prefer be held in confidence).

- - -

>Thank you
>
>Eric Dose\
>Albuquerque, New Mexico, USA\
>   _AAVSO observer DERA_
