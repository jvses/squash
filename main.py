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
Vel_max=23
Vel_Padrao = 20
Vel_passo = 10
Vel_min=3
vX = 5
vY = 5
scale=4
v_atrito=2
quadra_largura=largura
quadra_altura=592
default_pos1=(600,255)
default_pos2=(600,453)
clocke=60

#cores
light_beje = (243,223,171)
mid_beje=(229,206,159)
dark_beje=(212,189,142)
red_line=(241,118,119)
cinza_bola=(68,70,81)
bluey=(133,200,250)
bluey_dark=(32,30,67)
branco=(255,255,255)
green_light=(199,227,82)
green_cyan=(65,155,156)
green_dark=(66,119,150)

pg.init() # muitas funções de som, imagem e etc precisam dessa tela inicializada para serem feitas
tela = pg.display.set_mode((largura,altura)) #abre tela com formatação de tamanho
pg.display.set_caption('Bluey Squash Game') # Coloca título na tela			

#musicas e sons
default_back_song = pg.mixer.music.load(os.path.join(dir_sons,'Sportmanship.mp3')) # seleciona musica de background padrão
pg.mixer.music.play(-1)# coloca musica em loop
pg.mixer.music.set_volume(0.5)
sons_colisao = [pg.mixer.Sound(os.path.join(dir_sons,'som_bola1.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola2.wav')), pg.mixer.Sound(os.path.join(dir_sons,'som_bola3.wav'))]
for i in range(3):
	sons_colisao[i].set_volume(0.1)
som_bola = 0

#Flags de configuração
hit_area_visible = True
pause = False #autoexplicativo



#sprites e frames
sprite_bandit = pg.image.load(os.path.join(dir_imgs,'sheet_bandit.png')).convert_alpha()
sprite_stripe = pg.image.load(os.path.join(dir_imgs,'sheet_stripe.png')).convert_alpha()
#preparando sistema de skins
sprite_p1 = sprite_bandit #skin p1 recebe o bandit por padrão
sprite_p2 = sprite_stripe #skin p2 recebe o stripe por padrão

class Player(pg.sprite.Sprite): # classe de jogador
	def __init__(self,img_sheet,Pos,Vel,Kup,Kdown,Kleft,Kright,quadraX,quadraY,defasagem_quadraY,auxAreaFlag):
		self.px = Pos[0]
		self.py = Pos[1]
		self.vel = Vel
		self.ku = Kup
		self.kd= Kdown
		self.kl = Kleft
		self.kr = Kright
		self.limiteX = quadraX
		self.limiteY = quadraY
		self.limiteY_def = defasagem_quadraY
		self.animacao = False
		self.aux_area_flag = auxAreaFlag
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
		self.area_batida = pg.draw.circle(tela,bluey_dark,(self.px,self.py),self.circle_size, 2)
	def draw_area_bater(self):
		if self.aux_area_flag:
			pg.draw.circle(tela,bluey_dark,(self.px,self.py),self.circle_size, 2)
	def update_frame(self): # deve passar quando ele bater na bola
		if self.animacao == True:
			self.index_frame += 0.5
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
	def newSpeed(self,speed,theta): # quero usar para mudar a velocidade quando bater num jogador
		self.vx = -speed*math.cos(theta)#deletar depois e reescrever, ou não, sei lá
		self.vy = -speed*math.sin(theta)
	def newPos(self,Pos): # quero usar pra acompanhar o jogador antes do saque
			self.px = Pos[0] - 30 # coloquei uma diferença em relação a entrada para poder sacar sem estar reto
			self.py = Pos[1] + 60 # vou usar isso no sistema de saques
	def colisao_bola(self):
		if self.px <= raio_bola: # bateu na esquerda Vx é - -> +
			self.px = raio_bola+1
			self.vx += v_atrito
			self.vx = -self.vx
			if abs(self.vx) < Vel_min :
				self.vx = Vel_min
			if self.vy < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vy += v_atrito
				if abs(self.vy) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vy = -Vel_min
			else: # se for positivo ele tira 2
				self.vy -= v_atrito
				if abs(self.vy) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vy = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.px >= (quadra_largura - raio_bola): # bateu na direita
			self.px = (quadra_largura - raio_bola)+1
			self.vx -= v_atrito
			self.vx = -self.vx
			if abs(self.vx) < Vel_min :
				self.vx = -Vel_min
			if self.vy < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vy += v_atrito
				if abs(self.vy) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vy = -Vel_min
			else: # se for positivo ele tira 2
				self.vy -= v_atrito
				if abs(self.vy) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vy = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.py <= (altura-quadra_altura + raio_bola): #bateu no teto
			self.py = (altura-quadra_altura + raio_bola) +1
			self.vy += v_atrito
			self.vy = -self.vy
			if abs(self.vy) < Vel_min :
				self.vy = Vel_min
			if self.vx < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vx += v_atrito
				if abs(self.vx) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vx = -Vel_min
			else: # se for positivo ele tira 2
				self.vx -= v_atrito
				if abs(self.vx) < Vel_min:# se modulo menor que 2 ele mantêm em 2
					self.vx = Vel_min  # após colidir a bola perde velocidade em ambas dimensões e então é invertida de acordo com o eixo que bateu
		if self.py >= altura - raio_bola :# bateu no chão
			self.py = (altura - raio_bola) +1
			self.vy -= v_atrito
			self.vy = -self.vy
			if abs(self.vy) < Vel_min :
				self.vy = -Vel_min
				
			if self.vx < 0: # se o vx é negativa ele diminui o modulo em 2
				self.vx += v_atrito
				if abs(self.vx) < Vel_min: # se o modulo for menor que 2 ele mantem e -2
					self.vx = -Vel_min
			else: # se for positivo ele tira 2
				self.vx -= v_atrito
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
	
	# linhas auxiliares
	#linha auxiliar pra determinar a pontuação. se a bola passar dela tem que dar um ponto pro ultimo jogador que bateu nela 
	pg.draw.line(tela,branco,(largura-60,altura-quadra_altura),(largura-60,altura),2)

# para se fazer colisões de circulos eu vou ter que fazer uma função própria
# já que o pygame só reconhece colisões com base em retângulos e todo desenho ele encaixa em um retângulo

def circle_colision(ponto1,raio1,ponto2,raio2): # função para checar colisões entre círculos
	if math.sqrt( pow(ponto1[0] - ponto2[0], 2) + pow(ponto1[1] - ponto2[1], 2) ) < (raio1+raio2):
		return True
	else:
		return False

def get_angle(ponto1,ponto2):
	dx = ponto1[0]-ponto2[0]
	dy = ponto1[1]-ponto2[1]
	if dx == 0:
		dx = 0.001
	# para evitar quicar demais no eixo Y eu vou limitar o angulo para no máximo 60º
	teta = math.atan(dy/dx)*180/math.pi
	if teta < -60:
		teta = -60*math.pi/180
	elif teta > 60:
		teta = 60*math.pi/180
	else:
		teta = math.atan(dy/dx)
	return teta
	

# a estratégia para os menus é colocar cada menu numa função cada um com seu proprio loop

def get_font(size): # função auxiliar para mudar tamanho dos textos A fonte está padronizada
    return pg.font.Font(os.path.join(dir_main,'Hello_Headline_Regular.ttf'),size)
'''Loop de pausas'''
def menu_pausa():
	global pause
	pg.display.set_caption('Bluey Squash Game - Paused') # atualiza o nome da janela
	#tela.fill(bluey) # pinta tela de azul
	
	pause_mouse = pg.mouse.get_pos() # pega a posiçãod o mouse na tela de menu
	texto_pause=get_font(64).render("Paused", False,green_dark)
	ret_pause = texto_pause.get_rect(center=(largura/2,70))
		
	bot_resume = Button(image = None, pos=(largura/2, 300),text_input="Resume", font=get_font(44), base_color=green_cyan, hovering_color=green_dark)
	bot_back_menu = Button(image = None, pos=(largura/2, 350),text_input="Main Menu", font=get_font(44), base_color=green_cyan, hovering_color=green_dark)
	bot_quit = Button(image = None, pos=(largura/2, 400),text_input="Quit Game", font=get_font(44), base_color=green_cyan, hovering_color=green_dark)
		
	tela.blit(texto_pause,ret_pause) # até aqui ele printa o titulo do menu na tela
				
	for butao in [bot_resume,bot_back_menu,bot_quit]:
		butao.changeColor(pause_mouse)
		butao.update(tela)
		
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()
		if event.type == pg.MOUSEBUTTONDOWN:
			if bot_resume.checkForInput(pause_mouse):
				pause = False
				#star_play() mudar para função de trocar skin padrão
			if bot_back_menu.checkForInput(pause_mouse):
				pause = False
				menu_principal()
			if bot_quit.checkForInput(pause_mouse):
				pg.quit()
				exit()
				
	pg.display.flip()


'''Loop das partidas'''
def star_play():
	global pause

	#Flags durante o jogo (talvez eu leve elas para a função de play
	hit_primeiro = False # auxiliar de início de partida
	hit_loss = False # avisa a perda da bola e marcação de pontos 

	
	
	
	pg.display.set_caption('Bluey Squash Game - Playing') # atualiza o nome da janela
	clk = pg.time.Clock()
	
	bola = Bola((383,altura-(592/2)),(-Vel_max,-Vel_max),raio_bola)

#para as sprites funcionarem vc precisa adicionar elas
	todas_as_sprites = pg.sprite.Group()
	player1 = Player(sprite_p1,default_pos1,Vel_passo,K_w,K_s,K_a,K_d,largura,altura,altura-quadra_altura,hit_area_visible)# up down left rigth
	player2 = Player(sprite_p2,default_pos2,Vel_passo,K_UP,K_DOWN,K_LEFT,K_RIGHT,largura,altura,altura-quadra_altura,hit_area_visible)
	todas_as_sprites.add(player1)
	todas_as_sprites.add(player2)
	# dados dos players
	pontos_p1 = 0
	pontos_p2 = 0
	player_da_vez = player1 # variavel que marca player que inicia o jogo
	hit_last_player = player2 # marca o ultimo player que bateu na bola
	
	while True:
		tela.fill(bluey) # pinta tela de azul
		clk.tick(clocke/2)
		desenhar_quadra()
		texto_play=get_font(40).render(f'Score \t Bandit:{pontos_p1} \t Stripe:{pontos_p2}', False,branco)
		ret_play = texto_play.get_rect(center=(largura/2,25))
		tela.blit(texto_play,ret_play)
	
		if hit_primeiro: # se a primero lance já tiver sido feito ele atualiza a bola
			bola.update()
		else: # se não ela va acompanhar o player da vez
			bola.newPos((player_da_vez.px,player_da_vez.py))
			
		if bola.px >= (largura-60): # se a bola passar do limite da linha branca um ponto é acrescentado pro ultimo que bateu
			if hit_last_player == player1: # reconhece o ultimo que bateu
				pontos_p1 += 1 # dá um ponto pra ele
				hit_primeiro = False # altera flag de novo início de partida
				player_da_vez = player1 #atualiza o player que vai dar início a nova partida
				hit_last_player = player2	
			elif hit_last_player == player2:
				pontos_p2 += 1
				hit_primeiro = False
				player_da_vez = player2
				hit_last_player = player1
				
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
		bola.draw()
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					if not hit_primeiro:
						hit_primeiro = True
					player1.bater_animacao() #só vai checar a colisão se o jogador apertar o botão, se não a bola passa por ele
					if circle_colision((bola.px,bola.py),bola.size,(player1.px,player1.py),player1.circle_size):
						if hit_last_player == player2:
							teta = get_angle((bola.px,bola.py),(player1.px,player1.py))
							bola.newSpeed(Vel_Padrao,teta)
							hit_last_player = player1
						else:# se não ele dá um ponto pro outro e vai iniciar a partida nova
							pontos_p2 += 1
							player_da_vez = player2
							hit_primeiro = False
				if event.key == K_RETURN:
					if not hit_primeiro:
						hit_primeiro = True
					player2.bater_animacao()
					if circle_colision((bola.px,bola.py),bola.size,(player2.px,player2.py),player2.circle_size ):
						if hit_last_player == player1: # se o ultimo a bater foi o outro player então funciona normal
							teta = get_angle((bola.px,bola.py),(player2.px,player2.py))
							bola.newSpeed(Vel_Padrao,teta)
							hit_last_player = player2 # ataliza a info do ultimo qu bateu na bola
						else:# se não ele dá um ponto pro outro e vai iniciar a partida nova
							pontos_p1 += 1
							player_da_vez = player1
							hit_primeiro = False
				if event.key == K_ESCAPE:
					pause= True
					
			
			while pause:
				menu_pausa()
				
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



menu_principal()
#star_play()

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

