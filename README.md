# Meu Jogo do Sonic: Endless Runner

Um divertido e simples jogo estilo "Endless Runner" (Corrida Infinita) inspirado no clássico Sonic the Hedgehog, desenvolvido em Python utilizando a biblioteca Pygame. O objetivo é correr o máximo possível, coletar anéis, desviar de inimigos e alcançar a linha de chegada para completar a fase.

## 🚀 Como Jogar

* **Correr:** O Sonic corre automaticamente para a direita.
* **Pular:** Pressione a tecla **ESPAÇO** para fazer o Sonic pular e evitar obstáculos ou coletar anéis mais altos.
* **Anéis:** Colete anéis para aumentar sua pontuação. Eles também servem como "vida" temporária, protegendo o Sonic de um hit.
* **Inimigos:** Cuidado com os inimigos! Se o Sonic colidir com um inimigo sem pular em cima dele, ele perde todos os anéis coletados e se torna temporariamente invencível. Se ele for atingido sem anéis, perde uma vida.
* **Game Over:** O jogo termina se o Sonic perder todas as suas vidas.
* **Linha de Chegada:** Alcance a bandeira no final da fase para completá-la e reiniciar o desafio com uma nova fase.

## ✨ Funcionalidades Implementadas

* **Movimentação do Sonic:** Sonic corre e pula com física de gravidade.
* **Animação do Sonic:** Diferentes sprites para corrida e pulo.
* **Coleta de Anéis:** Sistema de anéis colecionáveis.
* **Inimigos:** Inimigos gerados aleatoriamente (Moto Bugs e Buzz Bombers) com comportamentos distintos (chão e voo).
* **Sistema de Vidas e Dano:** Sonic perde anéis ao ser atingido, e vidas se não tiver anéis. Invencibilidade temporária após dano.
* **Rolagem de Cenário (Parallax Scrolling):** Camadas de fundo com diferentes velocidades para criar profundidade.
* **Chão Dinâmico:** Geração procedural de um chão pixelado.
* **Aumento de Dificuldade:** A velocidade do jogo aumenta gradualmente com o tempo, tornando o desafio constante.
* **Linha de Chegada:** Um objetivo final para cada "fase", reiniciando o jogo ao ser alcançado.
* **Tela Inicial:** Uma tela de boas-vindas antes do jogo começar.
* **Tela de Game Over:** Para quando o Sonic fica sem vidas.
* **Tela de Fase Completa:** Mensagem de sucesso ao alcançar a linha de chegada.
* **Sistema de HUD:** Exibição de anéis, vidas, tempo e velocidade do jogo.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pygame:** Biblioteca para desenvolvimento de jogos 2D em Python.

## 📦 Como Executar

1.  **Pré-requisitos:**
    * Certifique-se de ter o Python 3.x instalado em sua máquina.
    * Instale a biblioteca Pygame:
        ```bash
        pip install pygame
        ```

2.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO # Navegue até a pasta do projeto
    ```
    (Substitua `SEU_USUARIO` e `SEU_REPOSITORIO` pelos seus dados do GitHub)

3.  **Estrutura de Pastas:**
    Certifique-se de que a pasta `assets` esteja no mesmo diretório do arquivo `meu_sonic.py` e contenha todas as imagens e sons necessários:
    ```
    .
    ├── meu_sonic.py
    └── assets/
        ├── sonic_parado_1.png
        ├── sonic_correndo_2.png
        ├── sonic_pulo_3.png
        ├── céu_1.png
        ├── ring.png
        ├── moto_bug.png
        ├── buzz_bomber.png
        ├── flag.png
        └── sua_musica_do_sonic.mp3
        └── Custom Edited - Sonic the Hedgehog Customs - Sonic SMS-Style.png # Tela inicial
    ```

4.  **Execute o Jogo:**
    ```bash
    python meu_sonic.py
    ```

## 🎨 Ativos Gráficos e Sonoros

A maioria dos assets gráficos foi adaptada ou inspirada em sprites de jogos clássicos do Sonic para manter a estética pixelada.
A música de fundo deve ser um arquivo MP3 na pasta `assets` com o nome `sua_musica_do_sonic.mp3` (você pode substituir pelo seu tema favorito do Sonic!).
