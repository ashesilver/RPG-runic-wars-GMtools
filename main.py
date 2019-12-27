import kernel
window = kernel.Graphics()
window.loadGraphicsAttributes()


#Title screen
window.bckg = "./img/start_background.png"

startbutton = kernel.Button(
	[647*window.screen_l/1600,373*window.screen_h/900],
	int(297*window.screen_l/1600),int(131*window.screen_h/900),
	"img/startbutton_base.png","img/startbutton_onclick.png","img/startbutton_hov.png"
	)
titlescreen = True
#############

exit = False
#keyboard_inputs=[]
while not (exit) :
	window.displayBackgroundUpdate()

	if titlescreen :
		if startbutton() :
			titlescreen = False
			window.bckg= "./img/transition_screen.png"
			mainmenu = True
	elif mainmenu :
		pass




	exit = window()
	#keyboard_inputs = window.getKeys()