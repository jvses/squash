import pygame #importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
from sys import exit #puxa a função de fechar janela do sistema

pygame.init()

largura = 900
altura = 650

tela = pygame.display.set_mode((largura,altura)) #abre tela com formatação de tamanho
pygame.display.set_caption('Bluey Squash Game') # Coloca título na tela

while True: # loop principal
	for event in pygame.event.get(): # fica a espera de eventos
		if event.type == QUIT:
			pygame.quit()
			exit()
	pygame.display.update() # atualiza a tela no loop principal
	

