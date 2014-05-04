from socket import *
from tkinter import *
import threading

class GUI:
	def __init__(self):
		#defines
		self.widthfen = 800
		self.heightfen = 600
		self.areax = 3000
		self.areay = 2000
		self.robotsize = 50
		self.robot_pos = [0, 0, 0]
		self.others_addr = '1'
		self.asserv_addr = '2'

		#self.serverHost = '10.42.0.52'
		self.serverHost = '127.0.0.1'
		self.serverPort = 2001

		#init comm
		try:
			self.sock = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
			self.sock.settimeout(60)
			self.sock.connect((self.serverHost, self.serverPort))  # connect to server on the port
		except:
			print("WARNING : Socket non ouvert, mode visualisation")

		#init GUI
		self.fen = Tk()
		self.fen.title("Clique moi")

		self.cadre = Canvas(self.fen, width=self.widthfen, height =self.heightfen, bg="light yellow")
		self.cadre.bind("<Button-1>", self.clic_goto)
		self.robot_rect = self.cadre.create_oval(0, 0, self.robotsize, self.robotsize, offset='center', fill='red')
		self.robot_txt = self.cadre.create_text(0, 0, text='Pos')
		self.move_robot(*self.robot_pos)

		self.chaine = Label(self.fen)

		#others
		self.bras_ouvert = False
		self.bras_button = Button(self.fen, text='Bras', command=self.bras)
		self.ret_ouvert = False
		self.ret_button = Button(self.fen, text='Retournement', command=self.ret)

		#reset
		self.reset_pos_button = Button(self.fen, text='Reset position', command=self.reset_pos)
		self.reset_goals_button = Button(self.fen, text='Reset objectifs', command=self.reset_goals)

		#fifo
		self.fifo_switch = Scale(self.fen, from_=0, to=1, label='Fifo', orient='horizontal')

		#goto manue
		self.goto_text = Label(self.fen, text= "Goto")
		self.gotox_e = Entry(self.fen)
		self.gotoy_e = Entry(self.fen)
		self.gotoang = Entry(self.fen)
		self.goto_frame = Frame()
		self.send_goto = Button(self.goto_frame, text="Goto", command=self.goto_handler).pack(side='left')
		self.send_gotoa = Button(self.goto_frame, text="Gotoa", command=self.gotoa_handler).pack(side='right')


		#pwm menu
		self.pwm_text = Label(self.fen, text= "PWM")
		self.pwm_g = Entry(self.fen)
		self.pwm_d = Entry(self.fen)
		self.pwm_duration = Entry(self.fen)
		self.pwm_frame = Frame()
		self.send_pwm = Button(self.pwm_frame, text="Send pwm", command=self.pwm_handler).pack(side='left')

		#reglages
		self.pida_text = Label(self.fen, text="PID angle")
		self.pida_p = Entry(self.fen)
		self.pida_p.insert(0, '180')
		self.pida_i = Entry(self.fen)
		self.pida_i.insert(0, '0')
		self.pida_d = Entry(self.fen)
		self.pida_d.insert(0, '40')

		self.pidd_text = Label(self.fen, text="PID distance")
		self.pidd_p = Entry(self.fen)
		self.pidd_p.insert(0, '2')
		self.pidd_i = Entry(self.fen)
		self.pidd_i.insert(0, '0')
		self.pidd_d = Entry(self.fen)
		self.pidd_d.insert(0, '0.5')

		self.acc_max_text = Label(self.fen, text="Acc max")
		self.acc_max = Entry(self.fen)
		self.acc_max.insert(0, '750')

		self.send_reg = Button(self.fen, text="Send", command=self.val_reg)


		self.chaine.pack(side='bottom')
		self.cadre.pack(side='right', padx=10, pady=10)
		self.bras_button.pack()
		self.ret_button.pack()
		self.fifo_switch.pack()
		self.reset_goals_button.pack(pady=10)
		self.reset_pos_button.pack(pady=10)

		self.goto_text.pack()
		self.gotox_e.pack()
		self.gotoy_e.pack()
		self.gotoang.pack()
		self.goto_frame.pack()

		self.pwm_text.pack()
		self.pwm_g.pack()
		self.pwm_d.pack()
		self.pwm_duration.pack()
		self.pwm_frame.pack()

		self.send_reg.pack(side='bottom')
		self.pidd_d.pack(side='bottom')
		self.pidd_i.pack(side='bottom')
		self.pidd_p.pack(side='bottom')
		self.pidd_text.pack(side='bottom')
		self.pida_d.pack(side='bottom')
		self.pida_i.pack(side='bottom')
		self.pida_p.pack(side='bottom')
		self.pida_text.pack(side='bottom')
		self.acc_max.pack(side='bottom')
		self.acc_max_text.pack(side='bottom')

		threading.Thread(target=self.pos_update).start()
		self.fen.after(100, self.pos_loop)
		self.fen.mainloop()

	def move_robot(self, x, y, a):
		x = int(x)
		y = int(y)
		self.cadre.coords(self.robot_rect, ((x / self.areax) * self.widthfen) - self.robotsize / 2, self.heightfen - ((y / self.areay) * self.heightfen) - self.robotsize / 2, ((x / self.areax) * self.widthfen) + self.robotsize / 2, self.heightfen - ((y / self.areay) * self.heightfen) + self.robotsize / 2)
		self.cadre.coords(self.robot_txt, ((x / self.areax) * self.widthfen), self.heightfen - ((y / self.areay) * self.heightfen) + self.robotsize / 1.5)
		self.cadre.itemconfig(self.robot_txt, text=str(x) + ";" + str(y) + ";" + "{:.2f}".format(a))

	def pos_update(self):
		while 1:
			ret = str(self.sock.recv(1024), 'utf-8')
			try:
				backup = self.robot_pos
				self.robot_pos = list(map(float, ret.split(":")))
				if len(self.robot_pos) != 3:
					print("taille de la pos : " + str(len(self.robot_pos)))
					raise Exception("Robot_pos corompu")
			except:
				print("Exception : robot_pos from backup")
				self.robot_pos = backup

	def pos_loop(self):
		self.move_robot(*self.robot_pos)
		self.fen.after(100, self.pos_loop)

	def bras(self):
		if self.bras_ouvert:
			tosend = [self.others_addr, 'O_BRAS_FERMER!']
		else:
			tosend = [self.others_addr, 'O_BRAS_OUVRIR!']
		tosend = ':'.join(tosend)
		self.bras_ouvert = not self.bras_ouvert
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data

	def ret(self):
		if self.ret_ouvert:
			tosend = [self.others_addr, 'O_RET_FERMER!']
		else:
			tosend = [self.others_addr, 'O_RET_OUVRIR!']
		tosend = ':'.join(tosend)
		self.ret_ouvert = not self.ret_ouvert
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data
	
	def reset_pos(self):
		self.chaine.configure(text = "reset_pos : "+str(200)+" ; "+str(1800)+" ; "+str(-1.57))
		arguments = [str(200), str(1800), str(-1.57)]
		tosend = ':'.join([self.asserv_addr, 'A_SET_POS'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data
	
	def reset_goals(self):
		self.sock.send(bytes(self.asserv_addr+':A_CLEANG!', 'utf-8'))               # send the datas

	def val_reg(self):
		arguments = [str(self.acc_max.get())]
		tosend = ':'.join([self.asserv_addr, 'A_ACCMAX'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data
		arguments = [str(self.pida_p.get()), str(self.pida_i.get()), str(self.pida_d.get())]
		tosend = ':'.join([self.asserv_addr, 'A_PIDA'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data
		arguments = [str(self.pidd_p.get()), str(self.pidd_i.get()), str(self.pidd_d.get())]
		tosend = ':'.join([self.asserv_addr, 'A_PIDD'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data

	def goto(self, gotox, gotoy):
		self.chaine.configure(text = "Goto : "+str(gotox)+" ; "+str(gotoy))
		#ENVOYER DATA PROTOCOLE
		if self.fifo_switch.get() == 0:#on clean la file a chaque nouvel ordre
			self.sock.send(bytes(self.asserv_addr +':A_CLEANG!', 'utf-8'))

		arguments = [str(gotox), str(gotoy)]
		tosend = ':'.join([self.asserv_addr, 'A_GOTO'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data
	
	def gotoa(self, gotox, gotoy, gotoa):
		self.chaine.configure(text = "Gotoa : "+str(gotox)+" ; "+str(gotoy)+" ; "+str(gotoa))
		#ENVOYER DATA PROTOCOLE
		if self.fifo_switch.get() == 0:#on clean la file a chaque nouvel ordre
			self.sock.send(bytes(self.asserv_addr +':A_CLEANG!', 'utf-8'))

		arguments = [str(gotox), str(gotoy), str(gotoa)]
		tosend = ':'.join([self.asserv_addr, 'A_GOTOA'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data

	def sendPwm(self, g, d, duration):
		self.chaine.configure(text = "pwm : "+str(g)+" ; "+str(d)+" ; "+str(duration))
		#ENVOYER DATA PROTOCOLE
		if self.fifo_switch.get() == 0:#on clean la file a chaque nouvel ordre
			self.sock.send(bytes(self.asserv_addr +':A_CLEANG!', 'utf-8'))

		arguments = [str(g), str(d), str(duration)]
		tosend = ':'.join([self.asserv_addr, 'A_PWM'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data

	def pwm_handler(self):
		self.sendPwm(self.pwm_g.get(), self.pwm_d.get(), self.pwm_duration.get())

	def goto_handler(self):
		self.goto(self.gotox_e.get(), self.gotoy_e.get())

	def gotoa_handler(self):
		self.gotoa(self.gotox_e.get(), self.gotoy_e.get(), self.gotoang.get())

	def clic_goto(self, event):
		gotox = int((event.x/self.widthfen)*self.areax)
		gotoy = int(self.areay - (event.y/self.heightfen)*self.areay)
		self.goto(gotox, gotoy)

if __name__ == '__main__':
	gui = GUI()
