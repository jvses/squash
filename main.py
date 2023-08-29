import pygame #importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
from sys import exit #puxa a função de fechar janela do sistema

pygame.init()

largura = 900
altura = 650

tela = pygame.display.set_mode((largura,altura)) #abre tela com formatação de tamanho
pygame.display.set_caption('Bluey Squash Game') # Coloca título na tela

#cores
light_beje = (243,223,171)
mid_beje=(229,206,159)
dark_beje=(212,189,142)
red_line=(241,118,119)
cinza_bola=(68,70,81)

#funções para desenhar
def desenhar_quadra():
	pygame.draw.rect(tela,mid_beje,(((largura-800)/2),(altura-592),800,592)) #(onde, (cor em RGB), (addrX, addrY, sizeX,sizeY))
	pygame.draw.line(tela,red_line,(383+100, altura-592),(383+100,altura), 12)

def desenhar_bola(Px,Py):
	pygame.draw.circle(tela,cinza_bola, (Px,Py), 9) #(onde, (cor em RGB), (addrX, addrY), raio)


while True: # loop principal
	for event in pygame.event.get(): # fica a espera de eventos
		if event.type == QUIT:
			pygame.quit()
			exit()
	desenhar_quadra()
	desenhar_bola(450,354)
	pygame.display.update() # atualiza a tela no loop principal
	

