from PIL import Image
import numpy as np

varreduras = ['esq_dir', 'alternada']
distr_titulos = ['floyd_steinberg', 'stevenson_acre', 'burkes', 'sierra', 'stucki', 'jarvis_judice_ninke']
distribuicoes = {'floyd_steinberg': [[[1, -1], 3/16], [[1, 0], 5/16], [[1, 1], 1/16], [[0, 1], 7/16]],

           'stevenson_acre': [[[0, 2], 32/200], [[1, -3], 12/200], [[1, -1], 26/200], [[1, 1], 30/200], 
                              [[1, 3], 16/200], [[2, -2], 12/200], [[2, 0], 26/200], [[2, 2], 12/200]],

            'burkes': [[[0, 1], 8/32], [[0, 2], 4/32], [[1, -2], 2/32], [[1, -1], 4/32], [[1, 0], 8/32], 
                       [[1, 1], 4/32], [[1, 2], 2/32]],

            'sierra': [[[0, 1], 5/32], [[0, 2], 3/32], [[1, -2], 2/32], [[1, -1], 4/32], [[1, 0], 5/32], 
                       [[1, 1], 4/32], [[1, 2], 2/32], [[2, -1], 2/32], [[2, 0], 3/32], [[2, 1], 2/32]],

            'stucki': [[[0, 1], 8/42], [[0, 2], 4/42], [[1, -2], 2/42], [[1, -1], 4/42], [[1, 0], 8/42], 
                       [[1, 1], 4/42], [[1, 2], 2/42], [[2, -2], 1/42], [[2, -1], 2/42], [[2, 0], 4/42], 
                       [[2, 1], 2/42], [[2, 2], 1/42]],   

            'jarvis_judice_ninke': [[[0, 1], 7/48], [[0, 2], 5/48], [[1, -2], 3/48], [[1, -1], 5/48], 
                                    [[1, 0], 7/48], [[1, 1], 5/48], [[1, 2], 3/48], [[2, -2], 1/48], 
                                    [[2, -1], 3/48], [[2, 0], 5/48], [[2, 1], 3/48], [[2, 2], 1/48]]}

#algoritmo slide 124 alterado
def meio_tom(im, nome_distrb, varredura):
    im = im.astype(np.float32)
    altura, largura = im.shape
    distrb = distribuicoes[nome_distrb]

    for x in range(altura):
        if varredura == 'esq_dir' or x % 2 == 0:
            range_y = range(largura)
        else:
            range_y = range(largura - 1, -1, -1)

        for y in range_y:
            pixel_anterior = im[x, y]
            pixel_atual = 255 if pixel_anterior > 127 else 0
            im[x, y] = pixel_atual
            erro = pixel_anterior - pixel_atual

            for p in distrb:
                coord, mult = p
                coord_x, coord_y = coord
                aux_x = x + coord_x

                if varredura == 'esq_dir' or x % 2 == 0: #espelhar o deslocamento horizontal na linha ímpar
                    aux_y = y + coord_y
                else:
                    aux_y = y - coord_y

                if altura > aux_x >= 0 and largura > aux_y >= 0:
                    im[aux_x, aux_y] += erro * mult

    im = np.clip(im, 0, 255)
    im = im.astype(np.uint8)
    return im

def main():
    nome = input("Digite o nome da imagem (sem '.png'): ")
    img = Image.open(f'trabalho2/images/{nome}.png')
    img_array = np.array(img)

    if len(img_array.shape) == 3 and img_array.shape[2] == 3: #detectando se a imagem é RGB ou Monocromatica
        is_rgb = True
    else:
        is_rgb = False

    contador = 1
    print('Distribuições: ')
    for k in distribuicoes.keys():
        print(f'{contador} - {k}')
        contador += 1
    print('7 - Todas (aplica todas as distribuições e varreduras, gerando 12 imagens)')
    print()
    distr_aplicada = int(input("Qual distribuição deseja aplicar? (Digite o numero): "))
    if 0 < distr_aplicada < 7:
        print("Varreduras: ")
        print("1 - Esquerda para direita")
        print("2 - Alternada (zigue-zague)")
        tipo_varredura = int(input("Qual varredura deseja aplicar? (Digite o número): "))
        if 0 < tipo_varredura < 3:
            distr_nome = distr_titulos[distr_aplicada - 1]
            varredura_tipo = varreduras[tipo_varredura - 1]

            if is_rgb:
                canais = []
                for i in range(3):
                    canal = meio_tom(img_array[:, :, i].copy(), distr_nome, varredura_tipo)
                    canais.append(canal)
                img_resultante = np.stack(canais, axis=2)
                img_resultante = Image.fromarray(img_resultante, mode='RGB')
            else:
                img_resultante = meio_tom(img_array.copy(), distr_nome, varredura_tipo)
                img_resultante = Image.fromarray(img_resultante).convert('L')

            img_resultante.save(f'trabalho2/images/outputs/ex1/output_{distr_nome}_{varredura_tipo}.png')
        else:
            print("Erro: o número digitado não é válido")
    elif distr_aplicada == 7:
        for k in distribuicoes.keys():
            for j in varreduras:
                if is_rgb:
                    canais = []
                    for i in range(3):
                        canal = meio_tom(img_array[:, :, i].copy(), k, j)
                        canais.append(canal)
                    img_resultante = np.stack(canais, axis=2)
                    img_resultante = Image.fromarray(img_resultante, mode='RGB')
                else:
                    img_resultante = meio_tom(img_array.copy(), k, j)
                    img_resultante = Image.fromarray(img_resultante).convert('L')
                img_resultante.save(f'trabalho2/images/outputs/ex1/output_{k}_{j}.png')
    else:
        print("Erro: o número digitado não é válido")

    return

main()
