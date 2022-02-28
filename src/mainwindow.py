
"""
Main - mainwindow

The main window, with all of the UI elements like menus and toolbars

"""

import tkinter as tk

from src.game import game

class Main:
	
	class menus:
		pass;
	
	def __init__(this):
		this.root = tk.Tk();
		
		this.root.title("Jezzball Clone");
		
		# menubar
		this.menu = tk.Menu(this.root);
		
		# file menu
		this.menus.file = tk.Menu(this.menu, tearoff=False);
		this.menus.file.add_command(label="Quit", command=this.root.quit);
		this.menu.add_cascade(label="File", menu=this.menus.file);
		
		# configure menu
		this.menus.settings = tk.Menu(this.menu, tearoff=False);
		this.menus.settings.add_command(label="Configure");
		this.menu.add_cascade(label="Settings", menu=this.menus.settings);
		
		# help menu
		this.menus.help = tk.Menu(this.menu, tearoff=False);
		this.menus.help.add_command(label="About");
		this.menu.add_cascade(label="Help", menu=this.menus.help);
		
		# make toolbar
		this.toolbar_main = tk.Frame(this.root, bd=1, relief=tk.RAISED);
		
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
		tb_main_pause.pack(side=tk.LEFT);
		this.tb_main_pause = tb_main_pause;
		
		# toolbar exit button
		tb_exit = tk.Button(this.toolbar_main, command=this.root.quit);
		tb_exit.configure(text="Exit");
		tb_exit.pack(side=tk.RIGHT);
		
		this.toolbar_main.pack(side=tk.TOP, fill=tk.X)
		
		this.root.config(menu=this.menu);
		this.canvas = tk.Canvas(this.root, width=500, height=300, bg="#000", bd=0, highlightthickness=0);
		this.canvas.pack();
	
	def run(this):
		this.root.mainloop();

