#!/usr/bin/python3

# main entry point for application...

from src.mainwindow import * 
from src.game import game

def main():
	mainwin = Main();
	
	game.new(mainwin.canvas);
	game.loop(mainwin.canvas);
	
	mainwin.mainloop();

if(__name__ == "__main__"):
	main();
