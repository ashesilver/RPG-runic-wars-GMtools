import kernel
window = kernel.Graphics()
window.loadGraphicsAttributes()

window.bckg = "./img/start_background.png"



startbutton = kernel.Button(
	[647*window.screen_l/1600,373*window.screen_h/900],
	int(297*window.screen_l/1600),int(131*window.screen_h/900),
	"img/startbutton_base.png","img/startbutton_onclick.png","img/startbutton_hov.png"
	)
menu = True



keyboard_inputs=[]
while type(keyboard_inputs)!=bool :
	window.displayBackgroundUpdate()

	if menu :
		if startbutton() :
			menu = False
			window.bckg= "./img/transition_screen.png"


	window()
	keyboard_inputs = window.getKeys()