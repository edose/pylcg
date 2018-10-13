# pylcg

#### A new (August-September 2018) python 3 replacement for AAVSO's venerable but doomed Light Curve Generator "LCG V1".

_Currently: version 0.2 Beta, October 12, 2018_

Mid-2018, the [AAVSO](http://www.aavso.org) (American Association of Variable Star Observers) decided that it must retire its original Light Curve Generator [LCG V1](https://www.aavso.org/lcg). For years it has been AAVSO's main web service for plotting variable-star "light curves". But LCG V1 will probably disappear late 2018. 
While AAVSO's newer light-curve plotting tool [LCG V2](https://www.aavso.org/LCGv2/) is in place, a number of high-volume CCD variable-star observers (including the one writing this) do not consider LCG V2 a viable replacement.    

So, in short, this author wrote this pylcg software as a lightweight, streamlined, but full-featured light curve plotting tool. Unlike AAVSO's LCG V1 and LCG V2, which are run on AAVSO's servers as web services, pylcg is offered as a Windows executable to run on one's own PC.

>A pylcg [screenshot](https://github.com/edose/pylcg/blob/master/screenshot_pylcg.png) is available here on this repository. Users of LCG V1 will get it right away and won't need much help.

### How to use pylcg version 0.2 BETA

For now, pylcg operates one plot at a time, just as web-based LCG does.

1. Enter the star ID. Or import star IDs from an upload file.
2. Define the time span by entering any 2 of these 3: Number of days, JD Start, JD End. The most common 2 entries by far are Number of days and JD End, with JD End as "now". If you press the "JD End = Now" button it will populate JD End with the JD of your PC's clock at that moment.
3. Make sure the photometric bands you want are selected. Check grid and errorbars if you want them (normally on).
4. Click Plot this Star under the star name.

To plot more stars with the same settings, just enter the star ID and click Plot this Star. Just about like web-based LCG V1 (RIP).

To see the same plot but with different bands, just select or deselect any bands, and the plot updates immediately (the legend at upper left, too).

Same with grid and error bars: change the check boxes and it updates immediately.

### Changes in Version 0.2 Beta (vs 0.1 Beta):

1. Star names may be imported from an upload file! The order within the file is retained, and duplicates are removed. This has been tested for both Extended (CCD) Format and Visual Format upload files. 
2. The Prev and Next buttons plot the previous or next star. This works whether star names were typed in or imported from an upload file. 
3. Calendar dates or Julian Dates may be entered in the Start and End boxes, in any combination. Plots will still be in Julian Date (see above). Entered dates may be in US format (mm/dd/yyyy) or international format (dd.mm.yyyy or dd-mm-yyyy).
4. Check marks on the right of the Start, End, and Days entry boxes mean that pylcg understands what's in the box. An X mark means it doesn't understand, and a dash means the entry box appears to be entry. When the check mark is highlighted green, that means that data has been loaded and plotted using those values. 
5. Less-than observations may be toggled on or off.
6. Cache may be cleared by user in the unlikely event something goes wrong with a download.

**Please note: Plotting with calendar dates on the x-axis did not make it into 0.2 Beta.** Sorry. A really difficult bug in the toolbar function (from TKinter and matplotlib) prevents zooming back correctly after axis units have changed, for example when changing from plotting in Julian Date to plotting in calendar dates. There is not enough time before the sun goes red giant to hack this stock toolbar, and then it would be unstable to later python versions anyway. Several days of research into this persuades me that it just fails to provide this functionality. 

So for an upcoming version, I will code my own zoom and cache functionality, then we can plot in JD, calendar dates, or any other time span, and with proper formatting. But not yet--it's not worth delaying 0.2 Beta any farther. I plan for Version 0.3 Beta (before the AAVSO November meeting) to have a complete rewrite of the zoom function. That will solve a lot of problems.

### Notable features retained from 0.1 Beta:

Plots are resizeable. Drag and drop the (say) right bottom corner of the whole window to resize the plot. You can shrink it small enough to fit easily in a laptop screen, or make it as large as you can stand (but note: the axes and data points don't grow with the screen).

To see the **_VSX record_** for the current star, click the "VSX" button. A populated VSX search page will appear in your browser.

To see the **_WebObs observations_** for this star, click the "Observations" button.

The _**Toolbar**_ (at lower left from the plot) has seven buttons. Let me cover them in a special order so you'll understand right away how they work together:
* The magnifying glass (5th button) is ZOOM, the button most often used. Click the zoom icon, then just drag a rectangle inside the plot, and the rectangle will zoom to full plot size. You can repeat this zooming as many times as you like.
* The left arrow (2nd button) goes back one zoom level. So never fear a zoom--if you don't like it, just hit the left arrow.
* The right arrow (3rd button) goes forward one zoom level if any.
* The home icon (1st button) resets the plot to your original scales.
* The 4-arrow icon (4th button) allows you to drag (pan) your zoomed plot in any direction.
* The settings icon (6th button) is rarely used except perhaps to tweak plots for publication.
* The disk icon (last button) allows you to save the plot as an image file (PNG format is default and recommended).

_**Data cacheing**_: Pylcg does download data from AAVSO for every plot, but it saves that data in a local cache. So it will not reload on zooming or on the 2nd or 100th time you plot the same star with the same time range, so long as you keep pylcg open. Good for the user, good for AAVSO.

### What doesn't work yet? And what does the future hold?

_NB: All issues, both pending and closed, are available at github.com/edose/pylcg/issues._

* Preferences are limited; more preferences and persistence are planned for 0.3 Beta. 

* When changing settings (e.g, bands, grid), a zoomed-in plot will snap back to full time span. This "feature" of the toolbar will disappear during upcoming rewrite of the zoom facility (0.3 Beta). 

* Plots with Calendar dates on X-axis (0.3 Beta).

* Status label to inform user while downloading observations, etc. (0.3 Beta)

* "List Observers" facility (for observations currently plotted). Easy. (0.3 Beta)

* Maybe: menu bar enhancements. Now limited to Exit, Browse Repo, and About menu items do work.

* Maybe: Highlight points from observer(s). _(Do people really use this?)_

* Maybe: various annotations right on the plot. Optional? Suggestions?

### Beyond that ... What do \*you\* want its future to be?
 
 _Please let me know:_
* on the AAVSO Forum (best for AAVSO-public comments), or
* via AAVSO private message (for comments you'd prefer be held in confidence).

- - -

>Thank you
>
>Eric Dose\
>Albuquerque, New Mexico, USA\
>   _AAVSO observer DERA_
