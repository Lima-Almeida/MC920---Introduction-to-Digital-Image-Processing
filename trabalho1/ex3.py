from PIL import Image
import numpy as np

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

altura = img.shape[0]
largura = img.shape[1]

if altura % 4 != 0 or largura % 4 != 0:
    print("Erro: A altura e largura da imagem devem ser divisíveis por 4.")
    exit()

alt_4 = altura // 4
larg_4 = largura // 4

#Criando submatrizes
pedaco_1 = img[0:alt_4, 0:larg_4]
pedaco_2 = img[0:alt_4, larg_4:larg_4*2]
pedaco_3 = img[0:alt_4, larg_4*2:larg_4*3]
pedaco_4 = img[0:alt_4, larg_4*3:largura]

pedaco_5 = img[alt_4:alt_4*2, 0:larg_4]
pedaco_6 = img[alt_4:alt_4*2, larg_4:larg_4*2]
pedaco_7 = img[alt_4:alt_4*2, larg_4*2:larg_4*3]
pedaco_8 = img[alt_4:alt_4*2, larg_4*3:largura]

pedaco_9 = img[alt_4*2:alt_4*3, 0:larg_4]
pedaco_10 = img[alt_4*2:alt_4*3, larg_4:larg_4*2]
pedaco_11 = img[alt_4*2:alt_4*3, larg_4*2:larg_4*3]
pedaco_12 = img[alt_4*2:alt_4*3, larg_4*3:largura]

pedaco_13 = img[alt_4*3:altura, 0:larg_4]
pedaco_14 = img[alt_4*3:altura, larg_4:larg_4*2]
pedaco_15 = img[alt_4*3:altura, larg_4*2:larg_4*3]
pedaco_16 = img[alt_4*3:altura, larg_4*3:largura]

linha_1 = np.concatenate((pedaco_6, pedaco_11, pedaco_13, pedaco_3), 1)
linha_2 = np.concatenate((pedaco_8, pedaco_16, pedaco_1, pedaco_9), 1)
linha_3 = np.concatenate((pedaco_12, pedaco_14, pedaco_2, pedaco_7), 1)
linha_4 = np.concatenate((pedaco_4, pedaco_15, pedaco_10, pedaco_5), 1)
final_img = np.concatenate((linha_1, linha_2, linha_3, linha_4), 0)

final_img = Image.fromarray(final_img).convert('RGB')
final_img.save('images/outputs/ex3/output_img.png')
