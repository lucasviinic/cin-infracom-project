import socket
import os


def enviaArquivo(nomeArquivo, tamanhoBuffer, udpSocket, enderecoServidor):
    try:
        with open(nomeArquivo, 'rb') as file:
            print(f"Enviando {nomeArquivo} para o servidor...")

            udpSocket.sendto(os.path.basename(nomeArquivo).encode(), enderecoServidor)

            while True:
                data = file.read(tamanhoBuffer)
                if not data:
                    break
                udpSocket.sendto(data, enderecoServidor)

            udpSocket.sendto(b"FINAL", enderecoServidor)
            print(f"{nomeArquivo} enviado com sucesso!")

    except FileNotFoundError as e:
        print(f"Erro: Arquivo {nomeArquivo} não encontrado.")
    except socket.error as e:
        print(f"Erro de socket: {str(e)}")
    except Exception as e:
        print(f"Erro ao enviar arquivo: {str(e)}")

def main():
    host = 'localhost'
    port = 12345
    tamanhoBuffer = 1024

    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    pasta_recebidos_cliente = "arquivos_recebidos_cliente"
    if not os.path.exists(pasta_recebidos_cliente):
        os.makedirs(pasta_recebidos_cliente)

    while True:
        nomeArquivo = input("Digite o caminho completo do arquivo que deseja enviar ('sair' para sair): ")

        if nomeArquivo.lower() == 'sair':
            udpSocket.sendto(b"SAIR", (host, port))
            break

        enderecoServidor = (host, port)
        enviaArquivo(nomeArquivo, tamanhoBuffer, udpSocket, enderecoServidor)

        data, _ = udpSocket.recvfrom(tamanhoBuffer)
        nomeArquivo_retransmitido = data.decode()

        if nomeArquivo_retransmitido != "FINAL":
            arquivo_recebido = os.path.join(pasta_recebidos_cliente, f"recebido_{os.path.basename(nomeArquivo_retransmitido)}")
            with open(arquivo_recebido, 'wb') as file:
                while True:
                    data, _ = udpSocket.recvfrom(tamanhoBuffer)
                    if data == b"FINAL":
                        break
                    file.write(data)

            print(f"{nomeArquivo_retransmitido} recebido do servidor com sucesso.")
        else:
            print("Erro: Nenhum arquivo retransmitido pelo servidor.")

    udpSocket.close()

if __name__ == "__main__":
    main()