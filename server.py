from socket import *
import _thread
import time
import random
import sys
import struct
global puzzle
global server
global end_game
global gameover
global thread_count
global wordlist
global clients1
global clients2
global clients3
global nex
nex = 1
clients1 = []
clients2 = []
clients3 = []
thread_count = 0
wordlist = ['test', 'meet', 'nest', 'make', 'date', 'apple', 'ready', 'which', 'first', 'poster', 'notebook', 'feedback', 'messages', 'examples', 'database']

class threaded_Serv():
	def __init__(self):
		self.length = len(puzzle)
		print (puzzle)

def handler2(clientsock1, addr1, clientsock2, addr2):
	global end_game2
	global gameover2
	global game
	game = 1
	end_game2 = 0
	gameover2 = False
	start = "Game starting!\nYour Turn"
	respond = struct.pack('>1B' + str(len(start)) + 's', len(start), bytes(start, 'utf-8'))
	clientsock1.sendall(respond)
	turn = "Your Turn"
	respond2 = struct.pack('>1B' + str(len(turn)) + 's', len(turn), bytes(turn, 'utf-8'))
	#wait1 = "Waiting on Player2"
	wait2 = "Game starting!\nWaiting on Player1"
	respond3 = struct.pack('>1B' + str(len(wait2)) + 's', len(wait2), bytes(wait2, 'utf-8'))
	#clientsock1.sendall(respond)
	#time.sleep(3)
	#clientsock2.sendall(respond)
	#time.sleep(3)
	clientsock2.sendall(respond3)
	wrong_guess = ""
	initial_pack = '_' * len(puzzle)
	while not gameover2:
		if game == 1:
			respond4 = struct.pack('>3B' + str(len(puzzle)) + 's' + str(end_game2) + 's', 0, len(puzzle), end_game2, bytes(initial_pack, 'utf-8'), bytes(wrong_guess, 'utf-8'))
			clientsock1.sendall(respond4)
			data = clientsock1.recv(1024).strip()
			respond5 = struct.unpack('>1B1s', data)
			guess = respond5[1].decode()
		else:
			respond4 = struct.pack('>3B' + str(len(puzzle)) + 's' + str(end_game2) + 's', 0, len(puzzle), end_game2, bytes(initial_pack, 'utf-8'), bytes(wrong_guess, 'utf-8'))
			clientsock2.sendall(respond4)
			data = clientsock2.recv(1024).strip()
			respond5 = struct.unpack('>1B1s', data)
			guess = respond5[1].decode()
		if guess in puzzle:
			pack = list(initial_pack)
			for i in range(len(puzzle)):
				if guess == puzzle[i]:
					pack[i] = guess
			initial_pack = "".join(pack)
			print (initial_pack)
			if game == 1:
				if initial_pack == puzzle:
					print('you win')
					over = "The word was " + puzzle + "\n" + "You WIN!\nGameOver!"
					lose = "The word was " + puzzle + "\n" + "You Lose!\nGameOver!"
					respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
					respond1 = struct.pack('>1B' + str(len(lose)) + 's', len(lose), bytes(lose, 'utf-8'))
					clientsock1.sendall(respond)
					clientsock2.sendall(respond1)
					gameover = True
					sys.exit(1)
				else:
					answer = "correct\nwait on player2"
					respond6 = struct.pack('>1B' + str(len(answer)) + 's', len(answer), bytes(answer, 'utf-8'))
					clientsock1.sendall(respond6)
					game = 2
					clientsock2.sendall(respond2)
			else:
				if initial_pack == puzzle:
					print('you win')
					gameover = True
					over = "The word was" + puzzle + "\n" + "You WIN!\nGameOver!"
					lose = "The word was " + puzzle + "\n" + "You Lose!\nGameOver!"
					respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
					respond1 = struct.pack('>1B' + str(len(lose)) + 's', len(lose), bytes(lose, 'utf-8'))
					clientsock2.sendall(respond)
					clientsock1.sendall(respond1)
					sys.exit(1)
				else:
					answer = "correct\nwait on player1"
					respond6 = struct.pack('>1B' + str(len(answer)) + 's', len(answer), bytes(answer, 'utf-8'))
					clientsock2.sendall(respond6)
					game = 1
					clientsock1.sendall(respond2)
		else:
			end_game2 += 1
			wrong_guess += guess
			if end_game2 >= 6:
				gameover = True
				if game == 1:
					over = "The word was " + puzzle + "\n" + "You Loss!\nGameOver!"
					win = "The word was " + puzzle + "\n" + "You WIN!\nGameOver!"
					respond1 = struct.pack('>1B' + str(len(win)) + 's', len(win), bytes(win, 'utf-8'))
					respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
					clientsock1.sendall(respond)
					clientsock2.sendall(respond1)
				else:
					over = "The word was " + puzzle + "\n" + "You Loss!\nGameOver!"
					win = "The word was " + puzzle + "\n" + "You WIN!\nGameOver!"
					respond1 = struct.pack('>1B' + str(len(win)) + 's', len(win), bytes(win, 'utf-8'))
					respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
					clientsock2.sendall(respond)
					clientsock1.sendall(respond1)
			else:
				if game == 1:
					answer = "incorrect\nwait on player2"
					respond6 = struct.pack('>1B' + str(len(answer)) + 's', len(answer), bytes(answer, 'utf-8'))
					clientsock1.sendall(respond6)
					game = 2
					clientsock2.sendall(respond2)
				else:
					answer = "incorrect\nwait on player1"
					respond6 = struct.pack('>1B' + str(len(answer)) + 's', len(answer), bytes(answer, 'utf-8'))
					clientsock2.sendall(respond6)
					game = 1
					clientsock1.sendall(respond2)

def handler(clientsock,addr):

	global end_game
	global thread_count
	global gameover
	global nex
	server = threaded_Serv()
	print (thread_count)
	if len(clients1) == 2 and len(clients2) < 2 and len(clients3) == 0:
		thread_count = 2
	elif len(clients1) == 2 and len(clients2) == 2 and len(clients3) < 2:
		thread_count = 3
	print ("here")
	print (thread_count)
	data = clientsock.recv(4096).strip()
	msg = struct.unpack('>1B', data)
	end_game = 0
	gameover = False
	if msg[0] == 0:
		if thread_count > 3:
			mess = "game overload"
			respond = struct.pack('>1B' + str(len(mess)) + 's', len(mess), bytes(mess, 'utf-8'))
			clientsock.sendall(respond)
			clientsock.close()
		else:
			wrong_guess = ""
			initial_pack = '_' * server.length
			while not gameover:
				respond = struct.pack('>3B' + str(server.length) + 's' + str(end_game) + 's', 0, server.length, end_game, bytes(initial_pack, 'utf-8'), bytes(wrong_guess, 'utf-8'))
				clientsock.sendall(respond)
				data = clientsock.recv(4096).strip()
				respond = struct.unpack('>1B1s', data)
				guess = respond[1].decode()
				if guess in puzzle:
					pack = list(initial_pack)
					for i in range(len(puzzle)):
						if guess == puzzle[i]:
							pack[i] = guess
					initial_pack = "".join(pack)
					if initial_pack == puzzle:
						print('you win')
						gameover = True
				else:
					end_game += 1
					wrong_guess += guess
					if end_game >= 6:
						gameover = True
			if end_game >= 6:
				over = "The word was " + puzzle + "\n" + "You Loss!\nGameOver!"
				print (len(over))
				respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
				clientsock.sendall(respond)
			else:
				over = "The word was" + puzzle + "\n" + "You WIN!\nGameOver!"
				respond = struct.pack('>1B' + str(len(over)) + 's', len(over), bytes(over, 'utf-8'))
				clientsock.sendall(respond)
			thread_count -= 1
	elif msg[0] == 2:
		if thread_count > 3:
			mess = "game overload"
			respond = struct.pack('>1B' + str(len(mess)) + 's', len(mess), bytes(mess, 'utf-8'))
			clientsock.sendall(respond)
			clientsock.close()
		else:
			print (clients1)
			print (clients2)
			print (clients3)
			print(nex)
			if len(clients1) != 2:
				clients1.append((clientsock, addr))
			elif len(clients2) != 2:
				clients2.append((clientsock, addr))
			elif len(clients3) != 2:
				clients3.append((clientsock, addr))
			if nex == 1:
				while len(clients1) != 2:
					continue
				if addr in clients1[1]:
					nex = 2
					handler2(clients1[0][0], clients1[0][1], clients1[1][0], clients1[1][1])
			elif nex == 2:
				while len(clients2) != 2:
					continue
				if addr in clients2[1]:
					nex = 3
					handler2(clients2[0][0], clients2[0][1], clients2[1][0], clients2[1][1])
			elif nex == 3:
				while len(clients3) != 2:
					continue
				if addr in clients3[1]:
					handler2(clients3[0][0], clients3[0][1], clients3[1][0], clients3[1][1])

if __name__=='__main__':
	if len(sys.argv) > 1:
		PORT = int(sys.argv[1])
		HOST = '0.0.0.0'
	# Generate Puzzle 
		puzzle = random.choice(wordlist)
		end_game = False
		
		#os.system('cls' if os.name == 'nt' else 'clear')
		print ("\n" + puzzle)
		
		# Socket Setup 	
		ADDR = (HOST, PORT)
		serversock = socket(AF_INET, SOCK_STREAM)
		serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		serversock.bind(ADDR)
		serversock.listen(6)
		# Establish Connections 
		while 1:
			print ('waiting for connection... listening on port', PORT)
			clientsock, addr = serversock.accept()
			print ('...connected from:', addr)
			t = _thread.start_new_thread(handler, (clientsock, addr));
			thread_count += 1
	else:
		print ("incorrect input")
		sys.exit(1)
