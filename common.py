import pickle
import numpy as np

class configuration(object):
	def __init__(self, version, lastFile, itemList, gui):
	    self.version = version
	    self.lastFile = lastFile
	    self.itemList = itemList
	    self.gui = gui

	def open(self):
		try:
			load = open("xp.cfg", "rb")
			print("Loading config...")
			temp_dict = pickle.load(load)
			load.close()
			self.version = temp_dict.version
			self.lastFile = temp_dict.lastFile
			self.itemList = temp_dict.itemList
			self.gui = temp_dict.gui
		except:
			print("Config file not detected.")
	
	def save(self):
		with open("xp.cfg", "wb") as sv:
			print("Saving config...")
			pickle.dump(self, sv)
			sv.close()
	    
class player(object):
	def __init__(self, name, player, xp, present, lvl, merit):
		self.name = name
		self.player = player
		self.xp = xp
		self.present = present
		self.lvl = lvl
		self.merit = merit
		
	def calcLvl(self):
		self.lvl = int(np.trunc(self.xp/1000)+1)
    
class saveFile(object):
	def __init__(self, version, players, xp, avgLvl, wealth, speed):
		self.version = version
		self.players = players
		self.xp = xp
		self.avgLvl = avgLvl
		self.wealth = wealth
		self.speed = speed #Future use for different advancement speeds
		
	def addPlayer(self, newbie):
		while newbie.xp > 1000:
			newbie.lvl += 1
			newbie.xp -= 1000
		newbie.xp += (newbie.lvl-1)*1000
		self.players.append(newbie)
		
	def adjLvl(self, dif, xp):
		out = xp
		if dif > 0:
			while dif > 0:
				dif -= 1
				out = xp * 1.5
		elif dif < 0:
			dif *= -1
			while dif > 0:
				dif -= 1
				out = xp * .75
		return out
		
	def calAvg(self):
		playerC = 0;
		playerT = 0;
		for i in self.players:
			if(i.present):
				playerC += 1
				playerT += i.lvl
		if playerT > 0:
			self.avgLvl = int(np.round(playerT/playerC))
		else:
			self.avgLvl = 0

	def calc(self, xp):
		highLvl = 0
		lowLvl = 9999
		present  = 0
		lowN = 0
		highN = 0
		totMerit = 0
		totLvl = 0
		ernd = []
		lUp = []
		for i in self.players:
			if i.present:
				present += 1
				if i.lvl < lowLvl:
					lowN = 1
					lowLvl = i.lvl
				elif i.lvl == lowLvl:
					lowN += 1
				if i.lvl > highLvl:
					highN = 1
					highLvl = i.lvl
				elif i.lvl == highLvl:
					highN += 1
				totMerit += i.merit
				totLvl += i.lvl
		if totMerit == 0:
			totMerit = 1
		xp += self.xp
		self.xp = 0
		tenPer = xp/10
		xp -= tenPer
		highXp = xp - tenPer
		lowXp = xp + ((tenPer*highN)/lowN)
		perMerit = (tenPer*present)/totMerit
		for i in self.players:
			earned  = 0		
			lvlUp = False
			if i.present:
				if lowLvl == highLvl:
					earned += xp
				elif i.lvl == lowLvl:
					earned += lowXp
				elif i.lvl == highLvl:
					earned += highXp
				else:
					earned += xp
				earned += i.merit*perMerit
				earned = self.adjLvl(self.avgLvl-i.lvl, earned)	
				target = i.lvl*1000	
				if (earned + i.xp) >= target:
					remainder = earned + i.xp - target
					earned -= remainder
					earned += self.adjLvl(-1, remainder)	
					if (earned + i.xp) >= (target + 1000):
						self.xp += self.adjLvl(i.lvl - self.avgLvl, (earned - ((target + 999) - i.xp))/len(self.players))
						earned = (target + 999) - i.xp
					lvlUp = True
					i.calcLvl()
				i.xp += int(np.round(earned))
			ernd.append(int(np.round(earned)))
			lUp.append(lvlUp)
		self.calAvg()
		return ernd, lUp

	def kill(self, a):
		return self.players.pop(a)
		
	def load(self, config):
		try:
			loadFile = open(config.lastFile, "rb")
			print("Loading characters...")
			temp = pickle.load(loadFile)
			loadFile.close()
			self.version = temp.version
			self.players = temp.players
			self.xp = temp.xp
			self.avgLvl = temp.avgLvl
			self.wealth = temp.wealth
			self.speed = temp.speed 
		except:
			print("Save file not found...")
		
	def save(self, fileName):
		with open(fileName, "wb") as saveFile:
			print("Saving...")
			pickle.dump(self, saveFile)
			saveFile.close()

class store(object):
	def __init__(self, name, salePrice, tags):
		self.name = name
		self.salePrice = salePrice
		self.tags = tags
