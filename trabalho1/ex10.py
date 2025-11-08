from PIL import Image
import numpy as np
import cv2

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

filtro_h1 = np.array([[0, 0, -1, 0, 0], 
                      [0, -1, -2, -1, 0], 
                      [-1, -2, 16, -2, -1],
                      [0, -1, -2, -1, 0],
                      [0, 0, -1, 0, 0]])

filtro_h2 = np.array([[1, 4, 6, 4, 1], 
                      [4, 16, 24, 16, 4], 
                      [6, 24, 16, 24, 6],
                      [4, 16, 24, 16, 4],
                      [1, 4, 6, 4, 1]]) * (1/256)

filtro_h3 = np.array([[-1, 0, 1], 
                      [-2, 0, 2], 
                      [-1, 0, 1]])

filtro_h4 = np.array([[-1, -2, -1], 
                      [0, 0, 0], 
                      [1, 2, 1]])

filtro_h5 = np.array([[-1, -1, -1], 
                      [-1, 8, -1], 
                      [-1, -1, -1]])

filtro_h6 = np.array([[1, 1, 1], 
                      [1, 1, 1], 
                      [1, 1, 1]]) * (1/9)

filtro_h7 = np.array([[-1, -1, 2], 
                      [-1, 2, -1], 
                      [2, -1, -1]])

filtro_h8 = np.array([[2, -1, -1], 
                      [-1, 2, -1], 
                      [-1, -1, 2]])

filtro_h9 = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0], 
                      [0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 1]]) * (1/9)

filtro_h10 = np.array([[-1, -1, -1, -1, -1], 
                      [-1, 2, 2, 2, -1], 
                      [-1, 2, 8, 2, -1],
                      [-1, 2, 2, 2, -1],
                      [-1, -1, -1, -1, -1]]) * (1/8)

filtro_h11 = np.array([[-1, -1, 0], 
                      [-1, 0, 1], 
                      [0, 1, 1]])

lista_filtros = [filtro_h1, filtro_h2, filtro_h3, filtro_h4, filtro_h5, filtro_h6, filtro_h7, filtro_h8, filtro_h9, filtro_h10, filtro_h11]

for k in range(11):
    img_k = cv2.filter2D(img, -1, lista_filtros[k])
    img_k = Image.fromarray(img_k)
    img_k.save(f'images/outputs/ex10/output_img_h{k+1}.png')

img_h3_c = cv2.filter2D(img, -1, filtro_h3)
img_h4_c = cv2.filter2D(img, -1, filtro_h4)

img_comb = np.sqrt(img_h3_c.astype(np.uint16)**2 + img_h4_c.astype(np.uint16)**2) #Transformando em uint16 para resolver problema do overflow quando elevamos ao quadrado.
img_comb = np.clip(img_comb, 0, 255)
img_comb = img_comb.astype(np.uint8) #Convertendo de volta para uint8
img_comb = Image.fromarray(img_comb)
img_comb.save('images/outputs/ex10/output_img_h3_h4.png')