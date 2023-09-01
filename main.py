#!/usr/bin/env python

import pygame #importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
from sys import exit #puxa a função de fechar janela do sistema
from random import randint #ajudar na aleatoriedade de colisões
import os

dir_main = os.path.dirname(__file__)
dir_imgs = os.path.dirname(dir_main, 'imgs')
dir_sons = os.path.dirname(dir_main, 'sons')

sprites_bandit = pygame.image.load(os.path.join(dir_imgs,sheet_bandit.png))
sprites_stripe = pygame.image.load(os.path.join(dir_imgs,sheet_stripe.png))

pygame.init()

class Player(pygame.sprite.Sprite): # o player vai ter sprites e outras coisas
	def __init__(self, px,py,hit):
		pygame.sprite.Sprite.__init__(self)
		self.px=px
		self.py=py
		self.hit=hit
	def mov(self,px,py):
			if pygame.key.get_pressed()[K_d]:
				px = px + 5
			if pygame.key.get_pressed()[K_a]:
				px = px - 5
			if pygame.key.get_pressed()[K_s]:
				py = py + 5
			if pygame.key.get_pressed()[K_w]:
				py = py - 5
		

#constantes ou variaveis
largura = 900
altura = 650
esp_linha = 12
raio_bola=9
baddrx=450
baddry=354
movX = 5
movY = 5
ncolisoes = 0
aux_coli = 0

#musicas e sons
default_back_song = pygame.mixer.music.load('Sportmanship.mp3') # seleciona musica de background padrão
pygame.mixer.music.play(-1)# coloca musica em loop
pygame.mixer.music.set_volume(0.05)
sons_colisao = [pygame.mixer.Sound('som_bola1.wav'), pygame.mixer.Sound('som_bola2.wav'), pygame.mixer.Sound('som_bola3.wav')]
for i in range(3):
	sons_colisao[i].set_volume(0.1)
som_bola = 0

#variaveis de texto
fonte = pygame.font.SysFont('Hello Headline Regular',32, True, False)
fonte2 = pygame.font.SysFont('Hello Headline Regular',40, False, False)
mensagens = ['Play', 'Quit', 'Change Caracter', 'Multiplayer', 'Yes', 'No', 'Game Over,', ' Press any Key to restart', 'Press ESC to back do Menu Screen']

#Flags do jogo
menu = True



tela = pygame.display.set_mode((largura,altura)) #abre tela com formatação de tamanho
pygame.display.set_caption('Bluey Squash Game') # Coloca título na tela

#cores
light_beje = (243,223,171)
mid_beje=(229,206,159)
dark_beje=(212,189,142)
red_line=(241,118,119)
cinza_bola=(68,70,81)
bluey=(133,200,250)

#funções para desenhar
def desenhar_quadra():
	pygame.draw.rect(tela,mid_beje,(((largura-800)/2),(altura-592),800,592)) #quadra maior (onde, (cor em RGB), (addrX, addrY, sizeX,sizeY))
	pygame.draw.line(tela,red_line,(383+100, altura-592),(383+100,altura), esp_linha)#(onde, (cor em RGB), addrXYinicio, addrXYfinal, espessura) 
	pygame.draw.line(tela,red_line,(383+100, 650-(592/2)),(largura-50,650-(592/2)), esp_linha)
	pygame.draw.line(tela,red_line,(383+100, 58+174),(383+100+192,58+174), esp_linha)#linha horizontal superior
	pygame.draw.line(tela,red_line,(383+100+192-6, 58),(383+100+192-6,58+174), esp_linha)#linha vertical sup
	pygame.draw.line(tela,red_line,(383+100, altura-174),(383+100+192,altura-174), esp_linha)#linha horizontal inferior
	pygame.draw.line(tela,red_line,(383+100+192-6, altura),(383+100+192-6,altura-174), esp_linha)#linha vertical inferior
	
def tela_menu(): 
	pygame.draw.rect(tela,cinza_bola,(50,25,800,600),3)
	
def desenhar_bola(Px,Py):
	bola = pygame.draw.circle(tela,cinza_bola, (Px,Py), 9) #(onde, (cor em RGB), (addrX, addrY), raio)
	
def colisao_bola(baddrx,movX,baddry,movY,ncolisoes):
	if baddrx < 50+6:
		movX = 5
		ncolisoes = ncolisoes + 1
	if baddrx > (850 - 6):
		movX = -5
		ncolisoes = ncolisoes + 1   
	if baddry < (altura-592+6):
		movY = 5
		ncolisoes = ncolisoes + 1
	if baddry > altura - 6:
		movY = -5
		ncolisoes = ncolisoes + 1
	return baddrx,movX,baddry,movY,ncolisoes
		
clk = pygame.time.Clock()


while True: # loop principal
	tela.fill(bluey)
	while menu:
		#tela.fill(bluey)
		tela_menu()
		textoFormatado = fonte.render(mensagens[0], True, (255,255,255) )
		
	clk.tick(50)
	tela.fill(bluey)
	mensagem = f'Colisões: {ncolisoes}'
	textoFormatado = fonte.render(mensagem, True, (255,255,255) )
	
	for event in pygame.event.get(): # fica a espera de eventos
		if event.type == QUIT:
			pygame.quit()
			exit()
			'''
		if event.type == KEYDOWN:
			if event.key == K_d:
				baddrx = baddrx + 5
			if event.key == K_a:    # esses eventos não se repetem com o botão continuamente pressionado
				baddrx = baddrx - 5
			if event.key == K_s:
				baddry = baddry + 5
			if event.key == K_w:
				baddry = baddry - 5'''   
				
	if pygame.key.get_pressed()[K_d]:
		baddrx = baddrx + 5
	if pygame.key.get_pressed()[K_a]:
		baddrx = baddrx - 5
	if pygame.key.get_pressed()[K_s]:
		baddry = baddry + 5
	if pygame.key.get_pressed()[K_w]:
		baddry = baddry - 5
		
	desenhar_quadra()

#	colisao_bola(baddrx,movX,baddry,movY,ncolisoes)
	baddrx,movX,baddry,movY,ncolisoes = colisao_bola(baddrx,movX,baddry,movY,ncolisoes)
	if aux_coli != ncolisoes:
		if som_bola >= 3:
			som_bola = 0
		sons_colisao[som_bola].play()
		aux_coli = ncolisoes
		som_bola = som_bola + 1
	baddrx = baddrx + movX
	baddry = baddry + movY
	
	desenhar_bola(baddrx,baddry)
	#print(baddrx,movX,baddry,movY)
	tela.blit(textoFormatado, (0,0))

	#pygame.display.flip()
	pygame.display.flip() # atualiza a tela no loop principal
	

