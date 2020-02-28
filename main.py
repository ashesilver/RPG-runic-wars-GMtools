import kernel,copy
window = kernel.Graphics()
window.loadAllAttributes()

custom_resol_1600_900 = kernel.Customres(1600,900)
fullHD = kernel.Customres(1920,1080)
downsizedFullHD = copy.deepcopy(fullHD)
downsizedFullHD.windowDownsize()


#[647*window.screen_l/1600,373*window.screen_h/900]
#int(297*window.screen_l/1600),int(131*window.screen_h/900)
#Title screen
window.bckg = "./img/start_background.png"

startbutton = kernel.Button(
	custom_resol_1600_900.resize(window,[647,373]),
	custom_resol_1600_900.resize(window,[297,131]),
	"img/startbutton_base.png","img/startbutton_onclick.png","img/startbutton_hov.png"
	)
titlescreen = True
#############

#[900*window.screen_l/1920,900*window.screen_h/1080]
#Main menu
testzone = kernel.Textzone(fontsize=24,coordinates=downsizedFullHD.resize(window,[900,900]),maxlength=30)


exit = False
#keyboard_inputs=[]
while not (exit) :
	window.displayBackgroundUpdate()

	if titlescreen :
		if startbutton() :
			titlescreen = False
			window.bckg = "./img/sheeteditor_background.png"
			mainmenu = True
	elif mainmenu :
		testzone()




	exit = window()
	keyboard_inputs = window.getKeys()