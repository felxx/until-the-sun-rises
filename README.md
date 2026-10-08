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
- [x] Funcionalidade de Score e Leaderboard, onde deverá salvar o nome do jogador
- [x] Adição de mais habilidades de level up
- [x] Adição de itens consumíveis (como medkits para o jogador se curar)
- [x] Balanceamento geral, levando em conta o tempo de 10 minutos para a vitória
- [x] Tela de encerramento, onde a manhã chega, os zumbis morrem e sobe os créditos do jogo
- [x] Polimento visual geral
