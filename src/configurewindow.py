
"""
Main - mainwindow

The main window, with all of the UI elements like menus and toolbars

"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

from src.game import game
from src.Ball import Ball

class ConfigureWindow(tk.Toplevel):
	def __init__(this, root):
		tk.Toplevel.__init__(this, root);
		this.transient(root);
		this.root = root;
		
		this.resizable(False, False);
		this.title(" ");
		
		this.s1 = tk.Frame(this);
		
		# spinint and associated label for the width
		this.label_width = tk.Label(this.s1, text="Width:")
		this.width = tk.IntVar(this.s1, game.width);
		this.inp_width = tk.Spinbox(this.s1, textvariable=this.width,
			width=5,
			from_=1, to=min(250, round((root.winfo_screenwidth()/16)+(1/2))),
			increment=1,
		);
		this.inp_width.config(increment=1.0);
		this.label_width.grid(row=1, column=1);
		this.inp_width.grid(row=1, column=2);
		
		# spinint and associated label for the height
		this.label_height = tk.Label(this.s1, text="Height:")
		this.height = tk.IntVar(this.s1, game.height);
		this.inp_height = tk.Spinbox(this.s1, textvariable=this.height,
			width=5,
			from_=1, to=min(250, (round((root.winfo_screenheight()/16)+(1/2))-6)),
			increment=1,
		);
		this.label_height.grid(row=1, column=3);
		this.inp_height.grid(row=1, column=4);
		
		# add them as the first line
		this.s1.grid(row=1);
		
		
		this.s2 = tk.Frame(this);
		
		# fill required to 
		this.label_fill = tk.Label(this.s2, text="Fill Required:")
		this.fill = tk.DoubleVar(this.s2, game.fill_required);
		this.inp_fill = tk.Spinbox(this.s2, textvariable=this.fill,
			width=7,
			from_=9, to=99,
			increment=1,
		);
		this.label_fill_perc = tk.Label(this.s2, text="%")
		
		this.label_fill.grid(row=1, column=1);
		this.inp_fill.grid(row=1, column=2);
		this.label_fill_perc.grid(row=1, column=3);
		
		# add them as the second line
		this.s2.grid(row=2);
		
		this.ballcollide = tk.BooleanVar(this, Ball.ballCollide);
		this.inp_ballcollide = ttk.Checkbutton(this,
			text="Balls collide against other balls",
			variable=this.ballcollide,
		);
		this.inp_ballcollide.grid(row=3);
		
		# finally, the bottons
		this.btns = tk.Frame(this);
		
		this.btn_cancel = ttk.Button(this.btns, text="Cancel", command=this.destroy);
		this.btn_apply = ttk.Button(this.btns, text="Apply", command=this.apply);
		this.btn_ok = ttk.Button(this.btns, text="OK", command=this.okButton);
		
		this.btn_cancel.pack(side=tk.RIGHT);
		this.btn_apply.pack(side=tk.RIGHT);
		this.btn_ok.pack(side=tk.RIGHT);
		
		# the buttons should always at the bottom
		this.btns.grid(row=99);
		
		this.focus_force();
		this.grab_set();
	
	def apply(this):
		# set size
		
		try:
			newWidth = int(this.width.get());
			newHeight = int(this.height.get());
		except:
			tk.messagebox.showerror("Error", "The width or height entered is invalid!");
			return False;
		
		try:
			newFill = float(this.fill.get());
		except:
			tk.messagebox.showerror("Error", "The fill amount entered is invalid!");
			return False;
		
		if(
			( newWidth < this.inp_width.cget("from") or newWidth > this.inp_width.cget("to") )
			or
			( newHeight < this.inp_height.cget("from") or newHeight > this.inp_height.cget("to") )
			or
			( newFill < this.inp_fill.cget("from") or newHeight > this.inp_fill.cget("to") )
		):
			tk.messagebox.showerror("Error", "One or more values are outside the valid range.");
			return False;
		
		game.width = newWidth;
		game.height = newHeight;
		
		game.fill_required = newFill;
		
		Ball.ballCollide = this.ballcollide.get();
		
		# start a new game to apply changes
		game.new(this.root.canvas);
		
		return True;
	
	def okButton(this):
		if( this.apply() ):
			# if applying is successful, close dialog
			this.destroy();

