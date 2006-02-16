# Orca
#
# Copyright 2006 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import gtk

class BrlMon(gtk.Window):

    """Displays a GUI braille monitor that mirrors what is being
    shown on the braille display.  This currently needs a lot of
    work, but it is a start.  TODO's include doing a better job of
    docking it at the top of the display (e.g., make all other
    windows move out from underneath it), doing better highlighting of
    the cursor cell, allowing the font to be set, and perhaps allowing
    clicks to simulate cursor routing keys."""

    def __init__(self, numCells=32, cellWidth=25, cellHeight=50):
	"""Create a new BrlMon.

	Arguments:
	- numCells: how many braille cells to make
	- cellWidth: width of each cell in pixels
 	- cellHeight: height of each cell in pixels
        """

	gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
	self.set_title("Braille Monitor")
	self.set_default_size(cellWidth * numCells, cellHeight)
	hbox = gtk.HBox(True)
	self.add(hbox)
	self.cellFrames = []
	self.cellLabels = []
	for i in range(0, numCells):
	    frame = gtk.Frame()
	    frame.set_shadow_type(gtk.SHADOW_OUT)
	    label = gtk.Label(" ")
	    label.set_use_markup(True)
	    frame.add(label)
	    hbox.add(frame)
	    self.cellFrames.append(frame)
	    self.cellLabels.append(label)

	# This prevents it from getting focus.
	#
	self.set_property("accept-focus", False)
	self.connect_after("realize", self.onRealize)

    def onRealize(self, object):
	"""Tell the window to be a dock, which I thinks means to
	attempt to glue it somewhere on the display.
	"""

	screen_width = gtk.gdk.screen_width()
	[window_width, window_height] = self.window.get_size()
	if window_width < screen_width:
	    x = (screen_width - window_width) / 2
	else:
	    x = 0

	self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
	self.move(x, 0)

    def writeText(self, cursorCell, string):
        """Display the given text and highlight the given
        cursor cell.  A cursorCell of 0 means no cell has
	the cursor.

	Arguments:
	- cursorCell: 1-based index of cell with cursor
	- string: len must be <= num cells.
	"""

	# Fill out the cells from the string.
	#
	for i in range(0, len(string)):
	    if i == (cursorCell - 1):
	        if string[i] == " ":
	  	    self.cellLabels[i].set_markup(
		        "<span"\
		        + " background='black'" \
		        + " weight='ultrabold'" \
	                + " style='italic'"\
	                + " size='xx-large'"\
		        + ">%s</span>" \
		        % string[i])
		else:
	  	    self.cellLabels[i].set_markup(
		        "<span"\
		        + " background='white'" \
		        + " weight='ultrabold'" \
	                + " style='italic'"\
	                + " size='xx-large'"\
		        + ">%s</span>" \
		        % string[i])
	 	self.cellFrames[i].set_shadow_type(
		    gtk.SHADOW_IN)
	    else:
	  	self.cellLabels[i].set_markup(
		    "<span"\
	            + " size='xx-large'"\
		    + ">%s</span>" \
		    % string[i])
	 	self.cellFrames[i].set_shadow_type(
		    gtk.SHADOW_OUT)

	# Pad the rest
	#
	for i in range(len(string), len(self.cellFrames)):
	    self.cellLabels[i].set_text(" ")
 	    self.cellFrames[i].set_shadow_type(
		gtk.SHADOW_OUT)
