
"""
Provides the doFill and checkFill functions:

doFill - Fills in empty areas without balls with walls

checkFill - gets the percentage of the playarea filled with walls


"""

from src.game import game
from src.Wall import Wall 

import sys;


_gamestate = [];

# based on the _unfill_recur function, but no longer relying on recursion
def _unfill_stack(x_, y_, objs):
	stack = [(x_, y_)];
	
	while( True ):
		try:
			x, y = stack.pop();
		except IndexError:
			break;
		
		if(_gamestate[x][y]):
			if(_gamestate[x][y].x == x and _gamestate[x][y].y == y ):
				continue;
		
		try:
			objs.index( (x, y) );
		except ValueError:
			pass;
		else:
			continue;
		
		objs.append( (x, y) );
		
		stack.append((x-1, y  ));
		stack.append((x+1, y  ));
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
	_unfill_recur(x  , y-1, objs);
	_unfill_recur(x  , y+1, objs);



def doFill(canvas, x, y):
	wallPos = [];
	
	# make sure gamestate is cleared
	_gamestate.clear();
	
	# fill wallPos array with every possible spot on playarea
	# while also preparing to fill gamestate array
	for x in range(game.width):
		s = [];
		for y in range(game.height):
			wallPos.append( (x, y) );
			s.append(False);
		_gamestate.append(s);
	
	# populate direct objects first
	for obj in game.objects:
		_x, _y = int(round(obj.x)), int(round(obj.y));
		if( obj.x == _x and obj.y == _y ):
			_gamestate[_x][_y] = obj;
	
	# indirect objects override direct objects
	for obj in game.objects:
		_x, _y = int(round(obj.x)), int(round(obj.y));
		if( obj.x != _x and obj.y != _y ):
			_gamestate[_x][_y] = obj;
	
	# check gameobjects positions
	unfill = [];
	for obj in game.objects:
		_x = round(obj.x); _y = round(obj.y);
		try:
				# delete anything that is anywhere where a static object is
				wallPos.remove( (obj.x, obj.y) );
		except ValueError:
			try:
				wallPos.index( (_x, _y) );
			except ValueError:
				pass;
			else:
				# probably a ball here, mark to unfill
				unfill.append( (_x, _y) );
		else:
				break;
	
	# unfill areas with balls
	# makes sure only empty areas without balls are filled in
	# no longer relying on recursion
	delete = [];
	for pos in unfill:
		_unfill_stack(pos[0], pos[1], delete);
	
	
	# actually delete walls
	for pos in delete:
		try:
			wallPos.remove( (pos[0], pos[1]) );
		except ValueError:
			pass;
	
	# finally, add walls in fill areas
	for pos in wallPos:
		game.objects.append(Wall( canvas, pos[0], pos[1] ));
	
	
	# make sure to clear gamestate
	# so objects can be deleted properly
	_gamestate.clear();



def checkFill():
	total = game.width*game.height;
	filled = 0;
	
	# loop through game objects and check how much of it is filled
	for obj in game.objects:
		if( isinstance(obj, Wall) ):
			filled += 1;
	
	# return integer percentage out of 100
	return (100*filled)//total;
