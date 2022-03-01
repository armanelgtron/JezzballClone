
from src.Wall import Wall 
from src.Ball import Ball 

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
		canvas.after(20, game.loop, canvas);
		
		if( game.paused ):
			return;
		
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


