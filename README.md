para rodar o cliente é necessário ter o kivy instalado

python3 -m pip install kivy[base]
ou
python -m pip install kivy[base]


para executar o server:
	python src/server/server.py

para executar os clients (executa dois clients de uma vez):
	python src/client/main.py & python src/client/main.py


Principais funcionalidades da aplicação:
	Esta aplicação se trata de um jogo da velha, jogado sempre entre dois jogadores.
	É possível ter mais de um jogo ocorrendo simultaneamente.

Para que uma partida do jogo seja iniciada, a aplicação espera que dois jogadores se conectem ao servidor, se um único jogador se conectar ele terá que esperar até que um segundo jogador se conecte para que o jogo se inicie. 

As jogadas são feitas através de uma interface gráfica

A aplicação ignora as jogadas enviadas por um jogador B até que o jogador A tenha feito sua jogada e vice-versa. A menos que seja a primeira jogada da partida.

Ao final da partida os jogadores são desconectados e a aplicação é fechada, a ideia é fazer com que cada partida possa ser realizada por um novo par de usuários que se conectaram à aplicação. Podem ser os mesmos usuários da última partida ou outros.

A aplicação verifica se o jogador A enviou o caractere correto (apenas X e O são permitidos).


As mensagens que o servidor aceita são do formato <LINHA>#<COLUNA>:<CARACTERE> 
onde:
	LINHA e COLUNA representam a posição da jogada numa matriz 3x3 (ambos variam de 0 à 2)
	CARACTERE é o símbolo do jogador (X ou O)




PODERIA TER SIDO DESENVOLVIDO:

Retornar uma mensagem de erro padrão para os clientes quando alguma mensagem não foi aceita. Até o momento, ao enviar uma mensagem num formato que não é o ideal, o usuário não consegue ter certeza se a mensagem não foi recebida pela aplicação ou se está errada, gerando ambiguidade.

Dar a possibilidade de o jogador continuar conectado ao servidor, entrando novamente na fila de espera para esperar outro jogador;

Implementar um sistema de pontuação para os jogadores;


PRINCIPAIS DIFICULDADES:
A utilização de threads foi, provavelmente, o maior desafio até acharmos uma solução para que os clientes alterassem um mesmo ‘tabuleiro’ do jogo e que o estado atual da aplicação fosse compartilhado entre os 2 jogadores (duas threads).

Também foi dificil lidar com o jogador sair no meio do jogo, pois ele possui uma socket esperando uma resposta do servidor 
