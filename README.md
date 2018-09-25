# Relógio ponto

## Definição do projeto e requisitos
     *Usaremos:
     *PHP
     *Postgres ou Firebase
     *Python

Vamos criar um sistema de controle de ponto para uma empresa de pequeno porte, com leitor de rfid e display lcd.
Os usuários utilizarão o seu cartão com etiqueta RFID para marcar os horários de chegada e saída.
O sistema salva os horários, que podem ser editados por um usuário administrador.
Cada trabalhador poderá consultar sua marcação também com o seu cartão, e solicitar para o administrador a alteração ou adição das marcações.

## Escolha da placa de desenvolvimento e os argumentos da escolha.

Vamos usar o microcomputador Raspberry Pi, devido a facilidade de uso -visto que roda um sistema operacional linux, baseado no Debian- vasto acervo de bibliotecas e repositórios, disponíveis na internet e também por já possuirmos a placa e o módulo RFID.
