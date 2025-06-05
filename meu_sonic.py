import pygame
import sys
import time
import random
import math

# --- Configurações Iniciais do Pygame ---
pygame.init()
pygame.mixer.init()

# Configurações da Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu Jogo do Sonic")

# Cores (RGB)
AZUL_CEU = (135, 206, 235)
VERDE_GRAMA = (34, 139, 34)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO_ANEL = (255, 215, 0)
VERMELHO_DANO = (255, 0, 0)

# Cores para o chão pixelado
VERDE_CLARO_CHAO = (76, 175, 80)
VERDE_ESCURO_CHAO = (27, 94, 32)
MARROM_CHAO = (121, 85, 72)
MARROM_ESCURO_CHAO = (62, 39, 35)

# --- Variáveis de Estado do Jogo ---
ESTADO_TELA_INICIAL = 0
ESTADO_JOGO = 1
ESTADO_GAME_OVER = 2
ESTADO_FASE_COMPLETA = 3
estado_atual_do_jogo = ESTADO_TELA_INICIAL

# --- Configurações do Jogo Principal ---
VELOCIDADE_JOGO_BASE = 6
POSICAO_CHAO_Y = ALTURA_TELA - 80
ALTURA_CHAO = 80
LARGURA_TILE_CHAO_GERADO = 16

VELOCIDADE_JOGO_ATUAL = VELOCIDADE_JOGO_BASE
VELOCIDADE_INCREMENTO_TEMPO = 0.5
INTERVALO_INCREMENTO_VELOCIDADE = 5000
VELOCIDADE_MAXIMA_JOGO = 20.0
tempo_ultimo_incremento_velocidade = 0

# --- Variáveis de Física do Sonic ---
GRAVIDADE = 0.5
FORCA_PULO = -12
sonic_velocidade_y = 0
esta_no_ar = False
invencivel = False
tempo_invencivel_fim = 0
DURACAO_INVENCIBILIDADE = 2000

# --- Variáveis do Jogo (Anéis, Vidas, Score) ---
anéis_coletados = 0
vidas_sonic = 3
tempo_jogo_segundos = 0
tempo_ultimo_tick = pygame.time.get_ticks()

# --- Configurações da Linha de Chegada ---
# Aumentado significativamente para que demore mais para a bandeira aparecer.
# Teste este valor e ajuste-o conforme o tempo de jogo desejado.
FINAL_DA_FASE_X = 50000 # Aumentado para 50.000 (era 5.000)
bandeira_chegada_rect = None

# --- Carregamento de Recursos (Imagens e Música) ---

try:
    pygame.mixer.music.load("assets/sound_sonic.mp3")
    pygame.mixer.music.set_volume(0.5)
except pygame.error as e:
    print(f"Erro ao carregar a música: {e}")
    print("Verifique se 'assets/sound_sonic.mp3' está no lugar certo e é um arquivo de áudio válido.")


tela_inicial_img = None
try:
    tela_inicial_img = pygame.image.load("assets/sonic.png").convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar a imagem da tela inicial: {e}")
    print("Verifique se 'assets/sonic.png' está correto.")
    pygame.quit()
    sys.exit()


img_x = (LARGURA_TELA - tela_inicial_img.get_width()) // 2
img_y = (ALTURA_TELA - tela_inicial_img.get_height()) // 2


sonic_frames_idle = []
sonic_frames_run = []
sonic_frames_pulo = []

SONIC_LARGURA = 48
SONIC_ALTURA = 63

try:
    parado_img = pygame.image.load("assets/sonic_parado_1.png").convert()
    parado_img.set_colorkey(PRETO)
    sonic_frames_idle.append(pygame.transform.scale(parado_img, (SONIC_LARGURA, SONIC_ALTURA)))

    correndo_img = pygame.image.load("assets/sonic_correndo_2.png").convert()
    correndo_img.set_colorkey(PRETO)
    sonic_frames_run.append(pygame.transform.scale(correndo_img, (SONIC_LARGURA, SONIC_ALTURA)))

    pulo_img = pygame.image.load("assets/sonic_pulo_3.png").convert()
    pulo_img.set_colorkey(PRETO)
    sonic_frames_pulo.append(pygame.transform.scale(pulo_img, (SONIC_LARGURA, SONIC_ALTURA)))

except pygame.error as e:
    print(f"Erro ao carregar os sprites do Sonic: {e}")
    print("Verifique se os arquivos 'sonic_parado_1.png', 'sonic_correndo_2.png', 'sonic_pulo_3.png' estão na pasta 'assets'.")
    pygame.quit()
    sys.exit()


background_layers = []
try:
    sky_mountains_clouds_img = pygame.image.load("assets/céu_1.png").convert_alpha()
    sky_mountains_clouds_img = pygame.transform.scale(sky_mountains_clouds_img, (LARGURA_TELA, ALTURA_TELA))
    background_layers.append({"image": sky_mountains_clouds_img, "speed_factor": 0.1, "y_pos": 0})

except pygame.error as e:
    print(f"Erro ao carregar a imagem de background 'céu_1.png': {e}")
    print("Verifique se 'assets/céu_1.png' está correto e com fundo transparente.")
    background_layers = []


ring_img = None
try:
    ring_img = pygame.image.load("assets/ring.png").convert_alpha()
    ring_img = pygame.transform.scale(ring_img, (20, 20))
except pygame.error as e:
    print(f"Erro ao carregar o sprite do anel: {e}")
    print("Verifique se 'ring.png' está na pasta 'assets'. Usando círculo amarelo temporariamente.")
    ring_img = None

INIMIGO_LARGURA = 40
INIMIGO_ALTURA = 40

inimigo_sprites = {}
try:
    moto_bug_img = pygame.image.load("assets/moto_bug.png").convert_alpha()
    inimigo_sprites['moto_bug'] = pygame.transform.scale(moto_bug_img, (INIMIGO_LARGURA, INIMIGO_ALTURA))

    buzz_bomber_img = pygame.image.load("assets/buzz_bomber.png").convert_alpha()
    inimigo_sprites['buzz_bomber'] = pygame.transform.scale(buzz_bomber_img, (INIMIGO_LARGURA, INIMIGO_ALTURA))

except pygame.error as e:
    print(f"Erro ao carregar os sprites dos inimigos: {e}")
    print("Verifique se 'moto_bug.png' e 'buzz_bomber.png' estão na pasta 'assets' e com fundo transparente.")
    print("Usando quadrado vermelho temporariamente para inimigos.")
    inimigo_sprites = {}

# --- Carregar Imagem da Bandeira de Chegada ---
bandeira_chegada_img = None
BANDEIRA_LARGURA = 80
BANDEIRA_ALTURA = 80
try:
    bandeira_chegada_img = pygame.image.load("assets/flag.png").convert_alpha()
    bandeira_chegada_img = pygame.transform.scale(bandeira_chegada_img, (BANDEIRA_LARGURA, BANDEIRA_ALTURA))
except pygame.error as e:
    print(f"Erro ao carregar a imagem da bandeira de chegada: {e}")
    print("Verifique se 'assets/flag.png' está no lugar certo. Usando retângulo branco temporariamente.")
    bandeira_chegada_img = None

# --- Variáveis do Sonic no Jogo Principal ---
sonic_rect = sonic_frames_idle[0].get_rect()
sonic_rect.midbottom = (LARGURA_TELA // 4, POSICAO_CHAO_Y)
sonic_frame_atual = 0
sonic_animacao_velocidade = 0.15

# --- Variáveis do Cenário ---
scroll_x = 0

# --- Anéis na Fase ---
aneis = []
ultimo_anel_gerado_tempo = 0
INTERVALO_GERAR_ANEIS = 3000

def gerar_aneis():
    global ultimo_anel_gerado_tempo
    
    agora = pygame.time.get_ticks()
    if agora - ultimo_anel_gerado_tempo < INTERVALO_GERAR_ANEIS:
        return

    num_aneis_a_gerar = random.randint(1, 3)
    distancia_inicial = random.randint(LARGURA_TELA + 50, LARGURA_TELA + 200)
    distancia_entre_aneis = random.randint(80, 150) 

    for i in range(num_aneis_a_gerar):
        x = distancia_inicial + (i * distancia_entre_aneis)
        y = POSICAO_CHAO_Y - 50 - random.randint(0, 100) 
        aneis.append(pygame.Rect(x, y, 20, 20))
    
    ultimo_anel_gerado_tempo = agora

inimigos = []
def gerar_inimigos():
    tipos_inimigos = list(inimigo_sprites.keys())
    if not tipos_inimigos: 
        return

    tem_moto_bug = 'moto_bug' in inimigo_sprites
    tem_buzz_bomber = 'buzz_bomber' in inimigo_sprites

    if len(inimigos) < 3: 
        num_para_gerar = 3 - len(inimigos)
        for i in range(num_para_gerar):
            x = LARGURA_TELA + 500 + random.randint(0, 500) 

            if tem_buzz_bomber and (not tem_moto_bug or random.random() < 0.5): 
                tipo = 'buzz_bomber'
                y = random.randint(ALTURA_TELA // 3, ALTURA_TELA // 2) 
                
                inimigos.append({
                    'rect': pygame.Rect(x, y, INIMIGO_LARGURA, INIMIGO_ALTURA),
                    'tipo': tipo,
                    'origem_y': float(y), 
                    'amplitude_voo': random.randint(20, 50), 
                    'velocidade_voo': random.uniform(0.02, 0.05), 
                    'fase_voo': random.uniform(0, 2 * math.pi) 
                })
            elif tem_moto_bug: 
                tipo = 'moto_bug'
                y = POSICAO_CHAO_Y - INIMIGO_ALTURA 
                inimigos.append({'rect': pygame.Rect(x, y, INIMIGO_LARGURA, INIMIGO_ALTURA), 'tipo': tipo})

fonte_hud = pygame.font.Font(None, 30)
fonte_game_over = pygame.font.Font(None, 60)
fonte_fase_completa = pygame.font.Font(None, 50)

# --- Função para Resetar o Jogo ---
def resetar_jogo():
    global anéis_coletados, vidas_sonic, tempo_jogo_segundos, tempo_ultimo_tick
    global sonic_rect, sonic_velocidade_y, esta_no_ar, invencivel
    global aneis, inimigos, ultimo_anel_gerado_tempo
    global VELOCIDADE_JOGO_ATUAL, tempo_ultimo_incremento_velocidade
    global scroll_x, bandeira_chegada_rect

    anéis_coletados = 0
    vidas_sonic = 3
    tempo_jogo_segundos = 0
    tempo_ultimo_tick = pygame.time.get_ticks()

    sonic_rect.midbottom = (LARGURA_TELA // 4, POSICAO_CHAO_Y)
    sonic_velocidade_y = 0
    esta_no_ar = False
    invencivel = False

    aneis.clear() 
    inimigos.clear() 
    ultimo_anel_gerado_tempo = 0 
    
    VELOCIDADE_JOGO_ATUAL = VELOCIDADE_JOGO_BASE 
    tempo_ultimo_incremento_velocidade = pygame.time.get_ticks() 

    scroll_x = 0

    # Reposiciona a bandeira de chegada
    if bandeira_chegada_img:
        bandeira_chegada_rect = bandeira_chegada_img.get_rect()
        bandeira_chegada_rect.midbottom = (FINAL_DA_FASE_X, POSICAO_CHAO_Y)
    
    if pygame.mixer.music.get_busy(): 
        pygame.mixer.music.stop()
    pygame.mixer.music.play(-1) 


# --- Inicializar a bandeira de chegada no início do jogo ---
if bandeira_chegada_img:
    bandeira_chegada_rect = bandeira_chegada_img.get_rect()
    bandeira_chegada_rect.midbottom = (FINAL_DA_FASE_X, POSICAO_CHAO_Y)


# --- Loop Principal do Jogo ---
relogio = pygame.time.Clock()
FPS = 60

loop_principal_ativo = True
while loop_principal_ativo:
    if estado_atual_do_jogo == ESTADO_TELA_INICIAL:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loop_principal_ativo = False
            if evento.type == pygame.K_ESCAPE: 
                loop_principal_ativo = False
            if evento.type == pygame.KEYDOWN:
                estado_atual_do_jogo = ESTADO_JOGO
                resetar_jogo()


        tela.fill(PRETO)
        tela.blit(tela_inicial_img, (img_x, img_y))

        fonte = pygame.font.Font(None, 36)
        texto = fonte.render("Pressione qualquer tecla para começar...", True, BRANCO)
        texto_rect = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 50))
        tela.blit(texto, texto_rect)

        pygame.display.flip()

    elif estado_atual_do_jogo == ESTADO_JOGO:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loop_principal_ativo = False
            if evento.type == pygame.K_ESCAPE: 
                loop_principal_ativo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not esta_no_ar:
                    sonic_velocidade_y = FORCA_PULO
                    esta_no_ar = True

        # --- Lógica de Aumento de Velocidade ---
        agora = pygame.time.get_ticks()
        if agora - tempo_ultimo_incremento_velocidade > INTERVALO_INCREMENTO_VELOCIDADE:
            VELOCIDADE_JOGO_ATUAL = min(VELOCIDADE_JOGO_ATUAL + VELOCIDADE_INCREMENTO_TEMPO, VELOCIDADE_MAXIMA_JOGO)
            tempo_ultimo_incremento_velocidade = agora

        # Aplicar Gravidade
        if esta_no_ar:
            sonic_velocidade_y += GRAVIDADE
            sonic_rect.y += sonic_velocidade_y

            if sonic_rect.bottom >= POSICAO_CHAO_Y:
                sonic_rect.bottom = POSICAO_CHAO_Y
                sonic_velocidade_y = 0
                esta_no_ar = False

        # Atualizar status de invencibilidade
        if invencivel and pygame.time.get_ticks() > tempo_invencivel_fim:
            invencivel = False

        # Atualizar a rolagem do cenário
        scroll_x = (scroll_x + VELOCIDADE_JOGO_ATUAL) 

        # Atualizar posição dos anéis e detectar colisão
        for anel in list(aneis): 
            anel.x -= VELOCIDADE_JOGO_ATUAL

            if sonic_rect.colliderect(anel):
                anéis_coletados += 1
                aneis.remove(anel)

            if anel.right < 0:
                aneis.remove(anel)
        
        if len(aneis) < 2: 
            gerar_aneis()


        # Atualizar posição dos inimigos e detectar colisão
        for inimigo_data in list(inimigos): 
            inimigo_rect = inimigo_data['rect']
            inimigo_tipo = inimigo_data['tipo']
            
            inimigo_rect.x -= VELOCIDADE_JOGO_ATUAL 

            if inimigo_tipo == 'buzz_bomber':
                inimigo_rect.y = inimigo_data['origem_y'] + inimigo_data['amplitude_voo'] * math.sin(inimigo_data['velocidade_voo'] * pygame.time.get_ticks() + inimigo_data['fase_voo'])
                
                if inimigo_rect.bottom > POSICAO_CHAO_Y:
                    inimigo_rect.bottom = POSICAO_CHAO_Y
                    inimigo_data['origem_y'] = POSICAO_CHAO_Y - inimigo_data['amplitude_voo'] - INIMIGO_ALTURA / 2

            if sonic_rect.colliderect(inimigo_rect) and not invencivel:
                if sonic_velocidade_y > 0 and sonic_rect.bottom - 10 < inimigo_rect.centery: 
                    inimigos.remove(inimigo_data) 
                    sonic_velocidade_y = FORCA_PULO * 0.7 
                else:
                    vidas_sonic -= 1 
                    anéis_coletados = 0 
                    invencivel = True
                    tempo_invencivel_fim = pygame.time.get_ticks() + DURACAO_INVENCIBILIDADE
                    if vidas_sonic <= 0:
                        estado_atual_do_jogo = ESTADO_GAME_OVER
                        pygame.mixer.music.stop() 

            if inimigo_rect.right < 0:
                inimigos.remove(inimigo_data)

        gerar_inimigos()

        # --- Lógica da Linha de Chegada ---
        if bandeira_chegada_rect:
            bandeira_chegada_x_na_tela = FINAL_DA_FASE_X - scroll_x + sonic_rect.x 
            bandeira_chegada_rect.x = bandeira_chegada_x_na_tela
            
            if bandeira_chegada_rect.left < LARGURA_TELA and sonic_rect.right > bandeira_chegada_rect.centerx: 
                estado_atual_do_jogo = ESTADO_FASE_COMPLETA
                pygame.mixer.music.stop() 


        # Atualizar o tempo do jogo
        agora = pygame.time.get_ticks()
        if agora - tempo_ultimo_tick >= 1000:
            tempo_jogo_segundos += 1
            tempo_ultimo_tick = agora


        # Determinar qual sprite do Sonic usar
        if esta_no_ar:
            sonic_img_atual = sonic_frames_pulo[0]
        else:
            if sonic_frames_run:
                sonic_animacao_velocidade_ajustada = 0.15 + (VELOCIDADE_JOGO_ATUAL - VELOCIDADE_JOGO_BASE) * 0.05
                sonic_frame_atual = (sonic_frame_atual + sonic_animacao_velocidade_ajustada) % len(sonic_frames_run)
                sonic_img_atual = sonic_frames_run[int(sonic_frame_atual)]
            else: 
                sonic_img_atual = sonic_frames_idle[0] if sonic_frames_idle else pygame.Surface((SONIC_LARGURA, SONIC_ALTURA))
                sonic_img_atual.fill(BRANCO)


        # --- Desenhar na Tela ---

        # Desenhar camadas de background (Parallax)
        if not background_layers or not (background_layers[0]["image"].get_alpha() is not None or background_layers[0]["image"].get_colorkey() is not None):
            tela.fill(AZUL_CEU)

        for layer_info in background_layers:
            img = layer_info["image"]
            speed_factor = layer_info["speed_factor"]
            y_pos = layer_info.get("y_pos", 0)

            offset_x = (scroll_x * speed_factor) % img.get_width()

            tela.blit(img, (-offset_x, y_pos))
            tela.blit(img, (img.get_width() - offset_x, y_pos))


        # Desenhar o chão pixelado gerado por código
        tile_width = LARGURA_TILE_CHAO_GERADO
        ground_offset_x = int(-scroll_x % tile_width)

        for x in range(ground_offset_x - tile_width, LARGURA_TELA + tile_width, tile_width):
            altura_camada_superior = ALTURA_CHAO // 2 
            pygame.draw.rect(tela, VERDE_CLARO_CHAO, (x, POSICAO_CHAO_Y, tile_width, altura_camada_superior))
            
            pygame.draw.rect(tela, VERDE_ESCURO_CHAO, (x, POSICAO_CHAO_Y + altura_camada_superior, tile_width, ALTURA_CHAO - altura_camada_superior))

            if random.random() < 0.1: 
                detail_x = x + random.randint(0, tile_width - 5) 
                detail_y = POSICAO_CHAO_Y + altura_camada_superior + random.randint(0, ALTURA_CHAO - altura_camada_superior - 5)
                pygame.draw.rect(tela, MARROM_ESCURO_CHAO, (detail_x, detail_y, random.randint(2,5), random.randint(2,5)))
            
            if random.random() < 0.05: 
                detail_x = x + random.randint(0, tile_width - 8)
                detail_y = POSICAO_CHAO_Y + random.randint(0, altura_camada_superior - 8)
                pygame.draw.rect(tela, MARROM_CHAO, (detail_x, detail_y, random.randint(4,8), random.randint(4,8)))

        # Desenhar os Anéis
        for anel in aneis:
            if ring_img:
                tela.blit(ring_img, anel)
            else:
                pygame.draw.circle(tela, AMARELO_ANEL, anel.center, anel.width // 2)

        # Desenhar os Inimigos
        for inimigo_data in inimigos:
            inimigo_rect = inimigo_data['rect']
            inimigo_tipo = inimigo_data['tipo']
            inimigo_sprite_atual = inimigo_sprites.get(inimigo_tipo)

            if inimigo_sprite_atual:
                if invencivel and int(pygame.time.get_ticks() / 100) % 2 == 0:
                    pass
                else:
                    tela.blit(inimigo_sprite_atual, inimigo_rect)
            else:
                pygame.draw.rect(tela, VERMELHO_DANO, inimigo_rect)

        # --- Desenhar a Bandeira de Chegada ---
        if bandeira_chegada_img and bandeira_chegada_rect:
            if bandeira_chegada_rect.x < LARGURA_TELA and bandeira_chegada_rect.right > 0:
                tela.blit(bandeira_chegada_img, bandeira_chegada_rect)


        # Desenhar o Sonic (e efeito de invencibilidade)
        if invencivel and int(pygame.time.get_ticks() / 100) % 2 == 0: 
            pass 
        else:
            tela.blit(sonic_img_atual, sonic_rect)


        # --- Desenhar o HUD ---
        texto_aneis = fonte_hud.render(f"Anéis: {anéis_coletados}", True, BRANCO)
        tela.blit(texto_aneis, (10, 10))

        texto_vidas = fonte_hud.render(f"Vidas: {vidas_sonic}", True, BRANCO)
        tela.blit(texto_vidas, (10, 40))

        texto_tempo = fonte_hud.render(f"Tempo: {tempo_jogo_segundos}", True, BRANCO)
        tela.blit(texto_tempo, (LARGURA_TELA - texto_tempo.get_width() - 10, 10))

        texto_velocidade = fonte_hud.render(f"Velocidade: {VELOCIDADE_JOGO_ATUAL:.1f}", True, BRANCO)
        tela.blit(texto_velocidade, (LARGURA_TELA - texto_velocidade.get_width() - 10, 40))


        pygame.display.flip()

        relogio.tick(FPS)

    elif estado_atual_do_jogo == ESTADO_GAME_OVER:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loop_principal_ativo = False
            if evento.type == pygame.K_ESCAPE: 
                loop_principal_ativo = False
            if evento.type == pygame.KEYDOWN:
                estado_atual_do_jogo = ESTADO_TELA_INICIAL
                resetar_jogo()

        tela.fill(PRETO)
        texto_game_over = fonte_game_over.render("GAME OVER", True, VERMELHO_DANO)
        texto_rect_go = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 30))
        tela.blit(texto_game_over, texto_rect_go)

        texto_recomecar = fonte_hud.render("Pressione qualquer tecla para reiniciar", True, BRANCO)
        texto_rect_re = texto_recomecar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 30))
        tela.blit(texto_recomecar, texto_rect_re)

        pygame.display.flip()

    elif estado_atual_do_jogo == ESTADO_FASE_COMPLETA:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                loop_principal_ativo = False
            if evento.type == pygame.K_ESCAPE: 
                loop_principal_ativo = False
            if evento.type == pygame.KEYDOWN:
                estado_atual_do_jogo = ESTADO_JOGO
                resetar_jogo()

        tela.fill(AZUL_CEU)
        texto_parabens = fonte_fase_completa.render("FASE COMPLETA!", True, BRANCO)
        texto_rect_pb = texto_parabens.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40))
        tela.blit(texto_parabens, texto_rect_pb)

        texto_score = fonte_hud.render(f"Anéis Coletados: {anéis_coletados}", True, BRANCO)
        texto_rect_score = texto_score.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 10))
        tela.blit(texto_score, texto_rect_score)

        texto_recomecar = fonte_hud.render("Pressione qualquer tecla para continuar", True, BRANCO)
        texto_rect_re = texto_recomecar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 60))
        tela.blit(texto_recomecar, texto_rect_re)

        pygame.display.flip()


pygame.quit()
sys.exit()