#Módulos permitidos paro o teste
import pgzrun
import random
from pygame import Rect

#Variaveis de ajustes iniciais
WIDTH, HEIGHT = 800, 600
BROWN = (111, 66, 27)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = -12
INITIAL_ENEMY_VELOCITY = 4
MAX_ENEMY_VELOCITY = 8
LAYER_SPEEDS = [0.5, 0.5, 0.5, 1.0]
LAYER_IMAGES = [f"layer{i+1}" for i in range(4)]

# Variáveis globais do jogo
score = 0
game_over = False
menu = True
music_on = True
blink_time = 0
show_text = True
death_sound = False
music.play("gatonafloresta")

# Configuração dos frames para parallax
layers = [
    {"image": LAYER_IMAGES[i], "speed": LAYER_SPEEDS[i], "x": 0}
    for i in range(4)
]

# Classe do herói do jogo (o gato)
class Hero(Actor):
    
    #Parâmetros
    def __init__(self, images, jump_images, scale=0.8, x=50, y=500, fps=10):
        super().__init__(images[0])
        self.images = images
        self.jump_images = jump_images
        self.scale = scale
        self.pos = (x, y)
        self.index = 0
        self.fps = fps
        self.time = 0
        self.velocity = 0
        self.is_jumping = False
        self.hitbox = Rect(self.x, self.y, self.width, self.height)
        
    #Comportametos
    def update(self):
        if keyboard.up and self.y == 500:
            self.velocity = JUMP_STRENGTH
            sounds.pulo.play()
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y > 500:
            self.y = 500
            self.velocity = 0
            self.is_jumping = False
        else:
            self.is_jumping = True

        #Classe Rect e método hitbox para evitar colisões antecipadas
        self.hitbox = Rect(self.topleft, (self.width, self.height))
        
    #Animações(configuração das imagens)
    def animate(self, dt):
        self.time += dt
        if self.time > 1 / self.fps:
            self.time = 0
            self.index = (self.index + 1) % len(self.images if not self.is_jumping else self.jump_images)
            self.image = (self.images if not self.is_jumping else self.jump_images)[self.index]

# Classe do objetivo (pássaro)
class Objective(Actor):
    VELOCITY = 3

    #Parâmetros
    def __init__(self, images, scale=0.5, x=900, y=300, fps=10):
        super().__init__(images[0])
        self.images = images
        self.scale = scale
        self.pos = (x, y)
        self.index = 0
        self.fps = fps
        self.time = 0
        self.hitbox = Rect(self.x - 30, self.y - 30, 50, 50) #Classe Rect e método hitbox para evitar colisões antecipadas

    #Movimeto os eixos x e y
    def movement(self):
        self.x -= self.VELOCITY
        if self.x < 0:
            self.x = random.randint(900, 1500)
            self.y = random.randint(300, 400)
        self.hitbox.topleft = (self.x - 30, self.y - 30)

    #Animações(configuração das imagens)
    def animate(self, dt):
        self.time += dt
        if self.time > 1 / self.fps:
            self.time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

# Classe dos inimigos do jogo (cachorro e espinho)
class Enemy(Actor):
    
    #Parâmetros 
    def __init__(self, images, scale=0.5, x=1600, y=510, fps=10):
        super().__init__(images[0])
        self.images = images
        self.scale = scale
        self.pos = (x, y)
        self.index = 0
        self.fps = fps
        self.time = 0
        self.velocity = INITIAL_ENEMY_VELOCITY
        self.hitbox = Rect(self.x - 10, self.y - 10, 20, 20) #Classe Rect e método hitbox para evitar colisões antecipadas
        
    #Movimeto os eixos x e y
    def movement(self):
        self.x -= self.velocity
        if self.x < 0:
            self.x = random.randint(1000, 3000)
            self.velocity = min(self.velocity + 0.05, MAX_ENEMY_VELOCITY)
        self.hitbox = Rect(
            self.x - self.width // 2 + 15,
            self.y - self.height // 2 + 20,
            self.width - 30,
            self.height - 30,
        )

    #Animações(configuração das imagens)
    def animate(self, dt):
        self.time += dt
        if self.time > 1 / self.fps:
            self.time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

# Classe para os botões do menu
class MenuButton(Actor):
    def __init__(self, image, x, y, action):
        super().__init__(image)
        self.pos = (x, y)
        self.action = action

#imagens dos botões
menu_buttons = [
    MenuButton("start1", 200, 500, "start_game"),
    MenuButton("on1", 400, 500, "toggle_sound"),
    MenuButton("quit1", 600, 500, "exit_game"),
]

# Classe para animação do gato no mrnu
class AnimatedActor:
    
    #Parâmetros
    def __init__(self, images, pos, fps=10):
        self.images = images
        self.image = images[0]
        self.pos = pos
        self.index = 0
        self.fps = fps
        self.time = 0

    #Animações(configuração das imagens)
    def animate(self, dt):
        self.time += dt
        if self.time > 1 / self.fps:
            self.time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    #Desehho na tela inicial
    def draw(self):
        screen.blit(self.image, self.pos)

# Frames necessários para o gato
cat = Hero(
    ["cat1", "cat2", "cat3", "cat4"],
    [f"pulo{i}" for i in range(1, 15)]
)
bird = Objective(["bird1", "bird2", "bird3", "bird4", "bird5", "bird6"]) #Frames pássaro
dog = Enemy(["dog1", "dog2", "dog3", "dog4", "dog5"]) #Frames cachorro
spike = Enemy(["spike1", "spike2", "spike3", "spike4", "spike5"]) #Frames espinho 
cat_animation = AnimatedActor(["vivo1", "vivo2", "vivo3", "vivo4"], (270, 100), fps=8) #Frames gato inicial
 
# Função para resetar o jogo
def reset_game():
    global game_over, score, death_sound
    game_over = False
    score = 0
    death_sound = False
    cat.pos = (50, 500)
    bird.pos = (900, 350)
    dog.pos = (1600, 510)
    spike.pos = (2000, 510)
    dog.velocity = INITIAL_ENEMY_VELOCITY
    spike.velocity = INITIAL_ENEMY_VELOCITY

# Função para lidar com cliques do mouse
def on_mouse_down(pos):
    global menu
    if menu:
        for button in menu_buttons:
            if button.collidepoint(pos):
                if button.action == "start_game":
                    menu = False
                    reset_game()
                    sounds.miado_aleatorio.play()
                elif button.action == "toggle_sound":
                    toggle_music()
                    button.image = "on1" if music_on else "off1"
                elif button.action == "exit_game":
                    exit()

# Função para alternar a música
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("gatonafloresta")
    else:
        music.stop()

# Função principal de desenho
def draw():
    if menu:
        screen.blit("layer1", (0, 0))
        if show_text:
            screen.draw.text(
                "Catch the Bird",
                centerx=400,
                centery=80,
                color=BLACK,
                fontname="press-start",
                fontsize=50,
            )
        cat_animation.draw()

        for button in menu_buttons:
            button.draw()
    else:
        screen.clear()

        if game_over:
            screen.blit("morto5", (330, 50))
            screen.draw.text(
                "Fim de Jogo",
                centerx=400,
                centery=250,
                color=WHITE,
                fontname="press-start",
                fontsize=60,
            )
            screen.draw.text(
                f"Pontos: {score}",
                centerx=400,
                centery=400,
                color=WHITE,
                fontname="press-start",
                fontsize=45,
            )
            screen.draw.text(
                "Aperte espaço para Reiniciar",
                centerx=400,
                centery=500,
                color=WHITE,
                fontname="press-start",
                fontsize=15,
            )

        else:
            for layer in layers:
                screen.blit(layer["image"], (layer["x"], 0))
                screen.blit(layer["image"], (layer["x"] + WIDTH, 0))
            screen.draw.filled_rect(Rect(0, 500, WIDTH, HEIGHT), BROWN)
            screen.draw.text(
                f"Pontos:{score}",
                centerx=100,
                centery=50,
                color=WHITE,
                background=BLACK,
                fontname="press-start",
                fontsize=20,
            )
            cat.draw()
            bird.draw()
            dog.draw()
            spike.draw()

# Função de atualização do jogo (gerar comportamentos e animações)
def update(dt):
    global score, game_over, menu, blink_time, show_text, death_sound

    #Comportamento parallax
    for layer in layers:
        layer["x"] -= layer["speed"]
        if layer["x"] <= -WIDTH:
            layer["x"] = 0

    #Evitar proximidade entre o cachorro e o espinho
    if abs(spike.x - dog.x) < 350:
        spike.x = random.randint(1300, 3000)

    #Colisão gato e pássaro, ajuste de pontuação
    if cat.hitbox.colliderect(bird.hitbox) and not game_over:
        sounds.collect.play()
        sounds.comendo_passaro.play()
        bird.x = random.randint(900, 1500)
        bird.y = random.randint(350, 400)
        score += 1
    #Colisão gato e cachorro ou gato e espinho, game over
    if cat.hitbox.colliderect(dog.hitbox) or cat.hitbox.colliderect(spike.hitbox):
        game_over = True
        if not death_sound and not menu:
            sounds.inicio_jogo.play()
            sounds.game_over.play()
        death_sound = True

    #Animação de título do jogo
    if menu:
        blink_time += dt
        if blink_time > 0.4:
            blink_time = 0
            show_text = not show_text
    
    #Atualização de comportamentos e animações dos personagens        
    cat_animation.animate(dt)
    cat.update()
    cat.animate(dt)
    bird.animate(dt)
    bird.movement()
    dog.animate(dt)
    dog.movement()
    spike.animate(dt)
    spike.movement()

    #Condição para restart
    if keyboard.space and game_over:
        sounds.miado_aleatorio.play()
        reset_game()
        cat.pos = (50, 500)
    return

pgzrun.go()