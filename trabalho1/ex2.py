from PIL import Image
import numpy as np

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

img_normal = img / 255

img_gama_1_5 = (img_normal ** (1/1.5)) * 255
img_gama_2_5 = (img_normal ** (1/2.5)) * 255
img_gama_3_5 = (img_normal ** (1/3.5)) * 255

img_gama_1_5 = Image.fromarray(img_gama_1_5).convert('RGB')
img_gama_2_5 = Image.fromarray(img_gama_2_5).convert('RGB')
img_gama_3_5 = Image.fromarray(img_gama_3_5).convert('RGB')

img_gama_1_5.save('images/outputs/ex2/output_img_1_5.png')
img_gama_2_5.save('images/outputs/ex2/output_img_2_5.png')
img_gama_3_5.save('images/outputs/ex2/output_img_3_5.png')