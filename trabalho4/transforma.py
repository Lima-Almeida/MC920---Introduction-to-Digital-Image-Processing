from PIL import Image
import numpy as np
import argparse
import math

def ler_imagem(caminho):
    return np.array(Image.open(caminho).convert('L'))

def salvar_imagem(img, caminho):
    img = Image.fromarray(np.uint8(np.clip(img, 0, 255)))
    img.save(caminho)

def P(t):
    return t if t > 0 else 0

def R(s):
    return (1/6) * (
        P(s + 2)**3
        - 4 * P(s + 1)**3
        + 6 * P(s)**3
        - 4 * P(s - 1)**3
    )

#metodos de interpolação

def interpolacao_vizinho(img, x, y):
    h, w = img.shape
    x_int = int(math.floor(x))
    y_int = int(math.floor(y))
    dx = x - x_int
    dy = y - y_int

    if dx < 0.5 and dy < 0.5:
        xi, yi = x_int, y_int
    elif dx >= 0.5 and dy < 0.5:
        xi, yi = x_int + 1, y_int
    elif dx < 0.5 and dy >= 0.5:
        xi, yi = x_int, y_int + 1
    else:
        xi, yi = x_int + 1, y_int + 1

    if 0 <= xi < w and 0 <= yi < h:
        return img[yi, xi]
    return 0


def interpolacao_bilinear(img, x, y):
    h, w = img.shape
    if x < 0 or x >= w - 1 or y < 0 or y >= h - 1:
        return 0
    x0, y0 = int(x), int(y)
    dx, dy = x - x0, y - y0

    val = (
        (1 - dx) * (1 - dy) * img[y0, x0] +
        dx * (1 - dy) * img[y0, x0 + 1] +
        (1 - dx) * dy * img[y0 + 1, x0] +
        dx * dy * img[y0 + 1, x0 + 1]
    )
    return int(val)

def interpolacao_bicubica(img, x, y):
    h, w = img.shape
    x0, y0 = int(x), int(y)
    result = 0
    for m in range(-1, 3):
        for n in range(-1, 3):
            xm = int(np.clip(x0 + m, 0, w - 1))
            yn = int(np.clip(y0 + n, 0, h - 1))
            dx = x - (x0 + m)
            dy = y - (y0 + n)
            result += img[yn, xm] * R(dx) * R(dy)
    return int(np.clip(result, 0, 255))

def LagrangeAux(i, dx):
    if i == -1:
        return (-dx * (dx - 1) * (dx - 2)) / 6
    elif i == 0:
        return ((dx + 1) * (dx - 1) * (dx - 2)) / 2
    elif i == 1:
        return (-dx * (dx + 1) * (dx - 2)) / 2
    elif i == 2:
        return (dx * (dx + 1) * (dx - 1)) / 6
    return 0

def interpolacao_lagrange(img, x, y):
    h, w = img.shape
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    dx, dy = x - x0, y - y0

    result = 0
    for m in range(-1, 3):
        for n in range(-1, 3):
            xm = int(np.clip(x0 + m, 0, w - 1))
            yn = int(np.clip(y0 + n, 0, h - 1))
            result += img[yn, xm] * LagrangeAux(m, dx) * LagrangeAux(n, dy)

    return int(np.clip(result, 0, 255))

#transformacoes

def escala(img, fator, interpolador):
    h, w = img.shape
    h_out, w_out = int(h * fator), int(w * fator)
    img_out = np.zeros((h_out, w_out), dtype=np.uint8)
    for y_out in range(h_out):
        for x_out in range(w_out):
            x_in = x_out / fator
            y_in = y_out / fator
            img_out[y_out, x_out] = interpolador(img, x_in, y_in)
    return img_out

def rotacao(img, angulo, interpolador):
    ang_rad = math.radians(angulo)
    h, w = img.shape
    cx, cy = w / 2, h / 2
    cos_a, sin_a = math.cos(ang_rad), math.sin(ang_rad)

    #calculand novo tamanho da imagem
    corners = [(-cx, -cy), (w - cx, -cy), (-cx, h - cy), (w - cx, h - cy)]
    x_coords = [cos_a * x - sin_a * y for x, y in corners]
    y_coords = [sin_a * x + cos_a * y for x, y in corners]
    w_out = int(max(x_coords) - min(x_coords))
    h_out = int(max(y_coords) - min(y_coords))
    cx_out, cy_out = w_out / 2, h_out / 2

    img_out = np.zeros((h_out, w_out), dtype=np.uint8)
    for y_out in range(h_out):
        for x_out in range(w_out):
            x = x_out - cx_out
            y = y_out - cy_out
            x_in = cos_a * x + sin_a * y + cx
            y_in = -sin_a * x + cos_a * y + cy
            img_out[y_out, x_out] = interpolador(img, x_in, y_in)
    return img_out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=float, help='Ângulo de rotação (graus)')
    parser.add_argument('-e', type=float, help='Fator de escala (float)')
    parser.add_argument('-m', type=str, choices=['vizinho', 'bilinear', 'bicubica', 'lagrange'], default='vizinho', help='Método de interpolação')
    parser.add_argument('-i', type=str, required=True, help='Imagem de entrada (sem extensão)')
    parser.add_argument('-o', type=str, required=True, help='Nome da imagem de saída (sem extensão)')
    args = parser.parse_args()

    if args.m == 'vizinho':
        interpolador = interpolacao_vizinho
    elif args.m == 'bilinear':
        interpolador = interpolacao_bilinear
    elif args.m == 'bicubica':
        interpolador = interpolacao_bicubica
    elif args.m == 'lagrange':
        interpolador = interpolacao_lagrange
    else:
        raise ValueError(f'Método de interpolação inválido: {args.m}')

    img = ler_imagem(f'images/{args.i}.png')

    if args.a is not None:
        img_transformada = rotacao(img, args.a, interpolador)
    elif args.e is not None:
        img_transformada = escala(img, args.e, interpolador)
    else:
        raise ValueError('Informe -a para rotação ou -e para escala.')

    salvar_imagem(img_transformada, f'images/outputs/parte2/{args.o}.png')

main()
