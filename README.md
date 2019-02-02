# pylcg

#### A new (early 2019) python 3 replacement for AAVSO's venerable but doomed Light Curve Generator "LCG V1".

_Currently: version 1.00, February 2, 2019_  :: INITIAL RELEASE

Mid-2018, the [AAVSO](http://www.aavso.org) (American Association of Variable Star Observers) decided that it must retire its original Light Curve Generator [LCG V1](https://www.aavso.org/lcg) _[NB: this link will eventually fail]_. 
For years it has been AAVSO's main web service for plotting variable-star "light curves". 
But LCG V1 will probably disappear sometime in 2019. 
While AAVSO's newer light-curve plotting tool [LCG V2](https://www.aavso.org/LCGv2/) is indeed in place, a number of high-volume CCD variable-star observers (including the one writing this) want speed and a more straightforward visual interface.    

So I, Eric Dose, wrote this pylcg software as a lightweight, streamlined, but full-featured light curve plotting tool. Unlike AAVSO's LCG V1 and LCG V2, which are run on AAVSO's servers as web services, pylcg is offered as a Windows executable to run on one's own PC.

>A pylcg [screenshot](https://github.com/edose/pylcg/blob/master/screenshot_pylcg_03beta.png) is available here on this repository. Users of LCG V1 will get it right away and won't need much help.

### Installing pylcg 1.00

_Pylcg has been tested on Windows 7 and 10, presumed to work on Windows 8 as well._

1. Download the zip file (instructions on AAVSO forum). Unzip that file to wherever you'd like (under Program Files or Program File (x86) not recommended.)
2. In Windows Explorer, double-click on the app.exe file to run pylcg and make sure it opens. If you like pylcg, you'll probably want to make a shortcut to app.exe.
3. Enjoy! 

### How to use pylcg 1.00

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
* **Bands**: Choose U, B, V, R, I, Vis., or TG directly. 
   Check 'other' to include all other bands not listed.
   Check 'ALL' to include all bands allowed in the AAVSO database.  When you uncheck 'other' or 'ALL', the other selections are kept and used.
* **Grid**: select to show a grid over the plot, deselect to remove.
* **Error bars**: select to show error bars on each point, as submitted by the observer.
* **plot in JD**: select for Julian Data on the horizontal axis, deselect for calendar dates.
* **less-thans**: select to show observations marked by the observer as a less-than magnitude, deselect to hide them.
* **Observer code** settings: You may enter an AAVSO observer code (usually your own) in the box.
   When you select "Highlight", pylcg will highlight each point submitted by that observer.
   When you select "Plot only", pylcg will plot only the points from that observer (subject to the Bands selections).

**Buttons**: Each buttons at bottom right triggers an action you might find useful:
* "Preferences..." is disabled. 
* "VSX" launches your browser in the VSX Search window for the current target star.
* "Observations" launches your browser in the WebObs window populated with the target star's observations.
* "List Observers" shows a pop-up box with a summary of the observers that submitted observations for the current target star in the current date range (enhanced in v 1.00).

**Also note**:
* Check marks shown on the right of the Start, End, and Days entry boxes mean that pylcg understands what's in the box. An X mark means it doesn't understand, and a dash means the entry box appears to be empty. 
     And when the check mark is highlighted green, that means that data has been loaded and plotted using those values.
* Plots are resizeable. Drag and drop the (say) right bottom corner of the whole window to resize the plot. 
     You can shrink it small enough to fit easily in a laptop screen, or make it as large as you can stand.
     This manual resizing is *not* stored in Preferences.
     But you can use the new (v 1.00) Preferences menu item to set launch-time window size to Smaller or Larger.
* Zoom and pan now work! Use the magnifying glass and 4-arrow buttons in the toolbar at bottom.
* Save a plot using the disk button in the toolbar.
* When you change settings, any zooming gets undone. 
     This won't matter for most users most of the time, 
     but it appears to be a matplotlib limitation and is unlikely to be improved.

### Changes in release Version 1.00 (vs 0.31 Beta):
* User can set plot window size to Larger or Smaller. 
   Make your choice in the top menu bar under Preferences. You'll have to restart pylcg for this to take effect (matplotlib limitation). 
   Typically, you'll use Larger if you're working on either a desktop monitor or a high-resolution laptop screen when you've turned off Win 10 "High DPI" options.
   Typically, you'll use Smaller if you're working on a standard laptop screen.
* List Observers is greatly enhanced. 
   For each observer having submitted data in the time span, pylcg now shows the number of observations, 
      the number of observations by band, and the days (from present) since that observer's most recent
      observation of the currently plotted target (within the time range selected).
   When a column header is clicked, the table is instantly sorted on that column's contents. 
   To reverse the sort order, simply click it again.
* Plots may have observations limited to those of only one observer (check "Plot only" when an observer code is
   entered in the box).
* Plots in JD with small time ranges now plot as a base JD + offset for legibility.
* X-axis formatting in calendar-date mode is improved.
* All option combinations at right now play nicely together in any combination.
* Various speed enhancements. Most operations are essentially instantaneous after the data has been downloaded from AAVSO.
* Retrieval from AAVSO's database are slightly faster from an improved access method (thanks, George and Cliff!)

### Changes in Version 0.31 (vs 0.3 Beta):
* [made obsolete by v 1.00] Size of initial window is smaller, to accommodate Windows 10's weird rescaling of GUIs on laptops. Vertical size is now 772 pixels; I don't think I can make it smaller than this. Don't forget that you can always size the plot larger by dragging a window corner. Initial window size will be a persistent Preference (small-for-laptop vs. normal-for-desktop) in release 1.0.  

### Changes in Version 0.3 (vs 0.2 Beta):
* Dates (horizontal axis) may be in Julian date or calendar date. (This will be improved in release 1.0.)
* Observer codes may be highlighted and/or may limit the set of points plotted.
* List Observers button gives a summary table of the observers.
* The cursor's current position in JD, calendar date, and magnitude is now presented instantaneously just to the right of the toolbar buttons, at plot bottom.
* A considerable number of other small improvements in speed and stability, especially in parsing downloaded data (thanks, George!). 

### Versions after 1.00:
pylcg now does everything I wanted it to do, and I know of no bugs in it (and it's been hammered on pretty hard).

I'll certainly fix meaningful bugs brought to my attention, and will publish new minor revisions if needed. 

But short of that: I am making major observatory changes early 2019, 
so I do not expect to make major revisions before 3rd quarter 2019 at the earliest.

Even so...

### What might \*you\* want pylcg's future to be?
 
 _Please let me know:_
* on the AAVSO Forum (best for AAVSO-public comments), or
* via AAVSO private message (for comments you'd prefer be held in confidence).

- - -

>Thank you
>
>Eric Dose\
>Albuquerque, New Mexico, USA\
>   _AAVSO observer DERA_
