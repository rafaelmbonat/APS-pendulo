import cv2
import numpy as np
import pandas as pd
import time

# Função para processar o vídeo
def processar_video(caminho_video):
    # Abre o vídeo
    cap = cv2.VideoCapture(caminho_video)
    
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return
    
    # Obtém informações do vídeo
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Lista para armazenar as posições e tempos
    dados = []
    
    # Loop para processar cada frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Redimensiona o frame para 540x960
        frame_redimensionado = cv2.resize(frame, (540, 960))
        
        # Converte para escala de cinza
        gray = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2GRAY)
        
        # Aplica um blur para reduzir ruído
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        
        
        # Binariza a imagem (ajuste o threshold conforme necessário)
        _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)
        
        # Encontra contornos
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Se encontrou contornos
        if contours:
            # Pega o maior contorno (assumindo que é a massa)
            c = max(contours, key=cv2.contourArea)
            
            # Obtém o retângulo delimitador
            x, y, w, h = cv2.boundingRect(c)
            
            # Desenha o retângulo no frame
            cv2.rectangle(frame_redimensionado, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Calcula o centro da massa
            centro_x = x + w // 2
            centro_y = y + h // 2
            
            # Obtém o tempo atual do frame
            tempo = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            
            # Adiciona os dados à lista
            dados.append([tempo, centro_x, centro_y])
        
        # Mostra o frame processado
        cv2.imshow('Video Processado', frame_redimensionado)
        
        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libera os recursos                           
    cap.release()
    cv2.destroyAllWindows()
    
    # Cria um DataFrame com os dados
    df = pd.DataFrame(dados, columns=['Tempo (s)', 'Posicao X', 'Posicao Y'])
    
    # Exibe a tabela
    print("\nTabela de Posições da Massa:")
    print(df)
    
    # Opcional: Salvar a tabela em um arquivo CSV
    df.to_csv('posicoes_massa.csv', index=False)

# Caminho para o vídeo (substitua pelo caminho do seu vídeo)
caminho_video = 'pendulo.mp4'  # Substitua pelo nome do seu arquivo de vídeo

# Executa a função
processar_video(caminho_video) 