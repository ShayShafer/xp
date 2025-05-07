import tkinter as tk
import common

checkBoxes = []
config = common.configuration(0, "", [], True)
lvlRange = []
meritVar = []
miscXp = None
modified = False
players = common.saveFile(0, [], 0, 0, 0, 0)
prompt = ""
root = None
tally = None
title = ""
xpVar = []	
	

def addPlayerBtn(p):
	def commitPlayer(p):
		global players
		t = common.player(name.get(), person.get(), int(xp.get()), True, int(lvl.get()), 0)
		players.players.append(t)
		destRoot()
		prom.destroy()
		drawRoot()

	prom = tk.Tk()
	prom.title("AddPlayer")
	grid = tk.Frame(prom)
	tk.Label(grid, text = "Name").grid(row = 0, column = 0)
	tk.Label(grid, text = "Player").grid(row = 0, column = 1)
	tk.Label(grid, text = "Lvl").grid(row = 0, column = 2)	
	tk.Label(grid, text = "XP").grid(row = 0, column = 3)
	name = tk.Entry(grid)
	person = tk.Entry(grid)
	lvl = tk.Entry(grid)
	xp = tk.Entry(grid)
	name.grid(row = 1, column = 0)
	person.grid(row = 1, column = 1)
	lvl.grid(row = 1, column = 2)
	xp.grid(row = 1, column = 3)
	tk.Button(grid, text="Add Player", command= lambda p = p: commitPlayer(p)).grid(row = 1, column = 4)
	grid.pack()
	prom.mainloop()

def accumulate(p):
	global players
	global miscXp
	global tally
	multp = [10, 30, 80, 2, 3, 4, 6, 8, 12, 16, 24, 32, 10, 15, 20, 30, 40, 60, 80, 120, 160]
	accu = 0
	for i in range(21):
		accu += multp[i] * xpVar[i].get()
		xpVar[i].set(0)
	if miscXp.get():
		accu += int(miscXp.get())
	tally.set(tally.get()+accu)
	players.xp = tally.get()
	
def btnUp(i):
	global xpVar
	xpVar[i].set(xpVar[i].get()+1)
	
def btnDwn(i):
	global xpVar
	xpVar[i].set(xpVar[i].get()-1)
	
def calc(p):
	global players
	accumulate(0)
	earned, lvlUp = players.calc(0)
	destRoot()
	disp = tk.Tk()
	grid = tk.Frame(disp)
	for i in range(len(earned)):
		if players.players[i].present:
			tk.Label(grid, text = players.players[i].name).grid(row = i, column = 0)
			tk.Label(grid, text = earned[i]).grid(row = i, column = 1)
			if lvlUp[i]:	
				tk.Label(grid, text = "Level Up!").grid(row = i, column = 2)
	grid.pack()
	disp.mainloop()
	drawRoot()

def check_change(j):
	global checkBoxes
	global lvlRange
	global players
	oldAvg = players.avgLvl
	players.players[j].present = not players.players[j].present
	players.calAvg()
	lvlDif = oldAvg - players.avgLvl
	for i in range(9):
		lvlRange[i].set(lvlRange[i].get()-lvlDif)
		
def destRoot():
	global checkBoxes
	global lvlRange
	global meritVar
	global xpVar
	checkBoxes = []
	lvlRange = []
	meritVar = []
	xpVar = []	
	root.destroy()

def drawRoot():
	global checkBoxes
	global config
	global lvlRange
	global meritVar
	global miscXp
	global players
	global root
	global tally
	global title
	global xpVar
	updateTitle()
	root = tk.Tk()
	root.title(title)
	tk.Label(root, text="Players").pack()
	playerList = tk.Frame(root, padx = 10, pady = 10)
	tk.Label(playerList, text = "Present").grid( row = 0, column = 0)
	tk.Label(playerList, text = "Name").grid( row = 0, column = 1)	
	tk.Label(playerList, text = "Player").grid( row = 0, column = 2)
	tk.Label(playerList, text = "XP").grid( row = 0, column = 3)
	tk.Label(playerList, text = "Lvl").grid( row = 0, column = 4)
	tk.Label(playerList, text = "Merit").grid( row = 0, column = 6)
	tk.Label(playerList, text = "Kill").grid( row = 0, column = 8)
	j = 0
	for i in players.players:
		tBool = tk.BooleanVar()
		checkBoxes.append(tBool)
		tMerit = tk.StringVar()
		tMerit.set(i.merit)
		meritVar.append(tMerit)
		check = tk.Checkbutton(playerList, variable=tBool, command=lambda j=j: check_change(j), onvalue=1, offvalue=0)
		check.grid(row = j+1, column = 0)
		if i.present:
			check.select()
		tk.Label(playerList, text = i.name).grid( row = j+1, column = 1)	
		tk.Label(playerList, text = i.player).grid( row = j+1, column = 2)
		tk.Label(playerList, text = i.xp).grid( row = j+1, column = 3)
		tk.Label(playerList, text = i.lvl).grid( row = j+1, column = 4)
		tk.Button(playerList, text="<", command=lambda j=j: meritDown(j)).grid( row = j+1, column = 5)
		tk.Label(playerList, textvariable = meritVar[j]).grid( row = j+1, column = 6)
		tk.Button(playerList, text=">", command=lambda j=j: meritUp(j)).grid( row = j+1, column = 7)
		tk.Button(playerList, text="X", bg = "red", command=lambda j=j: kill(j)).grid( row = j+1, column = 8)
		j += 1
	playerList.pack()
	accList = tk.Frame(root, bg = "green", padx = 10, pady = 10)
	hazList = tk.Frame(root, bg = "yellow", padx = 10, pady = 10)
	advList = tk.Frame(root, bg = "red", padx = 10, pady = 10)
	misList = tk.Frame(root, padx = 10, pady = 10)
	tk.Label(accList, text = "Accomplishment").grid( row = 0, column = 0, columnspan = 4)
	tk.Label(accList, text = "Minor").grid(row = 1, column = 0)
	tk.Label(accList, text = "Moderate").grid(row = 1, column = 1)
	tk.Label(accList, text = "Major").grid(row = 1, column = 2)
	tk.Label(hazList, text = "Hazard").grid( row = 0, column = 0, columnspan = 9)
	tk.Label(advList, text = "Adversary").grid( row = 0, column = 0, columnspan = 9)
	tk.Label(accList, text = "Misc").grid( row = 1, column = 3)
	miscXp = tk.Entry(accList)
	miscXp.grid(row = 3, column = 3)
	for i in range(9):
		tLvl = tk.IntVar()
		tLvl.set(players.avgLvl+i-4)
		lvlRange.append(tLvl)
		tk.Label(hazList, textvariable = lvlRange[i]).grid( row = 1, column = i)
		tk.Label(advList, textvariable = lvlRange[i]).grid( row = 1, column = i)
	for i in range(21):
		tXp = tk.IntVar()
		tXp.set(0)
		xpVar.append(tXp)
		if i < 3:
			col = i
			lis = accList
		elif i < 12:
			col = i - 3
			lis = hazList
		elif i < 21:
			col = i - 12
			lis = advList
		else:
			col = - 1
			lis = root
		tk.Button(lis, text = "^", command = lambda i=i:btnUp(i)).grid(row = 2, column = col)
		tk.Label(lis, textvariable = xpVar[i]).grid(row = 3, column = col)
		tk.Button(lis, text = "v", command = lambda i=i:btnDwn(i)).grid(row = 4, column = col)
	tally = tk.IntVar()
	tally.set(players.xp)
	tk.Label(misList, text = "Accumulation").grid(row = 0, column = 2)
	tk.Label(misList, textvariable = tally).grid(row = 3, column = 2)
	tk.Button(misList, text="Accumulate", command = lambda j=j : accumulate(j)).grid( row = 3, column = 1)
	tk.Button(misList, text="Calc!", command=lambda j=j: calc(j)).grid( row = 3, column = 3)
	accList.pack(expand=True, fill=tk.BOTH)
	hazList.pack(expand=True, fill=tk.BOTH)
	advList.pack(expand=True, fill=tk.BOTH)
	misList.pack(expand=True, fill=tk.BOTH)
	tk.Button(root, text="Add Player", command=lambda j=j: addPlayerBtn(j)).pack()
	tk.Button(root, text="Reset Merit", command=lambda j=j: resetMerit(j)).pack()
	tk.Button(root, text="Save", command=lambda j=j: save(j)).pack()
	root.mainloop()
	
def kill(j):
	global players
	global root
	players.kill(j)
	destRoot()
	drawRoot()

def meritDown(j):
	global meritVar
	global players
	players.players[j].merit -= 1
	meritVar[j].set(players.players[j].merit)

def meritUp(j):
	global meritVar
	global players
	players.players[j].merit += 1
	meritVar[j].set(players.players[j].merit)

def resetMerit(p):
	global players
	global meritVar
	for i in range(len(players.players)):
		players.players[i].merit = 0
		meritVar[i].set(0)
	
def save(p):
	global config
	global players
	ent = None
	def pr(p):
		config.LastFile = ent.get()
		sv.destroy()
	if not config.lastFile:
		sv = tk.Tk()
		ent = tk.Entry(sv)
		tk.Button(sv, command = lambda p=p: pr(p))
		sv.mainloop()
	players.save(config.lastFile)
	
def start(cfg):
	global config
	global players
	config = cfg
	players.load(config)
	drawRoot()
	return config
	
def updateTitle():
	global config
	global title
	title = config.lastFile
	title +=  " - XP"		
