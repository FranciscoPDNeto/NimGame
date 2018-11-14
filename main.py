import os
from time import sleep
from random import randint

numLines = 4
score = 0
isWinnerSituation = None

'''
Matriz que terá cada bit de número de palitos de cada linha.
Dispostos de forma que se possa encontrar as somas rX colocadas
na especificação.
'''
Matrix = [[0 for x in range(3)] for y in range(numLines)]

'''
Função para mostrar na tela a situação corrente do jogo.
'''
def printGame(matchsticksByLine, score):
	for i in range(numLines):
		print ((i+1), ' '*(numLines-i-1) + 'I'*(matchsticksByLine[i]))
	print ("Score: ", score)

'''
Função para pegar cada bit dos números de palitos por linha.
Usada para verificar se a soma desses bits são todos pares
ou não, discriminando assim situações ganhadores e perdedoras.
'''
def getBits(matchsticksByLine):
	a3 = ('{0:03b}'.format(matchsticksByLine[0]))[2]
	a2 = ('{0:03b}'.format(matchsticksByLine[0]))[1]
	a1 = ('{0:03b}'.format(matchsticksByLine[0]))[0]

	b3 = ('{0:03b}'.format(matchsticksByLine[1]))[2]
	b2 = ('{0:03b}'.format(matchsticksByLine[1]))[1]
	b1 = ('{0:03b}'.format(matchsticksByLine[1]))[0]

	c3 = ('{0:03b}'.format(matchsticksByLine[2]))[2]
	c2 = ('{0:03b}'.format(matchsticksByLine[2]))[1]
	c1 = ('{0:03b}'.format(matchsticksByLine[2]))[0]

	d3 = ('{0:03b}'.format(matchsticksByLine[3]))[2]
	d2 = ('{0:03b}'.format(matchsticksByLine[3]))[1]
	d1 = ('{0:03b}'.format(matchsticksByLine[3]))[0]

	Matrix = [[int(a1), int(b1), int(c1), int(d1)],
			  [int(a2), int(b2), int(c2), int(d2)],
			  [int(a3), int(b3), int(c3), int(d3)]]

	return Matrix

'''
Verifica se a jogada é ganhadora ou perdedora
'''
def verifyGameSituation(matchsticksByLine):
	Matrix = getBits(matchsticksByLine)
	global isWinnerSituation
	r = [0 for x in range(3)]
	#soma as linhas, tendo assim r1, r2 e r3
	for x in range(3):
		r[x] = sum(Matrix[x])

	#verifica se todas as somas(r1, r2, r3) das linhas
	#são pares
	if all(rX % 2 == 0 for rX in r):
		isWinnerSituation = False
	else:
		isWinnerSituation = True

'''
Verifica se a situação do jogo está dentre as seguintes
disposições:
(0,0,0,1), (0,0,1,0), (0,1,0,0), (1,0,0,0)
'''
def verifyLostSituation(matchsticksByLine):
	hasJustOne = 0
	lostSituation = 1
	for x in matchsticksByLine:
		if(x != 0):
			if( x == 1 and hasJustOne == 0):
				hasJustOne = 1
			else:
				lostSituation = 0
				break
	return lostSituation

'''
Limpa a tela.
'''
def cleanScreen():
	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')

'''
Realiza a jogada para o usuário.
'''
def userPlay(matchsticksByLine):
	print()
	try:
		line, matchsticks = input("Coloque a linha e a quantidade de palitos que deseja retirar respectivamente Ex.(1 1): ").split()
		line, matchsticks = int(line)-1,int(matchsticks)
		if line not in range(numLines) or matchsticks > matchsticksByLine[line]:
			raise Exception()

		matchsticksByLine[line] -= matchsticks
		return matchsticksByLine
	except Exception as e:
		print("Entrada inválida, por favor digite novamente")
		sleep(2)
		return -1

'''
Realiza a jogada do computador. Sempre a procura da jogada ganhadora,
que só será possível caso o usuário tenha feito uma jogada perdedora.
Caso não tenha jogada ganhadora, ele retira de uma linha aleatória uma
quantidade aleatória de palitos.
'''
def computerPlay(matchsticksByLine):
	print()
	print ("Minha Vez")
	sleep(2)
	line = 0
	matchsticks = 1
	matchsticksByLineWinner = []
	verifyGameSituation(matchsticksByLine)
	if (not isWinnerSituation):
		#Caso estiver em uma situação perdedoras,
		#então retira de uma linha aleatória uma quantidade aleatória de palitos.
		if (line == (numLines -1) and matchsticks >= matchsticksByLine[line] and (not matchsticksByLineWinner)):
			line = randint(0, numLines-1)

			while(matchsticksByLine[line] == 0):
				line = randint(0, numLines-1)
			matchsticks = randint(1, matchsticksByLine[line])

			matchsticksByLine[line] -= matchsticks
			return matchsticksByLine
	else:
		matchsticksByLineAux = matchsticksByLine[:]
		
		while True:
			while True:
				#Passa a linha caso ainda não tenha passado por todas as linhas, e o número
				#de palitos para retirar tenha ultrapassado a quantidade de palitos na linha
				#corrente.
				if(line < numLines-1 and matchsticksByLineAux[line] == 0):
					line += 1
					matchsticks = 1
				else:
					break
			matchsticksByLineAux = matchsticksByLine[:]
			if (line == (numLines -1) and matchsticks > matchsticksByLine[line]):
			 	return matchsticksByLineWinner
			
			matchsticksByLineAux[line] -= matchsticks

			verifyGameSituation(matchsticksByLineAux)
			#Pega o caso que tem situação ganhadora.
			if verifyLostSituation(matchsticksByLineAux):
				return matchsticksByLineAux	
			if not isWinnerSituation:
				matchsticksByLineWinner = matchsticksByLineAux
				pass
			matchsticks += 1

'''
Declara o fim da partida, anunciando quem ganhou, e perguntando para o
usuário se o mesmo deseja jogar outra partida.
'''
def endGame(msg):
	while 1:
		print()
		print(msg)
		continueGame = input("Voce quer jogar novamente?(S/N)")
		continueGame.upper()
		if continueGame == 'N' or continueGame == 'S':
			return continueGame

#Main do programa.
continueGame = 'S'
while (continueGame == 'S'):
	cleanScreen()
	#Inicialização das variáveis
	matchsticksByLine = [1, 3, 5, 7]
	isWinnerSituation = None

	printGame(matchsticksByLine, score)
	
	while ( 1 ):
		auxReturn = userPlay(matchsticksByLine)
		#Caso o usuário tenha colocado parâmetros incorretos.
		if auxReturn == -1:
			cleanScreen()
			printGame(matchsticksByLine, score)
			continue
		matchsticksByLine = auxReturn
		cleanScreen()
		printGame(matchsticksByLine, score)
		
		if verifyLostSituation(matchsticksByLine):
			continueGame = endGame("Você venceu")
			score += 1
			break


		matchsticksByLine = computerPlay(matchsticksByLine)

		cleanScreen()
		printGame(matchsticksByLine, score)
		
		if verifyLostSituation(matchsticksByLine):
			continueGame = endGame("Você Perdeu")
			score += 1
			break

print()
print("Score final de partidas: ", score)
print("Fim de Jogo!")