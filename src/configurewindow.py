
"""
Main - mainwindow

The main window, with all of the UI elements like menus and toolbars

"""

import tkinter as tk
import tkinter.ttk as ttk

from src.game import game

class ConfigureWindow(tk.Toplevel):
	def __init__(this, root):
		tk.Toplevel.__init__(this, root);
		
		this.resizable(False, False);
		this.title(" ");
		
		this.s1 = tk.Frame(this);
		
		# spinint and associated label for the width
		this.label_width = tk.Label(this.s1, text="Width:")
		this.width = tk.IntVar(this.s1);
		this.inp_width = tk.Spinbox(this.s1, textvariable=this.width,
			value=game.width,
			width=5,
			from_=0,
		);
		this.label_width.grid(row=1, column=1);
		this.inp_width.grid(row=1, column=2);
		
		# spinint and associated label for the height
		this.label_height = tk.Label(this.s1, text="Height:")
		this.height = tk.IntVar(this.s1);
		this.inp_height = tk.Spinbox(this.s1, textvariable=this.height,
			value=game.height,
			width=5,
			from_=0,
		);
		this.label_height.grid(row=1, column=3);
		this.inp_height.grid(row=1, column=4);
		
		# add them as the first line
		this.s1.grid(row=1);
		
		
		this.s2 = tk.Frame(this);
		
		# fill required to 
		this.label_fill = tk.Label(this.s2, text="Fill Required:")
		this.fill = tk.IntVar(this.s2);
		this.inp_fill = tk.Spinbox(this.s2,	textvariable=this.fill,
			value=game.fill_required,
			width=7,
			from_=0,
		);
		this.label_fill_perc = tk.Label(this.s2, text="%")
		
		this.label_fill.grid(row=1, column=1);
		this.inp_fill.grid(row=1, column=2);
		this.label_fill_perc.grid(row=1, column=3);
		
		# add them as the second line
		this.s2.grid(row=2);
		
		
		# finally, the bottons
		this.btns = tk.Frame(this);
		
		this.btn_cancel = ttk.Button(this.btns, text="Cancel");
		this.btn_ok = ttk.Button(this.btns, text="OK");
		
		this.btn_cancel.pack(side=tk.RIGHT);
		this.btn_ok.pack(side=tk.RIGHT);
		
		# the buttons should always at the bottom
		this.btns.grid(row=99);
		
		

