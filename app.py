import pygame
import random


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Heredamos funcionalidades de la clase Sprite
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load("./Assets/Player/bird1.png"),
            pygame.image.load("./Assets/Player/bird2.png"),
            pygame.image.load("./Assets/Player/bird3.png")
        ]
        self.counter = 0
        self.index = 0
        self.cooldown = 6
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #Hacemos un rectángulo de nuestra imágen.
        self.rect.center = [x, y] #Le damos su posición
        self.velocity_y = 0
        self.flying = False
        self.game_over = False
        
    def animation(self):
        self.movement()
        if self.game_over == False:
            self.counter += 1
            #Hacemos un cooldown antes de cambiar de imagen
            if self.counter > self.cooldown:
                self.counter = 0
                self.index += 1 #Aumentamos nuestro índice para recorrer las imágenes
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            
            #Rotamos la imagen cuandi este de caída
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity_y * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
    
    def movement(self):
        #En nuestro pajara tenemos dos fuerzas que están actuando,
        #Una es la gravedad que esta actuando constantemente.
        #En cada iteración la velocidad con la que cae va aumentando
       #Gravity
       if self.flying:
        self.velocity_y += 0.5
        if self.velocity_y > 8:
            self.velocity_y = 0    
        
        #Jump
        #Mientras sea menor el valor "y" del pajaro a 504 ira aumentado en "y"
        if self.rect.bottom < 504: 
            self.rect.y += int(self.velocity_y) 
       
       if not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.rect.y > 0:
                    self.rect.y -= 10
                    #print("AARINNA")


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./Assets/pipe.png')
        self.rect = self.image.get_rect()
        pipe_gap = 150
        #if posisiotn  1  is from the top, -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    
    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x < -80:
            self.kill()


class Button:
    def __init__(self, x, y):
        self.image = pygame.image.load("./Assets/restart.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.clicked = False
    
    def draw(self, screen):
        #Drawe buton
        screen.blit(self.image, [self.rect.x , self.rect.y])

    def click(self):
        #Get mouse position
        position = pygame.mouse.get_pos()
        
        #Check if the mouse is over the button
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                print("jjjjjjjjjjjjj")
            else:
                self.cliked = False
        return self.clicked


def draw_text(text, width, screen):
    font = pygame.font.SysFont("Bauhaus 93", 60)
    texto = font.render(str(text), True, (255, 255, 255))
    textRect = texto.get_rect()
    textRect.center = (width//2, 40)
    screen.blit(texto, textRect)


def draw_game(screen, bg, bg2, scroll, bird_arr, bird, pipe_group, score, width, button):
    #Draw Background
    screen.blit(bg, [0, 0])
    #Draw Pipe
    pipe_group.draw(screen)
    #Draw scrolling background of the floor
    screen.blit(bg2, [scroll, 504])
    
    bird.animation()
    bird_arr.draw(screen) #Dibujamos a nuestro pajaro, el método drwa() lo heredamos de Sprite

    draw_text(score, width, screen)
    if bird.game_over:
        button.draw(screen)
    pygame.display.update()
    
    
def reset_game(pipe_group, bird, height):
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = height // 2


def run():
    pygame.init()
    
    #FPS
    clock = pygame.time.Clock()
    FPS = 60
    
    #Screen set up
    screen_width = 664
    screen_height = 600
    
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption(("Flappy Bird"))
    
    #Game Variables
    scroll_speed = 4
    ground_scroll = 0
    pipe_frecuency = 1500 #Milisegundos
    last_pipe = pygame.time.get_ticks() - pipe_frecuency
    score = 0
    pass_pipe = False
    
    #Load Images
    background = pygame.transform.scale(pygame.image.load("./Assets/Bckground/bg.png"), [screen_width, 504])
    background_floor = pygame.transform.scale(pygame.image.load("./Assets/Bckground/ground.png"), [screen_width + 35, 96])
    
    bird_group = pygame.sprite.Group() #Creamos un grupo para nuestros sprites
    pipe_group = pygame.sprite.Group() #Grupo para nuestros Pipes
    
    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy) #Agregamos a nuestro grupo
    
    button = Button(screen_width // 2, screen_height // 2)
    
    running = True
    while running:
        #Frame Rate
        clock.tick(FPS)
        
        #Scroll Background
        if not flappy.game_over and flappy.flying == True:
            
            #Collision
            if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
                flappy.game_over = True
            
            #Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frecuency:
                pipe_height = random.randint(-100, 100)
                bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height /2) + pipe_height, 1)
                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
                #print(len(pipe_group))
            
            #Score
            #Para checar si ya paso el pipe vamos a checar primero si el lado izquierdo de nuestro pajaro
            #paso el lado izquierdo del pipe, y luego checamos que el lado izquierdo del pajaro haya pasado
            #el lado derecho del pipe
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			    and pass_pipe == False:
                    pass_pipe = True
                
                if pass_pipe == True:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        score += 1
                        pass_pipe = False
            print(score)
            
            #Si el juego llega estar en game over ya no habra scroll
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            
            pipe_group.update(scroll_speed)
            #print(len(pipe_group))
            
            #Game Over
            if flappy.rect.bottom >= 504:
                flappy.game_over = True
                flappy.flying = False
                
        elif flappy.game_over == True:
            if button.click():
                reset_game(pipe_group, flappy, screen_height)
                score = 0
                flappy.game_over = False
    
        draw_game(screen, background, background_floor, ground_scroll, bird_group, flappy, pipe_group, score, screen_width, button)
        
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #JUMP
            elif event.type == pygame.KEYDOWN and not flappy.game_over:
                if event.key == pygame.K_SPACE:
                    flappy.movement()
                    flappy.flying = True
    
    pygame.quit()
    


if __name__ == '__main__':
    run()
    