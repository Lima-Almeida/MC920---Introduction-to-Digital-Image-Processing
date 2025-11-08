from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

nome = input("Digite o nome da imagem (sem '.png'): ")
img = Image.open(f'trabalho2/images/{nome}.png')
img = np.array(img)

fourier = np.fft.fft2(img)
fourier_centro = np.fft.fftshift(fourier)
espectro_fourier = 20 * np.log(np.abs(fourier_centro) + 1)

#funcoes para criar mascaras
def passa_baixa(imagem, raio):
    linhas, colunas = imagem.shape
    mascara = np.zeros((linhas, colunas), np.uint8)
    cv2.circle(mascara, (colunas // 2, linhas // 2), raio, 1, thickness=-1)
    return mascara

def passa_alta(imagem, raio):
    return 1 - passa_baixa(imagem, raio)

def passa_faixa(imagem, raio1, raio2):
    return passa_baixa(imagem, raio1) - passa_baixa(imagem, raio2)

def rejeita_faixa(imagem, raio1, raio2):
    return 1 - passa_faixa(imagem, raio1, raio2)

def aplicar_filtro(fourier, mascara):
    fourier_filtrada = fourier * mascara
    fourier_s_centro = np.fft.ifftshift(fourier_filtrada)
    img_aux = np.abs(np.fft.ifft2(fourier_s_centro))
    return img_aux

passa_baixa_mascara = passa_baixa(img, 50)
passa_alta_mascara = passa_alta(img, 50)
passa_faixa_mascara = passa_faixa(img, 70, 30)
rejeita_faixa_mascara = rejeita_faixa(img, 70, 30)


img_pb = aplicar_filtro(fourier_centro, passa_baixa_mascara)
img_pa = aplicar_filtro(fourier_centro, passa_alta_mascara)
img_pf = aplicar_filtro(fourier_centro, passa_faixa_mascara)
img_rf = aplicar_filtro(fourier_centro, rejeita_faixa_mascara)

#compressao
limiar = np.percentile(np.abs(fourier_centro), 90)
fourier_comprimida = np.where(np.abs(fourier_centro) < limiar, 0, fourier_centro)
img_comprimida = np.abs(np.fft.ifft2(np.fft.ifftshift(fourier_comprimida))) #removendo o shift e aplicando a inversa

#salvando histogramas
def salvar_hist(nome, titulo, imagem):
    plt.figure()
    plt.hist(imagem.ravel(), bins=256, range=(0, 256), color='gray')
    plt.title(f'{titulo}')
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(f'trabalho2/images/outputs/ex2/{nome}.png')
    plt.close()

salvar_hist('histograma_original', 'Histograma Original', img)
salvar_hist('histograma_comprimido', 'Histograma Comprimido', img_comprimida)

#salvando imagens
def salvar_img(imagem, nome):
    imagem = Image.fromarray(np.uint8(np.clip(imagem, 0, 255)))
    imagem = imagem.convert('L')
    imagem.save(f'trabalho2/images/outputs/ex2/{nome}.png')


def salvar_nucleo_filtro(mascara, fourier, nome):
    fourier_filtrado = fourier * mascara
    espectro_filtrado = 20 * np.log(np.abs(fourier_filtrado) + 1)

    espectro_filtrado = np.uint8(255 * espectro_filtrado / np.max(espectro_filtrado))
    img = Image.fromarray(espectro_filtrado)
    img.save(f'trabalho2/images/outputs/ex2/nucleo_{nome}.png')

salvar_img(img, 'img_original')
salvar_img(espectro_fourier, 'espectro_fourier')
salvar_img(img_pb, 'img_passa_baixa')
salvar_img(img_pa, 'img_passa_alta')
salvar_img(img_pf, 'img_passa_faixa')
salvar_img(img_rf, 'img_rejeita_faixa')
salvar_img(img_comprimida, 'img_comprimida')
salvar_nucleo_filtro(passa_baixa_mascara, fourier_centro, 'passa_baixa')
salvar_nucleo_filtro(passa_alta_mascara, fourier_centro, 'passa_alta')
salvar_nucleo_filtro(passa_faixa_mascara, fourier_centro, 'passa_faixa')
salvar_nucleo_filtro(rejeita_faixa_mascara, fourier_centro, 'rejeita_faixa')
