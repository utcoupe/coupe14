from socket import *
from tkinter import *


class GUI:
	def __init__(self):
		#defines
		self.widthfen = 800
		self.heightfen = 600
		self.areax = 3000
		self.areay = 2000
		self.others_addr = '1'
		self.asserv_addr = '2'

		self.serverHost = '192.168.2.2'
		self.serverPort = 2001

		#init comm
		try:
			self.sock = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
			self.sock.settimeout(1)
			self.sock.connect((self.serverHost, self.serverPort)) # connect to server on the port
		except:
			print("WARNING : Socket non ouvert, mode visualisation")

		#init GUI
		self.fen = Tk()
		self.fen.title("Clique moi")

		self.cadre = Frame(self.fen, width = self.widthfen, height = self.heightfen, bg="light yellow", relief=SUNKEN)
		self.cadre.bind("<Button-1>", self.clic_goto)

		self.chaine = Label(self.fen)

		self.bras_ouvert = False
		self.bras_button = Button(self.fen, text = 'Bras', command=self.bras)
		self.ret_ouvert = False
		self.ret_button = Button(self.fen, text = 'Retournement', command=self.ret)

		self.reset_pos_button = Button(self.fen, text = 'Reset position', command=self.reset_pos)
		self.reset_goals_button = Button(self.fen, text = 'Reset objectifs', command=self.reset_goals)

		self.fifo_switch = Scale(self.fen, from_=0, to=1, orient='horizontal')

		self.chaine.pack(side = 'bottom')
		self.cadre.pack(side = 'right', padx = 10, pady = 10)
		self.bras_button.pack()
		self.ret_button.pack()
		self.reset_goals_button.pack()
		self.fifo_test = Label(self.fen, text='Fifo').pack()
		self.fifo_switch.pack()
		self.reset_pos_button.pack(side = 'bottom')
		self.fen.mainloop()

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
		self.sock.send(bytes(self.asserv_addr+':A_RESET_POS!', 'utf-8'))               # send the datas
	
	def reset_goals(self):
		self.sock.send(bytes(self.asserv_addr+':A_CLEANG!', 'utf-8'))               # send the datas



	def clic_goto(self, event):
		gotox = int((event.x/self.widthfen)*self.areax)
		gotoy = int(self.areay - (event.y/self.heightfen)*self.areay)
		self.chaine.configure(text = "Goto : "+str(gotox)+" ; "+str(gotoy))
		#ENVOYER DATA PROTOCOLE
		if self.fifo_switch.get() == 0:#on clean la file a chaque nouvel ordre
			self.sock.send(bytes(self.asserv_addr +':A_CLEANG!', 'utf-8'))

		arguments = [str(gotox), str(gotoy)]
		tosend = ':'.join([self.asserv_addr, 'A_GOTO'] + arguments) + '!'
		self.sock.send(bytes(tosend, 'utf-8'))               # send the data

if __name__ == '__main__':
	gui = GUI()
