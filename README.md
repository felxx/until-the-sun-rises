# Until The Sun Rises

Jogo de sobrevivência *Top-down Shooter / Roguelite / Bulletheaven* desenvolvido em Python utilizando a biblioteca Pygame. O projeto se passa em um cenário pós-apocalíptico noturno, onde o jogador possui campo de visão reduzido e deve utilizar uma lanterna para sobreviver a ondas de inimigos.

Este projeto está sendo desenvolvido como requisito de avaliação para a disciplina de Tópicos em Computação do curso de Engenharia de Software.

## Requisitos

- Python 3.x
- Pygame (fornecido no arquivo de dependências)

## Instalação e Execução

1. Clone o repositório ou extraia os arquivos na sua máquina.
2. Abra o terminal na pasta raiz do projeto.
3. Comandos para executar no terminal:
```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

## To-do (3° Trimestre)

- [x] Tela de menu, com as opções de iniciar, ranking de jogadores, créditos e sair
- [x] Menu de pause quando o jogador pressionar esc, onde terá as opções de reiniciar, configurações e sair.
- [x] Adicionar fog nos limites do mapa e aumentar as bordas
- [ ] Funcionalidade de Score e Leaderboard, onde deverá salvar o nome do jogador
- [ ] Balanceamento geral, levando em conta o tempo de 10 minutos para a vitória
- [ ] Tela de encerramento, onde a manhã chega, os zumbis morrem e sobe os créditos do jogo
- [ ] Inteligência artificial nos zumbis, para que eles contornem objetos.
- [ ] Adição de mais habilidades de level up
- [ ] Adição de itens consumíveis (como medkits para o jogador se curar)
- [ ] Polimento visual geral

## To-do (APENAS SE SOBRAR MUITO TEMPO)

- [ ] Tela de configuração para, principalmente, ajuste de áudio
- [ ] Adição de boss fights (3 no total: 1° no minuto 3:00, 2° no minuto 6:00 e a 3° no minuto 9:00)
- [ ] Inimigos especiais
- [ ] Mais opções de arsenal
- [ ] Barris explosivos no mapa
- [ ] Aprimoramento no sistema de dano, incluindo floating damage
- [ ] Sistema de recarga na arma
