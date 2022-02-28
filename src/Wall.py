
"""
The Wall class

The balls bounce off these.

"""


import tkinter as tk

class Wall:
	def __init__(this, canvas, x, y):
		this.x = x; this.y = y;
		
		# don't receive objects to interact with
		this.recvInteract = False;
		
		# create the wall on the playarea
		_x = x*16; _y = y*16;
		this.obj = canvas.create_rectangle(_x, _y, _x+16, _y+16, fill="#ccc");
		
		this._canvas = canvas;
	
	def __del__(this):
		this._canvas.delete(this.obj);
	
	def interact(this, obj):
		pass;
	
	def update(this):
		pass;

