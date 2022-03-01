
from src.Wall import Wall 
from src.Ball import Ball 

import time;
import random;

"""
game loop and variables

"""

class game:
	width = 32;
	height = 20;
	fill_required = 75;
	
	lives = 0;
	time = 0;
	fill = 0;
	
	level = 0;
	
	# whether the cursor is vertical or horizontal
	cursorMode = 1;
	
	objects = [];
	
	paused = False;
	
	@staticmethod
	def new(canvas): # new game
		game.level = 1;
		game.reset(canvas);
	
	@staticmethod
	def reset(canvas): # reset play for level
		# reset vars
		game.fill = 0;
		game.time = 0;
		
		# set to correct values for level
		game.balls = game.level + 1;
		game.lives = game.level;
		
		# reset objects array
		game.objects.clear();
		
		# balls to random positions
		for i in range(game.balls):
			game.objects.append(Ball( canvas, random.randint(2, game.width-3), random.randint(2, game.height-3) ));
		
		# bordering walls according to width/height
		for x in range(game.width):
			game.objects.append(Wall( canvas, x, 0             ));
			game.objects.append(Wall( canvas, x, game.height-1 ));
		for y in range(game.height):
			game.objects.append(Wall( canvas, 0,            y ));
			game.objects.append(Wall( canvas, game.width-1, y ));
		
		canvas.config(width=game.width*16, height=game.height*16)
	
	@staticmethod
	def loop(canvas):
		if( game.paused ):
			canvas.after(100, game.loop, canvas);
			return;
		
		start = time.time();
		
		game.update(canvas);
		
		timeout = int(20 - ( 1000 * ( time.time() - start )));
		if( timeout < 1 ):
			timeout = 1;
		
		canvas.after(timeout, game.loop, canvas);
	
	@staticmethod
	def update(canvas):
		for obj in game.objects:
			if( obj.recvInteract ):
				for obj2 in game.objects:
					obj.interact(obj2);
		
		destroyed = [];
		
		for obj in game.objects:
			if( obj.update() ):
				destroyed.append(obj);
		
		for d in destroyed:
			game.objects.remove(d);
	
	@staticmethod
	def updates(canvas, times):
		for x in range(times):
			game.update(canvas);


