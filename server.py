import socket
import os


def recebeArquivo(nomeArquivo, tamanhoBuffer, udpSocket, enderecoCliente):
    try:
        pasta_recebidos_servidor = "arquivos_recebidos_servidor"
        if not os.path.exists(pasta_recebidos_servidor):
            os.makedirs(pasta_recebidos_servidor)

        arquivo_destino = os.path.join(pasta_recebidos_servidor, nomeArquivo)

        with open(arquivo_destino, 'wb') as file:
            print(f"Recebendo arquivo {nomeArquivo} do cliente {enderecoCliente}...")
            while True:
                data, _ = udpSocket.recvfrom(tamanhoBuffer)
                if data == b"FINAL":
                    break
                file.write(data)

        reenviaArquivo(arquivo_destino, tamanhoBuffer, udpSocket, enderecoCliente)

    except FileNotFoundError as e:
        print(f"Erro ao receber: Arquivo {nomeArquivo} não encontrado.")
    except socket.error as e:
        print(f"Erro de socket ao receber: {str(e)}")
    except Exception as e:
        print(f"Erro ao receber arquivo: {str(e)}")

    print(f"{nomeArquivo} recebido do cliente {enderecoCliente} com sucesso.")

def reenviaArquivo(nomeArquivo, tamanhoBuffer, udpSocket, enderecoCliente):
    try:
        with open(nomeArquivo, 'rb') as file:
            print(f"Enviando {nomeArquivo} de volta para {enderecoCliente}...")

            nomeArquivo_bytes = os.path.basename(nomeArquivo).encode()

            udpSocket.sendto(nomeArquivo_bytes, enderecoCliente)
            while True:
                data = file.read(tamanhoBuffer)              
                if not data:
                    break
                udpSocket.sendto(data, enderecoCliente)
            udpSocket.sendto(b"FINAL", enderecoCliente)  

    except FileNotFoundError as e:
        print(f"Erro no reenvio: Arquivo {nomeArquivo} não encontrado.")
    except socket.error as e:
        print(f"Erro de socket no reenvio: {str(e)}")
    except Exception as e:
        print(f"Erro ao reenviar arquivo: {str(e)}")

    print(f"{nomeArquivo} enviado para {enderecoCliente} com sucesso.")

def main():
    host = 'localhost'
    port = 12345
    tamanhoBuffer = 1024

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.bind((host, port))

    print("Server UDP está pronto para receber arquivos.")

    while True:

        data, enderecoCliente = udpSocket.recvfrom(tamanhoBuffer)
        nomeArquivo = data.decode()  

        if nomeArquivo == "SAIR":
            print("Cliente encerrou a conexão.")
            break

        recebeArquivo(nomeArquivo, tamanhoBuffer, udpSocket, enderecoCliente)

    udpSocket.close()

if __name__ == "__main__":
    main()