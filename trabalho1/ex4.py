from PIL import Image
import numpy as np

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

filtro = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])

transposta = filtro.T
final_img = img.dot(transposta)
img_errada = img.dot(filtro)

img_errada = np.clip(img_errada, 0, 255)
final_img = np.clip(final_img, 0, 255)

final_img = Image.fromarray(final_img.astype(np.uint8))
img_errada = Image.fromarray(img_errada.astype(np.uint8))
final_img.save('images/outputs/ex4/output_img.png')
img_errada.save('images/outputs/ex4/output_img_errada.png')