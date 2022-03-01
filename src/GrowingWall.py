
"""
The GrowingWall class

This is the wall while it grows.

"""

from src.game import game
from src.Wall import Wall 

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
	framesStart = 8;
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
				print("Ball",obj, obj.x, this.x);
				for obj2 in this.owner.objects:
					obj2.destroy();
	
	def update(this):
		canvas = this.owner.canvas;
		
		if( this.frames ):
			this.frames -= 1;
		else:
			this.frames = this.framesStart;
			
			newx, newy = this.x+this.xdir, this.y+this.ydir;
			
			for obj in game.objects:
				if( newx == round(obj.x) and newy == round(obj.y) ):
					if( isinstance(obj, Wall) ):
						this.interact(obj);
						for obj2 in this.owner.objects:
							obj2.destroy();
							game.objects.append( Wall(this.owner.canvas, obj2.x, obj2.y) );
						return True;
			this.owner.addObj( SubGrowingWall(this.owner, newx, newy, this.xdir, this.ydir) );
			
			# stop the wall from growing more
			this.frames = 1e99;
		
		return this.shouldDestroy;