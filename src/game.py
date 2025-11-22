
"""
game loop and variables

"""

from src.Wall import Wall 
from src.Ball import Ball 

import time;
import random;

class game:
	width = 32;
	height = 20;
	fill_required = 75;
	
	lives = 0;
	time = 0;
	fill = 0;
	
	level = 0;
	frame = 0;
	lag = False;
	lagC = 0;
	
	# whether the cursor is vertical or horizontal
	# 0 = horizontal, 1 = vertical
	cursorMode = 1;
	
	# if the levels are advancing
	# used to workaround a bug: advancing twice and crashing
	advanceLevel = False;
	
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
		game.updateLabel();
		
		game.advanceLevel = False; # no longer advancing levels
	
	@staticmethod
	def check(canvas):
		if(game.advanceLevel):
			# Do nothing if we're advancing the level soon
			return;
		
		# check lives
		if( game.lives < 0 ):
			from tkinter import messagebox
			messagebox.showwarning("Oh no...", "You've run out of lives!\n\nBack to level 1...");
			game.new(canvas);
		else:
			game.updateLabel();
		
		# check fill
		if( game.fill >= game.fill_required ):
			game.level += 1;
			
			# show dialog
			from tkinter import messagebox
			messagebox.showinfo("Yay!", "You've successfully filled enough of the area!\nNow on to level "+str(game.level)+".");
			
			# reset game properly next cycle
			game.advanceLevel = True;
	
	@staticmethod
	def loop(canvas):
		if( game.advanceLevel ):
			# do game reset at beginning of loop cycle
			game.reset(canvas);
		
		if( game.paused ):
			# wait a short time before next loop cycle,
			# but not too long that there would be a 
			# noticable delay in unpausing
			canvas.after(100, game.loop, canvas);
			return;
		
		start = time.time();
		
		# call game update
		game.update(canvas);
		
		# calculate to keep game speed consistent
		timeout = int(20 - ( 1000 * ( time.time() - start )));
		if( timeout < 1 ):
			timeout = 1;
			# primitive detection for if the game is running slow
			if( not game.lag ):
				game.lagC += 1;
				if( game.lagC > 4 ):
					game.lag = True;
			elif( game.lagC < 10 ):
				game.lagC += 1;
		elif( timeout >= 8 and game.lagC > 0 ):
			game.lagC -= 1;
			if( game.lag and game.lagC == 0 ):
				game.lag = False;
		
		canvas.after(timeout, game.loop, canvas);
	
	@staticmethod
	def update(canvas): # do game cycle
		game.frame += 1;
		# only interact objects every other frame if slowdown is detected
		# somewhat basic but shouldn't affect the game as much as slowdown does
		# at the cost of somewhat jittery movement
		if( not game.lag or game.frame&1 ):
			for obj in game.objects:
				if( obj.recvInteract ):
					for obj2 in game.objects:
						obj.interact(obj2);
		
		destroyed = [];
		
		for obj in game.objects:
			if( obj.update() ):
				destroyed.append(obj);
		
		for d in destroyed:
			try:
				game.objects.remove(d);
			except:
				print(d);
	
	@staticmethod
	def updates(canvas, times): # do game cycle multiple times
		for x in range(times):
			game.update(canvas);


