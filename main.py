#!/usr/bin/env python

import pygame as pg#importa a biblioteca
from pygame.locals import * #puxa todas as funções e constantes da biblioteca
import math
#import pygame.gfxdraw # teste para novos desenhos
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
altura = 650
esp_linha = 12
raio_bola=9
bolaX_start=largura/2
bolaY_start=altura/2
Vel_max=20
Vel_min=3
vX = 5
vY = 5
scale=4
quadra_largura=largura
quadra_altura=592
clocke=30

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
pg.mixer.music.set_volume(0.5)
sons_colisao = [pg.mixer.Sound(os.path.join(dir_sons,'som_bola1.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola2.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola3.wav'))]
#for i in range(3):
#	sons_colisao[i].set_volume(0.1)
som_bola = 0

#sprites e frames
sprite_bandit = pg.image.load(os.path.join(dir_imgs,'sheet_bandit.png')).convert_alpha()
sprite_stripe = pg.image.load(os.path.join(dir_imgs,'sheet_stripe.png')).convert_alpha()

class Player(pg.sprite.Sprite): # classe de jogador
	def __init__(self,img_sheet,Px,Py,Vel,Kup,Kdown,Kleft,Kright,quadraX,quadraY,defasagem_quadraY):
		self.px = Px
		self.py = Py
		self.vel = Vel
		self.ku = Kup
		self.kd= Kdown
		self.kl = Kleft
		self.kr = Kright
		self.limiteX = quadraX
		self.limiteY = quadraY
		self.limiteY_def = defasagem_quadraY
		self.animacao = False
		pg.sprite.Sprite.__init__(self)
		self.circle_size = int(47*(scale-1.8))
		self.imagens_player = []  # lista de frames, vetor ainda vazio
		for i in range(4): # loop para colocar frames no vetor
			img = img_sheet.subsurface((i*43,0),(43,47)) # ((ponto para o corte),(dimensões de cada frame))
			self.imagens_player.append(img) 
		self.index_frame = 0 # var de controle dos frames
		self.image = self.imagens_player[int(self.index_frame)] # sprite padrão exibida no self.image
		self.image = pg.transform.scale(self.image,(43*scale, 47*scale))
		self.rect = self.image.get_rect() # pega o retângulo que a imagem ocupa
		self.rect.center = (self.px,self.py) # coloca o centro do retangulo da imagem nas posições de Px e Py e move ele pro endereço
		self.area_batida = pg.draw.circle(tela,bluey_dark,(self.px,self.py),self.circle_size, 5)
	def draw_area_bater(self):
		pg.draw.circle(tela,bluey_dark,(self.px,self.py),self.circle_size, 5)
	def update_frame(self): # deve passar quando ele bater na bola
		if self.animacao == True:
			self.index_frame += 1
			if self.index_frame >= len(self.imagens_player) :
				self.index_frame = 0 
				self.animacao = False
			self.image = self.imagens_player[int(self.index_frame)]
			self.image = pg.transform.scale(self.image,(43*scale, 47*scale))
			self.rect = self.image.get_rect() # pega o retângulo que a imagem ocupa
			self.rect.center = (self.px,self.py) # coloca o centro do retangulo da imagem nas posições de Px e Py e move ele pro endereço
	def mov(self): # vai ser ativado quando ele andar Com limitações das bordas da quadra
		if pg.key.get_pressed()[self.kr]:
			if self.px < self.limiteX - self.circle_size:
				self.px += self.vel
		if pg.key.get_pressed()[self.kl]:
			if self.px > self.circle_size:
				self.px -= self.vel
		if pg.key.get_pressed()[self.kd]:
			if self.py < self.limiteY - self.circle_size:
				self.py += self.vel
		if pg.key.get_pressed()[self.ku]:
			if self.py > (self.limiteY_def+self.circle_size):
				self.py -= self.vel
		self.draw_area_bater()
		#if pg.key.get_pressed()[K_SPACE]:
			#self.update_frame()
		self.rect.center = (self.px,self.py)
	def bater_animacao(self):
					self.animacao = True
		
		
class Bola(): 
	def __init__(self,pos,speed,raio):
		self.px = pos[0]
		self.py = pos[1]
		self.vx = speed[0]
		self.vy = speed[1]
		self.size = raio
		#self.ball = pg.draw.circle(tela,cinza_bola,(self.px,self.py),self.size )
	def draw(self):
		self.ball = pg.draw.circle(tela,cinza_bola,(self.px,self.py),self.size )
	def update(self): # atualiza a posiçãod a bola
		self.px += int(self.vx)
		self.py += int(self.vy)
	def newSpeed(self,speed): # quero usar para mudar a velocidade quando bater num jogador
		self.vx = speed[0]#deletar depois e reescrever, ou não, sei lá
		self.vy = speed[1]
	def newPos(self): # quero usar pra acompanhar o jogador antes do saque
			self.px += self.vx #deletar depois e reescrever
			self.py += self.vy
	def colisao_bola(self):
		if self.px <= raio_bola: # bateu na esquerda Vx é - -> +
			self.px = raio_bola+1
			self.vx += 2
			self.vx = -self.vx
			if abs(self.vx) < Vel_min :
				self.vx = Vel_min
			if self.vy < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vy += 2
				if abs(self.vy) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vy = -Vel_min
			else: # se for positivo ele tira 2
				self.vy -= 2
				if abs(self.vy) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vy = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.px >= (quadra_largura - raio_bola): # bateu na direita
			self.px = (quadra_largura - raio_bola)+1
			self.vx -= 2
			self.vx = -self.vx
			if abs(self.vx) < Vel_min :
				self.vx = -Vel_min
			if self.vy < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vy += 2
				if abs(self.vy) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vy = -Vel_min
			else: # se for positivo ele tira 2
				self.vy -= 2
				if abs(self.vy) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vy = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.py <= (altura-quadra_altura + raio_bola): #bateu no teto
			self.py = (altura-quadra_altura + raio_bola) +1
			self.vy += 2
			self.vy = -self.vy
			if abs(self.vy) < Vel_min :
				self.vy = Vel_min
			if self.vx < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vx += 2
				if abs(self.vx) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vx = -Vel_min
			else: # se for positivo ele tira 2
				self.vx -= 2
				if abs(self.vx) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vx = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.py >= altura - raio_bola :# bateu no chão
			self.py = (altura - raio_bola) +1
			self.vy -= 2
			self.vy = -self.vy
			if abs(self.vy) < Vel_min :
				self.vy = -Vel_min
				
			if self.vx < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vx += 2
				if abs(self.vx) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vx = -Vel_min
			else: # se for positivo ele tira 2
				self.vx -= 2
				if abs(self.vx) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vx = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
#desenhar a quadra
def desenhar_quadra():
	pg.draw.rect(tela,mid_beje,(0,(altura-quadra_altura),quadra_largura,quadra_altura)) #quadra maior (onde, (cor em RGB), (addrX, addrY, sizeX,sizeY))
	pg.draw.line(tela,red_line,(383, altura-592),(383,altura), esp_linha)#(onde, (cor em RGB), addrXYinicio, addrXYfinal, espessura) 
	pg.draw.line(tela,red_line,(383, altura-(592/2)),(largura,altura-(592/2)), esp_linha) # linha do meio
	pg.draw.line(tela,red_line,(383, 58+174),(383+192,58+174), esp_linha)#linha horizontal superior
	pg.draw.line(tela,red_line,(383+192-6, 58),(383+192-6,58+174), esp_linha)#linha vertical sup
	pg.draw.line(tela,red_line,(383, altura-174),(383+192,altura-174), esp_linha)#linha horizontal inferior
	pg.draw.line(tela,red_line,(383+192-6, altura),(383+192-6,altura-174), esp_linha)#linha vertical inferior

# para se fazer colisões de circulos eu vou ter que fazer uma função própria
# já que o pygame só reconhece colisões com base em retângulos e todo desenho ele encaixa em um retângulo

def circle_colision(ponto1,raio1,ponto2,raio2): # função para checar colisões entre círculos
	if math.sqrt( pow(ponto1[0] - ponto2[0], 2) + pow(ponto1[1] - ponto2[1], 2) ) < (raio1+raio2):
		return True
	else:
		return False


# a estratégia para os menus é colocar cada menu numa função cada um com seu proprio loop

def get_font(size): # função auxiliar para mudar tamanho dos textos A fonte está padronizada
    return pg.font.Font(os.path.join(dir_main,'Hello_Headline_Regular.ttf'),size)


def star_play():
	pg.display.set_caption('Bluey Squash Game - Playing') # atualiza o nome da janela
	clk = pg.time.Clock()
	
	bola = Bola((383,altura-(592/2)),(-Vel_max,-Vel_max),raio_bola)
	bola1 = pg.draw.circle(tela,red_line,(200,200),50 )
	bola2 = pg.draw.circle(tela,bluey_dark,(100,100),30 )
#para as sprites funcionarem vc precisa adicionar elas
	todas_as_sprites = pg.sprite.Group()
	player1 = Player(sprite_bandit,600,450,Vel_max,K_w,K_s,K_a,K_d,largura,altura,altura-quadra_altura)# up down left rigth
	player2 = Player(sprite_stripe,600,300,Vel_max,K_i,K_k,K_j,K_l,largura,altura,altura-quadra_altura)
	todas_as_sprites.add(player1)
	todas_as_sprites.add(player2)
	
	player_da_vez = player1 # variavel que marca player que inicia o jogo
	
	while True:
		tela.fill(bluey) # pinta tela de azul
		clk.tick(clocke)
		desenhar_quadra()
		bola.draw()
		#bola1 = pg.draw.circle(tela,red_line,(200,200),50 )
		#bola2 = pg.draw.circle(tela,bluey_dark,(100,100),30 )
		if circle_colision((bola.px,bola.py),bola.size,(player1.px,player1.py),player1.circle_size ):
			print("bola está na área de acerto")
		else:
			print("não bateu ainda")
		#print(bola.vx,bola.vy,bola.px,bola.py)
		bola.update()
		bola.colisao_bola()
		#if bola.ball.pg.collide_circle(player1.area_batida):
		#	print("bola está na área de acerto")
		
		todas_as_sprites.draw(tela) #desenha todas as sprites armazenadas na Tela
		
		player1.mov()
		player2.mov()
		#player1.draw_area_bater()
		player1.update_frame()
		player2.update_frame()
		todas_as_sprites.update()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_c:
					player1.bater_animacao() #só vai checar a colisão se o jogador apertar o botão, se não a bola passa por ele
					if circle_colision((bola.px,bola.py),bola.size,(player1.px,player1.py),player1.circle_size ):
						bola.newSpeed((-Vel_max,-Vel_max))
				if event.key == K_n:
					player2.bater_animacao()
					if circle_colision((bola.px,bola.py),bola.size,(player2.px,player2.py),player2.circle_size ):
						bola.newSpeed((-Vel_max,-Vel_max))
		pg.display.flip()

def menu_conf():
	pg.display.set_caption('Bluey Squash Game - Configurations') # atualiza o nome da janela
	
	while True:
		tela.fill(bluey) # pinta tela de azul
		
		conf_mouse = pg.mouse.get_pos() # pega a posiçãod o mouse na tela de menu
		texto_conf=get_font(64).render("Configurations", False,branco)
		ret_conf = texto_conf.get_rect(center=(largura/2,70))
		
		bot_change_player = Button(image = None, pos=(largura/2, 300),text_input="Change Skin", font=get_font(44), base_color=branco, hovering_color=bluey_dark)
		bot_back = Button(image = None, pos=(largura/2, 350),text_input="Back", font=get_font(44), base_color=branco, hovering_color=bluey_dark)
		bot_quit = Button(image = None, pos=(largura/2, 400),text_input="Quit", font=get_font(44), base_color=red_line, hovering_color=bluey_dark)
		
		tela.blit(texto_conf,ret_conf) # até aqui ele printa o titulo do menu na tela
		
		for butao in [bot_change_player,bot_back,bot_quit]:
			butao.changeColor(conf_mouse)
			butao.update(tela)
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				if bot_change_player.checkForInput(conf_mouse):
					#star_play() mudar para função de trocar skin padrão
					pass
				if bot_back.checkForInput(conf_mouse):
					menu_principal()
				if bot_quit.checkForInput(conf_mouse):
					pg.quit()
					exit()
				
		pg.display.flip()

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



#menu_principal()
star_play()

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

