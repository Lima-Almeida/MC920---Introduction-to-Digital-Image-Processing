from PIL import Image
import numpy as np
import cv2

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

#Negativo da imagem
img_neg = 255 - img
img_neg = Image.fromarray(img_neg).convert('L')
img_neg.save('images/outputs/ex8/output_img_neg.png')

#Imagem transformada
img_transf = np.clip(img, 100, 200)
img_transf = cv2.normalize(img_transf, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
img_transf = Image.fromarray(img_transf).convert('L')
img_transf.save('images/outputs/ex8/output_img_transf.png')

#Linhas pares invertidas
img_inv = img.copy()
img_inv[::2] = img_inv[::2, ::-1]
img_inv = Image.fromarray(img_inv).convert('L')
img_inv.save('images/outputs/ex8/output_img_inv.png')

#Reflexão de linhas
img_refl = img.copy()
height = img_refl.shape[0]
height = height // 2
img_refl[height:] = img_refl[:height][::-1]
img_refl = Image.fromarray(img_refl).convert('L')
img_refl.save('images/outputs/ex8/output_img_refl.png')

#Espelhamento vertical
img_esp = img.copy()
img_esp = img_esp[::-1]
img_esp = Image.fromarray(img_esp).convert('L')
img_esp.save('images/outputs/ex8/output_img_esp.png')
