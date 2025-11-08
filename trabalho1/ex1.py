from PIL import Image
import numpy as np
import cv2

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
grey_img = img.convert('L')
grey_img.save('images/outputs/ex1/output_img_grey.png')

grey_img = np.array(grey_img)
grey_img_blur_np = cv2.GaussianBlur(grey_img, (21, 21), 0)

grey_img_blur = Image.fromarray(grey_img_blur_np)
grey_img_blur.save('images/outputs/ex1/output_img_blur.png')

final_img = (grey_img / grey_img_blur_np) * 255
final_img = Image.fromarray(final_img)
final_img = final_img.convert('RGB')
final_img.save('images/outputs/ex1/output_final_img.png')

#Teste com tamanho de máscara 51x51
grey_img_blur_np_51 = cv2.GaussianBlur(grey_img, (1023, 1023), 0)
grey_img_blur_51 = Image.fromarray(grey_img_blur_np_51)
grey_img_blur_51.save('images/outputs/ex1/mask51/output_img_blur_51.png')

final_img_51 = (grey_img / grey_img_blur_np_51) * 255
final_img_51 = Image.fromarray(final_img_51)
final_img_51 = final_img_51.convert('RGB')
final_img_51.save('images/outputs/ex1/mask51/output_final_img_51.png')

#Teste com tamanho de máscara 5x5
grey_img_blur_np_5 = cv2.GaussianBlur(grey_img, (5, 5), 0)
grey_img_blur_5 = Image.fromarray(grey_img_blur_np_5)
grey_img_blur_5.save('images/outputs/ex1/mask5/output_img_blur_5.png')

grey_img_blur_np_5 = np.where(grey_img_blur_np_5 < 1e-5, 1e-5, grey_img_blur_np_5) #Colocado para evitar warning de divisao por 0 na divisão da linha abaixo (código ainda funciona sem essa linha)
final_img_5 = (grey_img / grey_img_blur_np_5) * 255
final_img_5 = Image.fromarray(final_img_5)
final_img_5 = final_img_5.convert('RGB')
final_img_5.save('images/outputs/ex1/mask5/output_final_img_5.png')

#Teste com imagem menos saturada
img_normalizada = cv2.normalize(grey_img, None, alpha=100, beta=150, norm_type=cv2.NORM_MINMAX)

grey_img_blur_np_norm = cv2.GaussianBlur(img_normalizada, (21, 21), 0)

final_img_norm = (img_normalizada / grey_img_blur_np_norm) * 255
final_img_norm = Image.fromarray(final_img_norm)
img_normalizada = Image.fromarray(img_normalizada)
img_normalizada = img_normalizada.convert('RGB')
img_normalizada.save('images/outputs/ex1/normalizada100_150/output_img_normalizada.png')
final_img_norm = final_img_norm.convert('RGB')
final_img_norm.save('images/outputs/ex1/normalizada100_150/output_final_img_normalizada.png')
