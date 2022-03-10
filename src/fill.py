
"""
Provides the doFill and checkFill functions:

doFill - Fills in empty areas without balls with walls

checkFill - gets the percentage of the playarea filled with walls


"""

from src.game import game
from src.Wall import Wall 

import sys;


# based on the _unfill_recur function, but no longer relying on recursion
def _unfill_stack(x_, y_, objs):
	stack = [(x_, y_)];
	
	while( True ):
		try:
			x, y = stack.pop();
		except IndexError:
			break;
		
		_continue = False;
		for obj in game.objects:
			if( obj.x == x and obj.y == y ):
				_continue = True;
				break;
		
		for pos in objs:
			if( pos[0] == x and pos[1] == y ):
				_continue = True;
				break;
		
		if(_continue): continue;
		
		objs.append( (x, y) );
		
		stack.append((x-1, y  ));
		stack.append((x+1, y  ));
		stack.append((x-1, y-1));
		stack.append((x-1, y+1));
		stack.append((x+1, y-1));
		stack.append((x+1, y+1));
		stack.append((x  , y-1));
		stack.append((x  , y+1));


# recursive function for un-filling in areas
# no longer needed, but left here just in case / as reference
def _unfill_recur(x, y, objs):
	for obj in game.objects:
		if( obj.x == x and obj.y == y ):
			return;
	
	for pos in objs:
		if( pos[0] == x and pos[1] == y ):
			return;
	
	objs.append( (x, y) );
	
	_unfill_recur(x-1, y  , objs);
	_unfill_recur(x+1, y  , objs);
	_unfill_recur(x-1, y-1, objs);
	_unfill_recur(x-1, y+1, objs);
	_unfill_recur(x+1, y-1, objs);
	_unfill_recur(x+1, y+1, objs);
	_unfill_recur(x  , y-1, objs);
	_unfill_recur(x  , y+1, objs);



def doFill(canvas, x, y):
	wallPos = [];
	
	# fill array with every possible spot on playarea
	for x in range(game.width):
		for y in range(game.height):
			wallPos.append( (x, y) );
	
	# check gameobjects positions
	unfill = [];
	for obj in game.objects:
		_x = round(obj.x); _y = round(obj.y);
		for pos in wallPos:
			if( pos[0] == obj.x and pos[1] == obj.y ):
				# delete anything that is anywhere where a static object is
				wallPos.remove(pos);
				break;
			if( pos[0] == _x and pos[1] == _y ):
				# probably a ball here, mark to unfill
				unfill.append( (_x, _y) );
	
	# unfill areas with balls
	# makes sure only empty areas without balls are filled in
	# no longer relying on recursion
	delete = [];
	for pos in unfill:
		_unfill_stack(pos[0], pos[1], delete);
	
	
	# actually delete walls
	for pos in delete:
		for pos2 in wallPos:
			if( pos[0] == pos2[0] and pos[1] == pos2[1] ):
				wallPos.remove(pos2);
				break;
	
	# finally, add walls in fill areas
	for pos in wallPos:
		game.objects.append(Wall( canvas, pos[0], pos[1] ));



def checkFill():
	total = game.width*game.height;
	filled = 0;
	
	# loop through game objects and check how much of it is filled
	for obj in game.objects:
		if( isinstance(obj, Wall) ):
			filled += 1;
	
	# return integer percentage out of 100
	return (100*filled)//total;
