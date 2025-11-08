from PIL import Image
import numpy as np

nome1 = input("Digite o nome da primeira imagem (sem '.png'): ")
nome2 = input("Digite o nome da segunda imagem (sem '.png'): ")
img_1 = Image.open(f'images/{nome1}.png')
img_2 = Image.open(f'images/{nome2}.png')

img_1 = np.array(img_1)
img_2 = np.array(img_2)

if img_1.shape != img_2.shape:
    print("Erro: As imagens devem ter as mesmas dimensões!")
    exit()

porcentagens = [[0.2, 0.8], [0.5, 0.5], [0.8, 0.2]]

for k in porcentagens:
    img_1_temp = img_1 * k[0]
    img_2_temp = img_2 * k[1]

    img_final = img_1_temp + img_2_temp
    img_final = Image.fromarray(img_final).convert('L')
    img_final.save(f'images/outputs/ex7/img_{int(k[0]*100)}_{int(k[1]*100)}.png')