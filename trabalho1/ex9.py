from PIL import Image
import numpy as np
import cv2

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

niveis_2 = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
niveis_4 = cv2.normalize(img, None, alpha=0, beta=3, norm_type=cv2.NORM_MINMAX)
niveis_8 = cv2.normalize(img, None, alpha=0, beta=7, norm_type=cv2.NORM_MINMAX)
niveis_16 = cv2.normalize(img, None, alpha=0, beta=15, norm_type=cv2.NORM_MINMAX)
niveis_32 = cv2.normalize(img, None, alpha=0, beta=31, norm_type=cv2.NORM_MINMAX)
niveis_64 = cv2.normalize(img, None, alpha=0, beta=63, norm_type=cv2.NORM_MINMAX)

niveis_2 = cv2.normalize(np.uint8(niveis_2), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
niveis_4 = cv2.normalize(np.uint8(niveis_4), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
niveis_8 = cv2.normalize(np.uint8(niveis_8), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
niveis_16 = cv2.normalize(np.uint8(niveis_16), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
niveis_32 = cv2.normalize(np.uint8(niveis_32), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
niveis_64 = cv2.normalize(np.uint8(niveis_64), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
img = np.uint8(img)

img_2_niveis = Image.fromarray(niveis_2).convert('RGB')
img_4_niveis = Image.fromarray(niveis_4).convert('RGB')
img_8_niveis = Image.fromarray(niveis_8).convert('RGB')
img_16_niveis = Image.fromarray(niveis_16).convert('RGB')
img_32_niveis = Image.fromarray(niveis_32).convert('RGB')
img_64_niveis = Image.fromarray(niveis_64).convert('RGB')
img_256_niveis = Image.fromarray(img).convert('RGB')

img_2_niveis.save('images/outputs/ex9/output_img_2.png')
img_4_niveis.save('images/outputs/ex9/output_img_4.png')
img_8_niveis.save('images/outputs/ex9/output_img_8.png')
img_16_niveis.save('images/outputs/ex9/output_img_16.png')
img_32_niveis.save('images/outputs/ex9/output_img_32.png')
img_64_niveis.save('images/outputs/ex9/output_img_64.png')
img_256_niveis.save('images/outputs/ex9/output_img_256.png')