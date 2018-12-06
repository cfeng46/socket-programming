import socket
import sys
import subprocess
import os
import time
import struct
global player
# constants
game_state = (
"""
	 ------
	 |    |
	 |
	 |
	 |
	 |
	 |
	 |
	 |
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |
	 |
	 |
	 |
	 |
	 |
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |   -+-
	 | 
	 |   
	 |   
	 |   
	 |   
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |  /-+-
	 |   
	 |   
	 |   
	 |   
	 |   
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |  /-+-/
	 |   
	 |   
	 |   
	 |   
	 |   
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |  /-+-/
	 |    |
	 |   
	 |   
	 |   
	 |   
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |  /-+-/
	 |    |
	 |    |
	 |   | 
	 |   | 
	 |   
	----------
""",
"""
	 ------
	 |    |
	 |    O
	 |  /-+-/
	 |    |
	 |    |
	 |   | |
	 |   | |
	 |  
	----------
""")

# This class contains all the functions required for the hangman game
class hangman():
	def connect(self, HOST, PORT):
		# Create a socket and establish a connection
		self.HOST = HOST
		self.PORT = PORT
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("connecting...")
		
		self.sock.connect((self.HOST, self.PORT))
		print("connection established...\n")
		data = struct.pack('>1B', player)
		self.sock.sendall(data)

	def game_display(self):
		print ("\n" + game_state[self.total_Wrong] + "\n")

	def game_display2(self):
		print ("\n" + game_state[self.total_Wrong2] + "\n")

	def game_setup2(self):
		self.wrong_guess2 = ""
		self.puzzle2 = ""
		self.total_Wrong2 = 0
		self.word2 = self.sock.recv(1024)
		self.msg2 = struct.iter_unpack('>1B', self.word2)
		self.endGame2 = next(self.msg2)[0]
		while self.endGame2 != 0:
			end = struct.unpack('>1B' + str(self.endGame2) + 's', self.word2)
			print (end[1].decode())
			if end[1].decode() == 'game overload':
				sys.exit(1)
			else:
				self.word2 = self.sock.recv(1024)
				self.msg2 = struct.iter_unpack('>1B', self.word2)
				self.endGame2 = next(self.msg2)[0]
		while (self.endGame2 == 0):
			self.word_length2 = next(self.msg2)[0]
			self.num_incorrect2 = next(self.msg2)[0]
			self.game_display2()
			self.total_Wrong2 = int(self.num_incorrect2)
			self.message2 = struct.unpack('>3B' + str(self.word_length2) + 's' + str(self.num_incorrect2) + 's', self.word2)
			self.puzzle2 = self.message2[3].decode()
			self.wrong_guess2 = self.message2[4].decode()
			#print ("Your Turn")
			print (self.puzzle2)
			print ("the incorrect guess: {}\n".format(self.wrong_guess2))
			self.data2 = input("Enter a guess: ")
			while len(self.data2) != 1:
				self.data2 = input("Error, please Enter one letter: ")
			while not self.data2.isalpha():
				self.data2 = input("Error, please Enter one letter: ")
			while self.data2 in self.wrong_guess2 or self.data2 in self.puzzle2:
				print ("\nYou have already guessed this: try again")
				self.data2 = input("Enter a guess: ")
			self.data2 = self.data2.lower()
			sent = struct.pack('>1B1s', 1, bytes(self.data2, 'utf-8'))
			self.sock.sendall(sent)
			self.word2 = self.sock.recv(1024)
			self.msg2 = struct.iter_unpack('>1B', self.word2)
			self.endGame2 = next(self.msg2)[0]
			while self.endGame2 != 0:
				if self.endGame2 > 30:
					self.is_done2()
				else:
					end = struct.unpack('>1B' + str(self.endGame2) + 's', self.word2)
					print (end[1].decode())
					self.word2 = self.sock.recv(1024)
					self.msg2 = struct.iter_unpack('>1B', self.word2)
					self.endGame2 = next(self.msg2)[0]

	def is_done2(self):
		done = struct.unpack('>1B' + str(self.endGame2) + 's', self.word2)
		gameover = done[1].decode()
		print (gameover)
		self.sock.close()
		sys.exit(1)

	def game_setup(self):
		self.wrong_guess = ""
		self.puzzle = ""
		self.total_Wrong = 0
		self.word = self.sock.recv(4096)
		self.msg = struct.iter_unpack('>1B', self.word)
		self.endGame = next(self.msg)[0]
		while (self.endGame == 0):
			self.word_length = next(self.msg)[0]
			self.num_incorrect = next(self.msg)[0]
			self.game_display()
			self.total_Wrong = int(self.num_incorrect)
			self.message = struct.unpack('>3B' + str(self.word_length) + 's' + str(self.num_incorrect) + 's', self.word)
			self.puzzle = self.message[3].decode()
			self.wrong_guess = self.message[4].decode()
			print (self.puzzle)
			print ("the incorrect guess: {}\n".format(self.wrong_guess))
			self.data = input("Enter a guess: ")
			while len(self.data) != 1:
				self.data = input("Error, please Enter one letter: ")
			while not self.data.isalpha():
				self.data = input("Error, please Enter one letter: ")
			while self.data in self.wrong_guess or self.data in self.puzzle:
				print ("\nYou have already guessed this: try again")
				self.data = input("Enter a guess: ")
			self.data = self.data.lower()
			sent = struct.pack('>1B1s', 1, bytes(self.data, 'utf-8'))
			self.sock.sendall(sent)
			self.word = self.sock.recv(4096)			
			self.msg = struct.iter_unpack('>1B', self.word)
			self.endGame = next(self.msg)[0]
		self.is_done()
	
	def is_done(self):
		done = struct.unpack('>1B' + str(self.endGame) + 's', self.word)
		gameover = done[1].decode()
		print (gameover)
		

if __name__ == "__main__":
	if len(sys.argv) > 2:
		HOST = sys.argv[1]
		PORT = int(sys.argv[2])
		player = 0
		game = hangman()
		try:
			ask = str(input("Two Players?(y/n): "))
			if ask == "y":
				player = 2
				game.connect(HOST, PORT)
				game.game_setup2()
			else:
				answer = str(input("Are you ready to start? y/n: "))
				if answer.lower() == 'y':
					game.connect(HOST, PORT)
					game.game_setup()
				else:
					game.sock.close()
			
			
		except (OverflowError, IOError):
			print("Error Message")	
				
		finally:
			 game.sock.close()
	else:
		print ("incorrect input")
		sys.exit(1)