import common
import text
import gui

#TODO Finish GUI
#TODO Add difficulty rating system
#TODO Add closeout warning
#TODO Add wealth tracker
#TODO Fix the try catch with the gui here
#TODO don't close the window to refresh lists

config = common.configuration(0, "", [], True)
config.open()
if config.gui:
	#try:
	config = gui.start(config)
	#except:
	#	print("Failed to laod GUI...")
	#	config.gui = False
else:
	config = text.start(config)
config.save()
