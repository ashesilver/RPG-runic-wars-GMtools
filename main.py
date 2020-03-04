import kernel,copy
window = kernel.Graphics()

custom_resol_1600_900 = kernel.Customres(1600,900)
fullHD = kernel.Customres(1920,1080)
downsizedFullHD = copy.deepcopy(fullHD)
downsizedFullHD.windowDownsize()


#Title screen
window.bckg = "./img/start_background.png"

create_startbutton = lambda : kernel.Button(
	custom_resol_1600_900.resize(window,[647,373]),
	custom_resol_1600_900.resize(window,[297,131]),
	"img/startbutton_base.png","img/startbutton_onclick.png","img/startbutton_hov.png"
	)

startbutton = create_startbutton()
titlescreen = True
#############

#Main menu
testzone = kernel.Textzone(fontsize=24,coordinates=downsizedFullHD.resize(window,[900,900]),maxlength=30)
testzone.loadKeysAttributes()


exit = False
#keyboard_inputs=[]
while not (exit) :
	window.displayBackgroundUpdate()

	if titlescreen :
		if startbutton() :
			titlescreen = False
			mainmenu = True
			del startbutton

			###debug kernel.Textzone - has to be mainmenu.png
			window.bckg = "./img/sheeteditor_background.png"
	elif mainmenu :
		### debug for kernel.Textzone
		testzone()




	exit = window()
	#keyboard_inputs = window.getKeys()