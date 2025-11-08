from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology

nome = input("Digite o nome da imagem (sem '.png'): ")
img_color = Image.open(f'images/{nome}.png')
img_color_np = np.array(img_color)

img_gray = cv2.cvtColor(img_color_np, cv2.COLOR_RGB2GRAY)
_, img_bin = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY_INV)

#criando contornos
img_bin_uint8 = (img_bin * 255).astype(np.uint8)
contornos, _ = cv2.findContours(img_bin_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contornos = np.ones_like(img_bin_uint8) * 255
cv2.drawContours(img_contornos, contornos, -1, color=0, thickness=1)
Image.fromarray(img_contornos).save('images/outputs/parte1/img_contornos.png')


img_bin = morphology.remove_small_objects(img_bin > 0, min_size=20)

label_img = measure.label(img_bin)
props = measure.regionprops(label_img)

print(f'Número de regiões: {len(props)}')
for i, prop in enumerate(props):
    print(f'região {i}: área: {prop.area} perímetro: {prop.perimeter:.6f} excentricidade: {prop.eccentricity:.6f} solidez: {prop.solidity:.6f}')


img_rotulada = img_color_np.copy()
for i, prop in enumerate(props):
    y, x = prop.centroid
    cv2.putText(img_rotulada, str(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 0), 2, cv2.LINE_AA)


Image.fromarray(np.uint8(img_gray)).save(f'images/outputs/parte1/img_gray.png')
Image.fromarray((img_bin * 255).astype(np.uint8)).save(f'images/outputs/parte1/img_bin.png')
Image.fromarray(img_rotulada).save(f'images/outputs/parte1/img_rotulada.png')

pequenos = sum(1 for p in props if p.area < 1500)
medios = sum(1 for p in props if 1500 <= p.area < 3000)
grandes = sum(1 for p in props if p.area >= 3000)

print(f'número de regiões pequenas: {pequenos}')
print(f'número de regiões médias: {medios}')
print(f'número de regiões grandes: {grandes}')

areas = [p.area for p in props]
plt.figure()
plt.hist(areas, bins=10, color='gray')
plt.title('Histograma de Áreas')
plt.xlabel('Área (pixels)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig('images/outputs/parte1/hist_area.png')
plt.close()
