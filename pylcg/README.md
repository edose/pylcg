#pylcg

#####A new (August-September 2018) python 3 replacement for AAVSO's venerable but doomed Light Curve Generator "LCG V1".

Mid-2018, the [AAVSO](http://www.aavso.org) (American Association of Variable Star Observers) decided that it must retire its original Light Curve Generator [LCG V1](https://www.aavso.org/lcg). For years it has been AAVSO's main web service for plotting variable-star "light curves". But LCG V1 will probably disappear late 2018.
 
While AAVSO's newer light-curve plotting tool [LCG V2](https://www.aavso.org/LCGv2/) is in place, a number of high-volume CCD variable-star observers (including the one writing this) do not consider LCG V2 a viable replacement. Their reasons can be readily found on AAVSO's Forums, but LCG V2's clumsy interface, tectonic load rates, and its (um) aesthetic sense seem to be the most cited causes for rejection.    

So, in short, this author wrote this pylcg software as a lightweight, streamlined, but full-featured light curve plotting tool. By contrast to AAVSO's LCG V1 and LCG V2, which are run on AAVSO's servers as web services, pylcg is offered as a Windows executable to run on one's own PC.

>A pylcg 0.1 [screenshot](https://github.com/edose/pylcg/pylcg/screenshot_pylcg.png) is available here on this repository. Users of LCG V1 will get it right away and won't need much help.

###How to use pylcg version 0.1

For now, pylcg operates one plot at a time, just as web-based LCG does.

1. Enter the star ID. 
2. Enter any 2 of the 3 time-span items: Number of days, JD Start, end JD End. The most common 2 entries by far are Number of days and JD End, with JD End as "now". If you press the "JD End = Now" button it will populate JD End with the JD of your PC's clock at that moment.
3. Make sure the photometric bands you want are selected. Check grid and errorbars if you want them (normally on).
4. Click Plot this Star under the star name.

To plot more stars with the same settings, just enter the star ID and click Plot this Star. Just about like web-based LCG V1 (RIP).

To see the same plot but with different bands, just select or deselect any bands, and the plot updates immediately (the legend at upper left, too).

Same with grid and error bars: change the check boxes and it updates immediately.

###Additional Features

The whole pylcg window is resizeable! Drag and drop the (say) right bottom corner of the whole window to resize the plot. You can shrink it small enough to fit easily in a laptop screen, or make it as large as you can stand (but note: the axes and data points don't grow with the screen).

To see the **_VSX record_** for the current star, click the "VSX" button. A populated VSX search page will appear in your browser.

To see the **_WebObs observations_** for this star, click the "Observations" button.

The _**Toolbar**_ (at lower left from the plot) has seven buttons. Let me cover them in a special order so you'll understand right away how they work together:
* The magnifying glass (5th button) is ZOOM, the button most often used. Click the zoom icon then just drag a rectangle inside the plot, and the rectangle will zoom to full plot size. You can repeat this zooming as many times as you like.
* The left arrow (2nd button) goes back one zoom level. So never fear a zoom--if you don't like it, just hit the left arrow.
* The right arrow (3rd button) goes forward one zoom level if any.
* The home icon (1st button) resets the plot to your original scales.
* The 4-arrow icon (4th button) allows you to drag (pan) your zoomed plot in any direction.
* The settings icon (6th button) is rarely used except perhaps to tweak plots for publication.
* The disk icon (last button) allows you to save the plot as an image file (PNG format is default and recommended).

_**Data cacheing**_: Pylcg 0.1 does downloads raw data from AAVSO for every plot, but it saves that data in a local cache. It will not reload the 2nd or 100th time you plot the same star with the same time range, so long as you keep pylcg open.

###What doesn't work yet?

Preferences are limited to persistence of time-span Number of Days and band selections.

The menu bar doesn't have much, although the Exit, Browse Repo, and About menu items do work.

### What does the future hold?

* First and foremost: facility to read an AAVSO Upload file of new data (Enhanced/CCD format) and make all star IDs available to the "Prev" and "Next" buttons (under "Plot this Star"; deactivated for now). That is: one-click per target to review all the data you just submitted, right in WebObs context. Ah. Nirvana.

* Highlight points from observer(s). _(Do people really use this?)_

* Preferences enhancements.

* "List Observers" facility (for observations currently plotted).

* Possibly: various annotations right on the plot. Optional? Suggestions?

>Beyond that ... _What do **you** want its future to be?_
 
 **_Please let me know:_**
* on the AAVSO Forum (best for AAVSO-public comments), or
* via AAVSO private message (for comments you'd prefer be held in confidence).

- - -

>Thank you\
>Eric Dose\
>Albuquerque New Mexico, USA\
>   AAVSO observer DERA
