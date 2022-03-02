
"""
The GrowingWall class

This is the wall while it grows.

"""

from src.game import game
from src.Wall import Wall 
from src.fill import doFill, checkFill

import time;

from tkinter import messagebox;

class GrowingWall:
	recvInteract = False;
	
	def __init__(this, canvas, x, y, xdir, ydir):
		this.x = x; this.y = y;
		this.xdir = xdir; this.ydir = ydir;
		
		this.canvas = canvas;
		this.objects = [];
		this.addObj( SubGrowingWall(this, x, y, xdir, ydir) );
	
	def addObj(this, item):
		this.objects.append(item);
		game.objects.append(item);
	
	def __del__(this):
		for item in this.objects:
			item.destroy();
	
	def interact(this, obj):
		pass;
	
	def update(this):
		for obj in this.objects:
			if( not obj.shouldDestroy ):
				return;
		
		return True; # all objects want destroyed

class SubGrowingWall:
	framesStart = 4;
	recvInteract = True;
	
	def __init__(this, owner, x, y, xdir, ydir):
		this.x = x; this.y = y;
		this.xdir = xdir; this.ydir = ydir;
		
		this.owner = owner;
		
		_x = x*16; _y = y*16;
		this.obj = owner.canvas.create_rectangle(_x, _y, _x+16, _y+16, fill="#f80");
		
		this.frames = this.framesStart;
		this.shouldDestroy = False;
	
	def destroy(this):
		#print("Hmm")
		this.shouldDestroy = True;
		try:
			this.owner.canvas.delete(this.obj);
		except:
			# eat error about destroyed canvas
			pass;
	
	def __del__(this):
		this.destroy();
	
	def interact(this, obj):
		if( this.shouldDestroy ):
			return;
		
		if( this.x == round(obj.x) and this.y == round(obj.y) ):
			if( str(obj).find(".Ball") != -1 ):
				this.destroy();
				#print("Ball",obj, obj.x, this.x);
				for obj2 in this.owner.objects:
					obj2.destroy();
				game.lives -= 1;
				if( game.lives < 0 ):
					messagebox.showwarning("Oh no...", "You've run out of lives!\n\nBack to level 1...");
					game.new(this.owner.canvas);
				else:
					game.updateLabel();
	
	def update(this):
		canvas = this.owner.canvas;
		
		if( this.frames ):
			this.frames -= 1;
		else:
			this.frames = this.framesStart;
			
			newx, newy = this.x+this.xdir, this.y+this.ydir;
			
			# check if there's a wall in our next grow spot
			for obj in game.objects:
				if( newx == round(obj.x) and newy == round(obj.y) ):
					if( isinstance(obj, Wall) ):
						# start time
						start = time.time();
						
						# replace the growingwall segment with real walls
						this.interact(obj);
						for obj2 in this.owner.objects:
							obj2.destroy();
							game.objects.append( Wall(this.owner.canvas, obj2.x, obj2.y) );
						
						# trigger filling
						doFill(this.owner.canvas, obj2.x, obj2.y);
						
						game.fill = checkFill();
						game.updateLabel();
						if( game.fill >= game.fill_required ):
							game.level += 1;
							messagebox.showinfo("Yay!", "You've successfully filled enough of the area!\nNow on to level "+str(game.level)+".");
							canvas.after_idle(game.reset, canvas);
							return True;
						
						# trigger early game cycles to make up time difference
						step = ( time.time() - start ) * 1000;
						steps = int( round( step / 40 ) );
						canvas.after_idle(game.updates, canvas, steps);
						return True;
			
			this.owner.addObj( SubGrowingWall(this.owner, newx, newy, this.xdir, this.ydir) );
			
			# stop the wall from growing more
			this.frames = 1e99;
		
		return this.shouldDestroy;
