#!/usr/bin/env python

import pygame as pg#importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
from sys import exit #puxa a função de fechar janela do sistema
from random import randint #ajudar na aleatoriedade de colisões
import os
from button import Button #Importando classe de botões do Youtuber gringo

#pastas 
dir_main = os.path.dirname(__file__)
dir_imgs = os.path.join(dir_main, 'imgs')
dir_sons = os.path.join(dir_main, 'sons')


#constantes ou variaveis
largura = 800
altura = 600
esp_linha = 12
raio_bola=6
bolaX_start=largura/2
bolaY_start=altura/2
Vel_max=10
Vel_min=3
vX = 5
vY = 5
quadra_X=largura
quadra_Y=592

#cores
light_beje = (243,223,171)
mid_beje=(229,206,159)
dark_beje=(212,189,142)
red_line=(241,118,119)
cinza_bola=(68,70,81)
bluey=(133,200,250)
bluey_dark=(32,30,67)
branco=(255,255,255)

pg.init() # muitas funções de som, imagem e etc precisam dessa tela inicializada para serem feitas
tela = pg.display.set_mode((largura,altura)) #abre tela com formatação de tamanho
pg.display.set_caption('Bluey Squash Game') # Coloca título na tela			

#musicas e sons
default_back_song = pg.mixer.music.load(os.path.join(dir_sons,'Sportmanship.mp3')) # seleciona musica de background padrão
pg.mixer.music.play(-1)# coloca musica em loop
pg.mixer.music.set_volume(0.05)
sons_colisao = [pg.mixer.Sound(os.path.join(dir_sons,'som_bola1.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola2.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola3.wav'))]
#for i in range(3):
#	sons_colisao[i].set_volume(0.1)
som_bola = 0

#sprites e frames
sprite_bandit = pg.image.load(os.path.join(dir_imgs,'sheet_bandit.png')).convert_alpha()
sprite_stripe = pg.image.load(os.path.join(dir_imgs,'sheet_stripe.png')).convert_alpha()

class Player(pg.sprite.Sprite):
	def __init__(self,img_sheet,Px,Py,Vel):
		self.imagens_player = []  # lista de frames, vetor ainda vazio
		for i in range(4): # loop para colocar frames no vetor
			img = self.img_sheet.subsurface((i*43,0),(43,47)) # ((ponto para o corte),(dimensões de cada frame))
			self.imagens_player.append(img) 
		self.index_frame = 0 # var de controle dos frames
		self.img = self.imagens_player[self.index_frame] # sprite padrão exibida no self.img
		self.rect = self.img.get_rect() # pega o retângulo que a imagem ocupa
		self.rect.center = (self.Px,self.Py) # coloca o centro do retangulo da imagem nas posições de Px e Py
	def update(self):
		if self.index_frame > 4 :
			self.index_frame = 0 
		self.index_frame += 0.25
		self.img = self.imagens_player[int(self.index_frame)]

# a estratégia para os menus é colocar cada menu numa função cada um com seu proprio loop

def get_font(size): # função auxiliar para mudar tamanho dos textos A fonte está padronizada
    return pg.font.Font(os.path.join(dir_main,'Hello_Headline_Regular.ttf'),size)


def star_play():
	print("Bora jogar !!!")
	menu_principal()

def menu_conf():
	print("Bora configurar !!!")
	menu_principal()

def menu_principal():
	#fonte = pg.font.SysFont('Hello Headline Regular',32, True, False)
	pg.display.set_caption('Bluey Squash Game - Menu') # atualiza o nome da janela
	
	while True:
		tela.fill(bluey) # pinta tela de azul
		
		menu_mouse = pg.mouse.get_pos() # pega a posiçãod o mouse na tela de menu
		texto_menu=get_font(64).render("Menu Principal", False,branco)
		ret_menu = texto_menu.get_rect(center=(largura/2,70))
		
		bot_play = Button(image = None, pos=(largura/2, 300),text_input="Play", font=get_font(44), base_color=branco, hovering_color=bluey_dark)
		bot_conf = Button(image = None, pos=(largura/2, 350),text_input="Config", font=get_font(44), base_color=branco, hovering_color=bluey_dark)
		bot_quit = Button(image = None, pos=(largura/2, 400),text_input="Quit", font=get_font(44), base_color=red_line, hovering_color=bluey_dark)
		
		tela.blit(texto_menu,ret_menu) # até aqui ele printa o titulo do menu na tela
		
		for butao in [bot_play,bot_conf,bot_quit]:
			butao.changeColor(menu_mouse)
			butao.update(tela)
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				if bot_play.checkForInput(menu_mouse):
					star_play()
				if bot_conf.checkForInput(menu_mouse):
					menu_conf()
				if bot_quit.checkForInput(menu_mouse):
					pg.quit()
					exit()
				
				
		pg.display.flip()



menu_principal()


'''
clk = pg.time.Clock()

while True:

	tela.fill(bluey)
		
	clk.tick(50)
	tela.fill(bluey)
	#mensagem = f'Colisões: {ncolisoes}'
	#textoFormatado = fonte.render(mensagem, True, (255,255,255) )
	
	for event in pg.event.get(): # fica a espera de eventos
		if event.type == QUIT:
			pg.quit()
			exit()


	#tela.blit(textoFormatado, (0,0))

	#pygame.display.flip()
	pg.display.flip() # atualiza a tela no loop principal
'''

