from PIL import Image
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

def carregar_imagem(nome):
    img = Image.open(f'images/{nome}').convert('L')
    img = np.array(img)
    return img


def salvar_imagem(imagem, modo, nome):
    img = Image.fromarray(np.uint8(np.clip(imagem, 0, 255)))
    img.save(f'images/outputs/{modo}/{nome}')
    return


def salvar_histograma_projecao(imagem_bin, modo, nome_hist):
    projecao = np.sum(imagem_bin, axis=1)
    plt.figure()
    plt.plot(projecao, color='black')
    plt.title(f'Projeção Horizontal - {nome_hist}')
    plt.xlabel('Linha (y)')
    plt.ylabel('Soma dos pixels')
    plt.tight_layout()
    plt.savefig(f'images/outputs/{modo}/{nome_hist}.png')
    plt.close()
    return


def salvar_linhas_hough(bordas, linhas, modo, nome_base):
    visualizacao = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)

    for linha in linhas:
        rho, theta = linha[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(visualizacao, (x1, y1), (x2, y2), (0, 0, 255), 1)

    salvar_imagem(visualizacao, modo, f"{nome_base}_linhas_hough.png")
    return


def calcular_threshold_dinamico(bordas, base=100, min_th=30, max_th=200):
    total_pixels = bordas.shape[0] * bordas.shape[1]
    qtd_bordas = np.count_nonzero(bordas)
    densidade = qtd_bordas / total_pixels

    desvio = np.std(bordas)

    peso_densidade = (1 - densidade)  #quanto menos borda, menor o threshold
    peso_contraste = desvio / 128     

    ajuste = (peso_densidade * 0.6 + peso_contraste * 0.4)

    threshold = int(base * ajuste)
    threshold = max(min_th, min(max_th, threshold)) 

    return threshold


def encontrar_angulo_projecao(imagem_bin):
    melhor_angulo = 0
    melhor_valor = -1

    for angulo in np.arange(-30, 30.1, 0.5):
        (h, w) = imagem_bin.shape
        matriz_rotacao = cv2.getRotationMatrix2D((w // 2, h // 2), angulo, 1.0)
        imagem_rotacionada = cv2.warpAffine(imagem_bin, matriz_rotacao, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
        projecao = np.sum(imagem_rotacionada, axis=1)
        valor = np.sum(np.diff(projecao) ** 2)
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_angulo = angulo

    return melhor_angulo


def encontrar_angulo_hough(imagem_bin, modo, nome_base):
    bordas = cv2.Sobel(imagem_bin, cv2.CV_8U, 1, 0, ksize=3)
    salvar_imagem(bordas, modo, f"{nome_base}_sobel.png")

    threshold = calcular_threshold_dinamico(bordas)
    linhas = cv2.HoughLines(bordas, 1, np.pi / 180, threshold=threshold)

    if linhas is None:
        return 0

    angulos = []
    for linha in linhas:
        rho, theta = linha[0]
        angulo = (theta * 180 / np.pi) - 90
        angulos.append(angulo)

    if len(angulos) == 0:
        return 0
    
    salvar_linhas_hough(bordas, linhas, modo, nome_base)

    return np.median(angulos)

def rotacionar(imagem, angulo):
    (h, w) = imagem.shape
    matriz_rot = cv2.getRotationMatrix2D((w // 2, h // 2), angulo, 1.0)
    return cv2.warpAffine(imagem, matriz_rot, (w, h), flags=cv2.INTER_LINEAR, borderValue=255)

def main():
    if len(sys.argv) != 4:
        print("Uso: python alinhar.py imagem_entrada.png modo imagem_saida.png")
        sys.exit(1)

    entrada = sys.argv[1]
    modo = sys.argv[2].lower()
    saida = sys.argv[3]

    nome_base = entrada.replace('.png', '')

    img_cinza = carregar_imagem(entrada)
    img_bin = np.where(img_cinza > 127, 255, 0).astype(np.uint8)
    img_bin_aux = img_bin.copy()

    salvar_histograma_projecao(img_bin, modo, f"{nome_base}_hist_original")

    if modo == "projecao":
        angulo = encontrar_angulo_projecao(img_bin)
    elif modo == "hough":
        angulo = encontrar_angulo_hough(img_bin, modo, nome_base)
    else:
        print("Modo inválido. Use 'projecao' ou 'hough'.")
        sys.exit(1)

    print(f"Ângulo detectado: {angulo:.2f} graus")

    salvar_imagem(img_bin_aux, modo, f'bin_{saida}')
    img_corrigida = rotacionar(img_cinza, angulo)
    salvar_imagem(img_corrigida, modo, saida)

    img_corrigida_bin = np.where(img_corrigida > 127, 0, 255).astype(np.uint8)
    salvar_histograma_projecao(img_corrigida_bin, modo, f"{nome_base}_hist_alinhada")
    return

main()