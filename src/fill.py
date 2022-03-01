
"""

Provides the doFill function

Fills in empty areas without balls with walls

"""

from src.game import game
from src.Wall import Wall 

import sys;

# recursive function for un-filling in areas
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
	
	# save and raise recursion limit...
	limit = sys.getrecursionlimit();
	sys.setrecursionlimit(int(1e6));
	
	# recursively unfill areas with ball
	# makes sure only empty areas without balls are filled in
	delete = [];
	for pos in unfill:
		_unfill_recur(pos[0], pos[1], delete);
	
	# restore original recursion limit
	sys.setrecursionlimit(limit);
	
	# actually delete walls
	for pos in delete:
		for pos2 in wallPos:
			if( pos[0] == pos2[0] and pos[1] == pos2[1] ):
				wallPos.remove(pos2);
				break;
	
	# finally, add walls in fill areas
	for pos in wallPos:
		game.objects.append(Wall( canvas, pos[0], pos[1] ));
