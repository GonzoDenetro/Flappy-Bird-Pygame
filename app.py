import pygame


def draw_game(screen, bg, bg2, scroll):
    #Draw Background
    screen.blit(bg, [0, 0])
    screen.blit(bg2, [scroll, 504])
    
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
    background = pygame.transform.scale(pygame.image.load("./Assets/bg.png"), [screen_width, 504])
    background_floor = pygame.transform.scale(pygame.image.load("./Assets/ground.png"), [screen_width + 35, 96])
    
    
    running = True
    while running:
        #Frame Rate
        clock.tick(60)
        
        #Scroll Background
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        
        
        
        draw_game(screen, background, background_floor, ground_scroll)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    


if __name__ == '__main__':
    run()
    