#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import time
import RPi.GPIO as GPIO
import MFRC522
import sqlite3
import psycopg2

import socket
from copy import *

#importa as bibliotecas para trabalhar com o display
import I2C_LCD_driver
import socket
import fcntl
import struct


if __name__ == '__main__':

    lcdi2c = I2C_LCD_driver.lcd()  
    # UID dos cartões que possuem acesso liberado.
    # 57:97:F4:DA:EE  - tag do cartao do prof anderson
     
    try:
        # Inicia o módulo RC522.
        LeitorRFID = MFRC522.MFRC522()
       
        print('Aproxime seu cartão RFID')
        #lcdi2c.lcd_display_string("Apro Cartao RFID", 1,0)
        #lcdi2c.lcd_display_string("Ou Dig Seu Cod", 2,0)
            
        #Mostra o horario no display
        lcdi2c.lcd_display_string("%s" %time.strftime("%H:%M:%S"), 1,4)

        #Mostra a data no display
        lcdi2c.lcd_display_string("%s" %time.strftime("%A %d/%m/%y"), 2,0)

     
        while True:
            # Verifica se existe uma tag próxima do módulo.
            status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)


            if status == LeitorRFID.MI_OK:
                print('Cartão detectado!')

                # Efetua leitura do UID do cartão.
                status, uid = LeitorRFID.MFRC522_Anticoll()
     
                if status == LeitorRFID.MI_OK:
                    uid = ':'.join(['%X' % x for x in uid])
                    print('UID do cartão: %s' % uid)
                    lcdi2c.lcd_clear()
                    lcdi2c.lcd_display_string("ID do cartao:", 1,0)
                    lcdi2c.lcd_display_string("%s" % uid, 2,0)	
                    time.sleep(3)
                    
                    conn = sqlite3.connect('Ponto.db')
                    cursor =  conn.cursor();


                    host='165.227.9.145'
                    a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    a.settimeout(.5)

                    if a.connect_ex((host,80)):
                       print('Sem conexao com a internet')
                       cursor.execute("insert into marcacao (uid,data_hora) values (?, datetime('now') )",( uid,))
                       conn.commit()


                    else:
                       conn_postgres = psycopg2.connect(host='165.227.9.145', dbname='ponto',
                       user='ponto', password='ponto')
                       cursor_postgres = conn_postgres.cursor()

                       print('Conectado a Internet')
                       
                       cursor.execute("""select * from marcacao""")
                       marcacoes_antigas = cursor.fetchall()
                       
                       if marcacoes_antigas:
                          linhas = len(marcacoes_antigas)
                          contador = 0
                          print('Inserindo Marcacoes Antigas')
                          while(linhas > contador):
                               cursor_postgres.execute("insert into marcacoes (ref_pessoa,data_hora) values ( (select id from pessoas where rfid = %s), %s )",(marcacoes_antigas[contador][0],marcacoes_antigas[contador][1]))
                               conn_postgres.commit()
                               contador = contador + 1                       
                     
                          cursor.execute("delete from marcacao")
                          conn.commit()
 
                           
                       cursor_postgres.execute("select * from pessoas where rfid = %s and validade >= date('now')", (uid,))
                    
                       #result = cursor.fetchall()
                       result = cursor_postgres.fetchall()
                     
                       # Se o cartão está liberado exibe mensagem de boas vindas.
                       if result:
                           id_pessoa = result[0][0]
                           nome_pessoa = result[0][1]
                           rfid_pessoa = result[0][2]
                           validade_pessoa = result[0][3]
                           print('Ponto Registrado!')
                           print("Ola " + nome_pessoa)
                        
                           cursor_postgres.execute("insert into marcacoes (ref_pessoa,data_hora) values ( %s, now() )",(id_pessoa,))
                           conn_postgres.commit()

                           lcdi2c.lcd_clear()
                           lcdi2c.lcd_display_string("Ponto Registrado", 1,0)
                           lcdi2c.lcd_display_string("Ola " + nome_pessoa, 2,0)
                           time.sleep(4)
                       else:
                           print('Usuario nao encontrado!')
                           lcdi2c.lcd_clear()
                           lcdi2c.lcd_display_string("Usuario nao enc", 1,0)
                           time.sleep(4); 
                    
                    
                    print('\nAproxime seu cartão RFID')
                    lcdi2c.lcd_clear()
                    lcdi2c.lcd_display_string("Aproxime Seu", 1,0)
                    lcdi2c.lcd_display_string("Cartao RFID", 2,0)
     
            time.sleep(.25)
    except KeyboardInterrupt:
        # Se o usuário pressionar Ctrl + C
        # encerra o programa.
        GPIO.cleanup()
        print('nPrograma encerrado.')
