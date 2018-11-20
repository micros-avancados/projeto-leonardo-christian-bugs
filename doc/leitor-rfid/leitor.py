#!/usr/bin/env python
# -*- coding: utf8 -*-
 
import time
import RPi.GPIO as GPIO
import MFRC522
import sqlite3

#importa as bibliotecas para trabalhar com o display
import I2C_LCD_driver
import socket
import fcntl
import struct

lcdi2c = I2C_LCD_driver.lcd()
 
# UID dos cartões que possuem acesso liberado.
# 57:97:F4:DA:EE  - tag do cartao do prof anderson
CARTOES_LIBERADOS = {
    'E0:1F:2C:33:E0': 'Chaveiro RFID',
    '3C:2F:4F:0:2D': 'Teste',
}
 
try:
    # Inicia o módulo RC522.
    LeitorRFID = MFRC522.MFRC522()
 
    print('Aproxime seu cartão RFID')
    lcdi2c.lcd_display_string("Apro Cartao RFID", 1,0)
    lcdi2c.lcd_display_string("Ou Dig Seu Cod", 2,0)

 
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
                
                cursor.execute("""select * from pessoas where rfid = ? and validade >= date('now')""", (uid,));
                
                result = cursor.fetchall()
                 
                # Se o cartão está liberado exibe mensagem de boas vindas.
                if result:
                    id_pessoa = result[0][0]
                    nome_pessoa = result[0][1]
                    rfid_pessoa = result[0][2]
                    validade_pessoa = result[0][3]
                    print('Acesso Liberado!')
                    print("ola " + nome_pessoa)

		    lcdi2c.lcd_clear()
	            lcdi2c.lcd_display_string("Acesso Liberado", 1,0)
		    lcdi2c.lcd_display_string("Ola " + nome_pessoa, 2,0)
	            time.sleep(4)
                else:
                    print('Acesso Negado!')
		    lcdi2c.lcd_clear()
	            lcdi2c.lcd_display_string("Acesso Negado", 1,0)
		    time.sleep(4); 

                print('\nAproxime seu cartão RFID')
		lcdi2c.lcd_clear()
		lcdi2c.lcd_display_string("Aproxime Seu", 1,0)
		lcdi2c.lcd_display_string("Cartao RFID", 2,0)
 
        time.sleep(.25)
except KeyboardInterrupt:
    # Se o usuário precionar Ctrl + C
    # encerra o programa.
    GPIO.cleanup()
    print('nPrograma encerrado.')
