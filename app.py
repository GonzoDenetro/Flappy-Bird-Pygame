import pygame


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
        self.cooldown = 5
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #Hacemos un rectángulo de nuestra imágen.
        self.rect.center = [x, y] #Le damos su posición
        
    def animation(self):
        self.counter += 1
        #Hacemos un cooldown antes de cambiar de imagen
        if self.counter > self.cooldown:
            self.counter = 0
            self.index += 1 #Aumentamos nuestro índice para recorrer las imágenes
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


def draw_game(screen, bg, bg2, scroll, bird_arr, bird):
    #Draw Background
    screen.blit(bg, [0, 0])
    screen.blit(bg2, [scroll, 504])
    
    bird.animation()
    bird_arr.draw(screen) #Dibujamos a nuestro pajaro, el método drwa() lo heredamos de Sprite
    
    pygame.display.update()


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
    
    #Load Images
    background = pygame.transform.scale(pygame.image.load("./Assets/Bckground/bg.png"), [screen_width, 504])
    background_floor = pygame.transform.scale(pygame.image.load("./Assets/Bckground/ground.png"), [screen_width + 35, 96])
    
    
    bird_group = pygame.sprite.Group() #Creamos un grupo para nuestros sprites
    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy) #Agregamos a nuestro grupo
    
    running = True
    while running:
        #Frame Rate
        clock.tick(60)
        
        #Scroll Background
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        

        draw_game(screen, background, background_floor, ground_scroll, bird_group, flappy)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    


if __name__ == '__main__':
    run()
    