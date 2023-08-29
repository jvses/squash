import pygame #importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
from sys import exit #puxa a função de fechar janela do sistema

pygame.init()

#constantes ou variaveis
largura = 900
altura = 650
esp_linha = 12
raio_bola=9
baddrx=450
baddry=354


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
	pygame.draw.line(tela,red_line,(383+100, altura-592),(383+100,altura), esp_linha)#(onde, (cor em RGB), addrXYinicio, addrXYfinal, espessura) 
	pygame.draw.line(tela,red_line,(383+100, 650-(592/2)),(largura-50,650-(592/2)), esp_linha)
	pygame.draw.line(tela,red_line,(383+100, 58+174),(383+100+192,58+174), esp_linha)#linha horizontal superior
	pygame.draw.line(tela,red_line,(383+100+192-6, 58),(383+100+192-6,58+174), esp_linha)#linha vertical sup
	pygame.draw.line(tela,red_line,(383+100, altura-174),(383+100+192,altura-174), esp_linha)#linha horizontal inferior
	pygame.draw.line(tela,red_line,(383+100+192-6, altura),(383+100+192-6,altura-174), esp_linha)#linha vertical inferior
	
def desenhar_bola(Px,Py):
	pygame.draw.circle(tela,cinza_bola, (Px,Py), 9) #(onde, (cor em RGB), (addrX, addrY), raio)


while True: # loop principal
	for event in pygame.event.get(): # fica a espera de eventos
		if event.type == QUIT:
			pygame.quit()
			exit()
	desenhar_quadra()
	desenhar_bola(baddrx,baddry)
	pygame.display.update() # atualiza a tela no loop principal
	

