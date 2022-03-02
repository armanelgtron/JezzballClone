
"""
The Ball class.



"""

import tkinter as tk

import random;

class Ball:
	def __init__(this, canvas, x=0, y=0):
		this.x = x; this.y = y;
		
		s=[-1,1];
		random.shuffle(s); this.xdir = s[0]*0.175;
		random.shuffle(s); this.ydir = s[0]*0.175;
		
		this._canvas = canvas;
		this.obj = canvas.create_oval(0, 0, 16, 16, fill="#fff");
		this._canvas.move(this.obj, this.x*16, this.y*16)
		
		# the object should receive objects to interact with
		this.recvInteract = True;
	
	def __del__(this):
		try:
			this._canvas.delete(this.obj);
		except:
			# eat error about destroyed canvas
			pass;
	
	def interact(this, obj):
		is_wall = str(obj).find("Wall");
		is_growingwall = str(obj).find("GrowingWall") != -1;
		if( is_wall ):
			# loop through 
			for i in range(4):
				# get the current collision offset check
				offset_x = ((-0.5, 0, 0.5, 0)[i]);
				offset_y = (( 0,-0.5, 0, 0.5)[i]);
				
				check_x = round(this.x+offset_x);
				check_y = round(this.y+offset_y);
				if( check_x == obj.x and check_y == obj.y ):
					if(is_growingwall):
						break;
					if(offset_x): # if the ball hit the left or right sides of the wall
						# flip the x direction
						if(offset_x > 0):
							this.xdir = -abs(this.xdir);
						else:
							this.xdir = abs(this.xdir);
					if(offset_y): # if the ball bounced from top or bottom of the wall
						# flip the y direction
						if(offset_y > 0):
							this.ydir = -abs(this.ydir);
						else:
							this.ydir = abs(this.ydir);
	
	def update(this):
		this.x += this.xdir;
		this.y += this.ydir;
		
		x = this.x*16; y = this.y*16;
		
		this._canvas.move(this.obj, this.xdir*16, this.ydir*16);

