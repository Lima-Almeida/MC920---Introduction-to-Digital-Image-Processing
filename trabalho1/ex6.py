from PIL import Image
import numpy as np

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'images/{nome}.png')
img = np.array(img)

for k in range(8):
    plano_k = ((img >> k) & 1) * 255
    img_plano_k = Image.fromarray(plano_k).convert('RGB')
    img_plano_k.save(f'images/outputs/ex6/output_img_{k}.png')

# plano_7 = ((img >> 7) & 1) * 255
# plano_6 = ((img >> 6) & 1) * 255
# plano_5 = ((img >> 5) & 1) * 255
# plano_4 = ((img >> 4) & 1) * 255
# plano_3 = ((img >> 3) & 1) * 255
# plano_2 = ((img >> 2) & 1) * 255
# plano_1 = ((img >> 1) & 1) * 255
# plano_0 = (img & 1) * 255

# img_plano_7 = Image.fromarray(plano_7).convert('RGB')
# img_plano_6 = Image.fromarray(plano_6).convert('RGB')
# img_plano_5 = Image.fromarray(plano_5).convert('RGB')
# img_plano_4 = Image.fromarray(plano_4).convert('RGB')
# img_plano_3 = Image.fromarray(plano_3).convert('RGB')
# img_plano_2 = Image.fromarray(plano_2).convert('RGB')
# img_plano_1 = Image.fromarray(plano_1).convert('RGB')
# img_plano_0 = Image.fromarray(plano_0).convert('RGB')

# img_plano_7.save('images\outputs\ex6\output_img_7.png')
# img_plano_6.save('images\outputs\ex6\output_img_6.png')
# img_plano_5.save('images\outputs\ex6\output_img_5.png')
# img_plano_4.save('images\outputs\ex6\output_img_4.png')
# img_plano_3.save('images\outputs\ex6\output_img_3.png')
# img_plano_2.save('images\outputs\ex6\output_img_2.png')
# img_plano_1.save('images\outputs\ex6\output_img_1.png')
# img_plano_0.save('images\outputs\ex6\output_img_0.png')