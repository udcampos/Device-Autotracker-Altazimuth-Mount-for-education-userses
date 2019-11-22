""" Importações de módulos para o programa, o socket é para fazer a conexão
com o Stellarium, o bitstring é para converter a string
de bytes em angulo e tempo, caso ocorra erro na importação é
possivel instalar o bitstring usando sudo aptitude install python3-bitstring"""


from socket import *
import time
from bitstring import BitArray, BitStream, ConstBitStream

""" As duas primeiras funções, servem para receber os dados do Stellarium"""
## A conecta() define os parametros de conexão, configurados no Stellarium

def conecta():
    HOST = "localhost"
    PORT = 10001
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM) ## cria o socket
    serversock.bind(ADDR) ## abre a porta
    serversock.listen(1)  ##começa a escutar 
    return serversock

## A faz_conexao se comunica com os Stellarium e recebe a string de bytes

def faz_conexao():
    serversock=conecta()
    while 1:
        print("Aguardando conexão")
        clientsock, addr = serversock.accept()
        print("esta conectado",addr)
        e='t'
        tamanho=2048
        data=[]
        print("Digite CTRL+2 simultâneamente, para obter coordenada do Stellarium", end="\n")
        while e!="0":            
            e=input("Para fazer nova aquisição digite qualquer número, se quiser sair digite 0  ")
            data.append(clientsock.recv(tamanho))
        return data
      
"""A converte_string_bytes, recebe a string de bytes e devolve a 
declinação e a ascensão reta """   
def converte_string_bytes(string_byte):
    data = ConstBitStream(bytes=string_byte, length=160)
    msize = data.read('intle:16')
    mtype = data.read('intle:16')
    mtime = data.read('intle:64')
    ant_pos = data.bitpos
    ra = data.read('hex:32')
    data.bitpos = ant_pos
    ra_uint = data.read('uintle:32')
    ant_pos = data.bitpos
    dec = data.read('hex:32')
    data.bitpos = ant_pos
    dec_int = data.read('intle:32')
    return dec_int,ra_uint

##A converte_dec_em_grau converte os valores decimais para graus
def converte_dec_em_grau(string_byte):
    t=converte_string_bytes(string_byte)
    dec=t[0]
    angulo=(90*dec)/1073741824    
    grau=int(angulo)
    grau_dec=float(int(angulo))    
    minuto_dec=(angulo-grau_dec)*60
    if minuto_dec<0:
        minuto=int(minuto_dec)*(-1)
        segundo_dec=((minuto_dec*-1)-(float(int(minuto))))*60
        segundo=round(segundo_dec,1)
    else:
        minuto=int(minuto_dec)
        segundo_dec=(minuto_dec-(float(int(minuto))))*60
        segundo=round(segundo_dec,1)
    return (grau, minuto,segundo)

## A converte_ascecao_reta, converte os valores decimais em horas
def converte_ascencao_reta(string_byte):
    t=converte_string_bytes(string_byte)
    ar=t[1]
    tempo=(12*ar)/2147483648
    hora=int(tempo)
    hora_dec=float(int(hora))                   
    minuto_dec=(tempo-hora_dec)*60
    minuto=int(minuto_dec)
    segundo_dec=((minuto_dec)-(float(minuto)))*60
    segundo=round(segundo_dec,2)
    return (hora, minuto,segundo)

## Função Principal
def main():
    string_byte_recebido=faz_conexao()
    quantidade_medicoes=len(string_byte_recebido)
    n=0
    grau=[]
    tempo=[]
    while quantidade_medicoes!=0:
        string_byte=string_byte_recebido[n]
        grau.append(converte_dec_em_grau(string_byte))
        tempo.append(converte_ascencao_reta(string_byte))
        n+=1
        quantidade_medicoes-=1
    return print(grau,tempo)

if __name__ == "__main__":
    main()
    
        
        
        

      
      
 
    

