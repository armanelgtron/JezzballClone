
"""
Main - mainwindow

The main window, with all of the UI elements like menus and toolbars

"""

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox

from src.game import game
from src.GrowingWall import *

from src.configurewindow import *

class Main(tk.Tk):
	
	# empty container class
	class menus:
		pass;
	
	def __init__(this):
		tk.Tk.__init__(this);
		
		this.style = ttk.Style();
		if( this.style.theme_use() == "default" ):
			this.style.theme_use("clam");
		
		this.title("Jezzball Clone");
		
		# menubar
		this.menu = tk.Menu(this);
		
		# file menu
		this.menus.file = tk.Menu(this.menu, tearoff=False);
		this.menus.file.add_command(label="New Game", command=lambda:game.new(this.canvas));
		this.menus.file.add_command(label="Quit", command=this.quit);
		this.menu.add_cascade(label="File", menu=this.menus.file);
		
		# configure menu
		this.menus.settings = tk.Menu(this.menu, tearoff=False);
		this.menus.settings.add_command(label="Configure", command=this.openConfiguration);
		this.menu.add_cascade(label="Settings", menu=this.menus.settings);
		
		# help menu
		this.menus.help = tk.Menu(this.menu, tearoff=False);
		this.menus.help.add_command(label="About");
		this.menu.add_cascade(label="Help", menu=this.menus.help);
		
		# make toolbar
		this.toolbar_main = tk.Frame(this, bd=1, relief=tk.RAISED);
		
		# new game toolbar action
		tb_main_new = tk.Button(this.toolbar_main, relief=tk.FLAT, command=lambda:game.new(this.canvas));
		tb_main_new.config(text="New");
		try:
			this._image1 = tk.PhotoImage(file="icons/filenew2.gif");
			tb_main_new.config(image=this._image1, compound=tk.LEFT);
		except:
			pass;
		tb_main_new.pack(side=tk.LEFT);
		
		# pause toolbar action
		tb_main_pause = tk.Button(this.toolbar_main, relief=tk.FLAT);
		tb_main_pause.config(text="Pause");
		try:
			this._image2 = tk.PhotoImage(file="icons/pause.gif");
			tb_main_pause.config(image=this._image2, compound=tk.LEFT);
		except:
			pass;
		tb_main_pause.config(command=this.togglePause)
		tb_main_pause.pack(side=tk.LEFT);
		this.tb_main_pause = tb_main_pause;
		
		# toolbar exit button
		tb_exit = ttk.Button(this.toolbar_main, command=this.destroy);
		tb_exit.configure(text="Exit");
		tb_exit.pack(side=tk.RIGHT);
		
		this.toolbar_main.pack(side=tk.TOP, fill=tk.X)
		
		this.config(menu=this.menu);
		this.canvas = tk.Canvas(this, width=500, height=300, bg="#000", bd=0, highlightthickness=0);
		this.canvas.pack();
		
		this.canvas.bind("<Button 1>", this.gameClick);
		this.canvas.bind("<Button 3>", this.gameRight);
		this.gameRight(None); # trigger a right-click now to set up cursor
		
		l = tk.Frame(this);
		this.fill_ = tk.Label(l, text="Fill: ");
		this.fill = tk.Label(l, text="0% ");
		
		this.fill_.grid(row=1, column=0); this.fill.grid(row=1, column=1);
		
		tk.Label(l, text=(" "*10)).grid(row=1, column=2);
		
		this.lives_ = tk.Label(l, text="Lives: ");
		this.lives = tk.Label(l, text="0 ");
		
		this.lives_.grid(row=1, column=10); this.lives.grid(row=1, column=11);
		
		tk.Label(l, text=(" "*10)).grid(row=1, column=12);
		
		this.lvl_ = tk.Label(l, text="Level: ");
		this.lvl = tk.Label(l, text="0 ");
		
		this.lvl_.grid(row=1, column=20); this.lvl.grid(row=1, column=21);
		
		
		l.pack();
		
		game.updateLabel = lambda:this.updateLabel();
	
	def report_callback_exception(this, exc, val, tb):
		import sys, traceback;
		sys.stderr.write("Exception in Tkinter callback\r\n");
		sys.last_type, sys.last_value = exc, val;
		sys.last_traceback = tb;
		traceback.print_exception(exc, val, tb);
		
		messagebox.showerror("Fatal Error",
			str.join("\n", traceback.format_exception(exc, val, tb))
		);
		
		this.destroy();
	
	def openConfiguration(this):
		conf = ConfigureWindow(this);
	
	def updateLabel(this):
		this.fill.config(text=str(game.fill)+"% ")
		this.lives.config(text=str(game.lives)+" ")
		this.lvl.config(text=str(game.level)+" ")
	
	def togglePause(this):
		game.paused = (not game.paused);
		
		if( game.paused ):
			this.tb_main_pause.config(relief=tk.SUNKEN);
		else:
			this.tb_main_pause.config(relief=tk.FLAT);
	
	def gameClick(this, e):
		if( game.paused ):
			# do nothing if the game is paused
			return;
		
		x = int(e.x/16); y = int(e.y/16);
		#print("Clicked", x, y);
		
		# make sure there's nothing here
		for obj in game.objects:
			if( round(obj.x) == x and round(obj.y) == y ):
				# there's an object here, abort
				return;
			if( isinstance(obj, GrowingWall) ):
				# can only be one growingwall at a time
				return;
		
		#print("Spawn", x, y);
		
		# my late-night "clever" code:
		# just flip the mode bit to set direction
		xdir = game.cursorMode;
		ydir = game.cursorMode^1;
		
		# then set the direction both ways
		game.objects.append( GrowingWall(this.canvas, x, y, xdir, ydir) );
		game.objects.append( GrowingWall(this.canvas, x, y,-xdir,-ydir) );
	
	def gameRight(this, e):
		# flip the cursormode between 0 and 1
		game.cursorMode ^= 1;
		if( game.cursorMode ):
			this.canvas.config(cursor="sb_h_double_arrow");
		else:
			this.canvas.config(cursor="sb_v_double_arrow");
	
