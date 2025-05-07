import common

commands = []
config = common.configuration(0, "", [], True)
modified = False
players = common.saveFile(0, [], 0, 0, 0, 0)
prompt = ""

def addPlayer():
	global commands
	global players
	temp = common.player("", "", 0, True, 1, 0)
	intake("Character name: ")
	temp.name = commands[0]
	intake("Player name: ")
	temp.player = commands[0]
	intake("Player level: ")
	temp.lvl = int(commands[0])
	intake("Character current XP: ")
	temp.xp = int(commands[0])
	players.addPlayer(temp)

def attendance():
	global players
	for i in players.players:
		print("Is " + i.player + " here: ",end = '')
		i.present = yn()
	players.calAvg()

def calc():
	global players
	xp = int(input("How mych xp did the party gain: "))
	for i in players.players:
		if i.present:
			i.merit = int(input("How much merit did "+i.name+" earn: "))
	earned, lvlUp = players.calc(xp)
	print("")
	j = 0
	for i in players.players:
		if i.present:
			print(i.player + f" earned: {earned[j]} For a total of: {i.xp}", end="")
			if lvlUp[j]:
				print(" Level up!")
				i.calcLvl()
			else:
				print("")
		j += 1

def intake(prompt):
	global commands
	if commands:
		commands.pop(0)
	if not commands:
		line = input(prompt)
		commands = line.split()

def kill():
	global players
	for i in range(len(players.players)):
		print("[", end="")
		print(i, end="")
		print("]: " + players.players[i].name)
	dead = players.kill(int(input("Select the number for the player you wish killed: ")))
	print(dead.name + " has been killed in action. They will be missed... A hero in their own time...")
	
def printInf():
	global players
	for i in players.players:
		print("Character: " + i.name + f" Level: {i.lvl}")
	print(f"Average party level: {players.avgLvl}")	

def runLoop():
	global commands
	global config
	global modified
	global players
	global prompt
	run = True
	while run:
		intake(prompt)
		if commands[0] == "add":
			addPlayer()
			modified = True
		elif commands[0] == "attend":
			attendance()
		elif commands[0] == "calc":
			calc()
			modified = True
		elif commands[0] == "exit":
			if modified:
				print("File has been modified... Save changes ", end="")
				if yn():
					save()
			run = False		
		elif commands[0] == "help":
			print("A textline utility for tracking Pathfinder 2nd Edition xp values.\nCommands:\nadd: adds a player to the group.\nattend: cycles through which players are present.\nexit: exits the program.\nhelp: displays this helpfile.\nkill: kills a character of your choosing\nload: load a different save file.\nprint: print some basic character info.\nsave: saves the current xp file.\nsaveas: saves the file with the specified file name.\nstart: takes attendance and prints information.")
		elif commands[0] == "kill":
			kill()
			modified = True
		elif commands[0] == "load":
			intake("What file: ")
			config.lastFile = commands[0]
			players.load(config)
			prompt = updatePrompt(config)
			modified = False
		elif commands[0] == "print":
			printInf()
		elif commands[0] == "save":
			save()
			modified = False
		elif commands[0] == "saveas":
			commands = intake(commands, "What save file: ")
			config.lastFile = commands[0]
			save()
			prompt = updatePrompt()
			modified = False
		elif commands[0] == "start":
			attendance()
			printInf()
		else:
			print("Unknown Command: " + commands[0] + "\nType help for more help!")
def save():
	global config
	global players
	if not config.lastFile:
		config.lastFile = input("Save file name: ")
	players.save(config.lastFile)	
	
def start(cfg):
	global config
	global players
	config = cfg
	players.load(config)
	updatePrompt()
	runLoop()
	return config

def updatePrompt():
	global prompt
	if not config.lastFile:
		prompt = "xp"
	else:
		prompt = config.lastFile
	prompt = prompt + ": "
	
def yn():
	while True:
		it = input("y/n: ")
		if it == "y":
			return True
		elif it == "n":
			return False
