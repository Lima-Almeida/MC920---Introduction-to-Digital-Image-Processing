from PIL import Image
import numpy as np

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

#a)
filtro = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])

#R
img_R1 = img[:, :, 2] * filtro[0, 0]
img_R2 = img[:, :, 2] * filtro[1, 0]
img_R3 = img[:, :, 2] * filtro[2, 0]

#G
img_G1 = img[:, :, 1] * filtro[0, 1]
img_G2 = img[:, :, 1] * filtro[1, 1]
img_G3 = img[:, :, 1] * filtro[2, 1]

#B
img_B1 = img[:, :, 0] * filtro[0, 2]
img_B2 = img[:, :, 0] * filtro[1, 2]
img_B3 = img[:, :, 0] * filtro[2, 2]

#Juntando
img_R = img_R1 + img_G1 + img_B1
img_G = img_R2 + img_G2 + img_B2
img_B = img_R3 + img_G3 + img_B3

img_R = np.clip(img_R, 0, 255)
img_G = np.clip(img_G, 0, 255)
img_B = np.clip(img_B, 0, 255)

final_img = np.stack([img_R, img_G, img_B], axis=-1)

final_img = Image.fromarray(final_img.astype(np.uint8))
final_img.save('images\outputs\ex5\output_img_a.png')

#b)
filtro2 = np.array([0.2989, 0.5870, 0.1140])

#R
R = img[:, :, 2] * filtro2[0]

#G
G = img[:, :, 1] * filtro2[1]

#B
B = img[:, :, 0] * filtro2[2]

#Juntando
I = R + G + B

i_final = np.clip(I, 0, 255)
i_final = Image.fromarray(i_final.astype(np.uint8))
i_final.save('images\outputs\ex5\output_img_b.png')