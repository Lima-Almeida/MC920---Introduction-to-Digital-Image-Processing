from PIL import Image
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def aplicar_ocr(imagem_path):
    img = Image.open(imagem_path).convert('L')
    texto = pytesseract.image_to_string(img)
    num_chars = len(texto.replace(" ", "").replace("\n", ""))
    return texto.strip(), num_chars

def main():
    if len(sys.argv) != 3:
        print("Uso: python analiseOCR.py nome_imagem modo")
        print("Exemplo: python analiseOCR.py sample1.png hough")
        sys.exit(1)

    nome_imagem = sys.argv[1]  #Ex: sample1.png
    modo = sys.argv[2].lower() #Ex: hough ou projecao

    caminho_original = f'images/{nome_imagem}'
    caminho_corrigida = f'images/outputs/{modo}/{nome_imagem}'

    print(f"Analisando OCR para a imagem original: {caminho_original}")
    texto_original, chars_original = aplicar_ocr(caminho_original)
    print(f"\n[OCR - Original] ({chars_original} caracteres):\n{texto_original}")

    print(f"\nAnalisando OCR para a imagem corrigida: {caminho_corrigida}")
    texto_corrigida, chars_corrigida = aplicar_ocr(caminho_corrigida)
    print(f"\n[OCR - Corrigida] ({chars_corrigida} caracteres):\n{texto_corrigida}")

    diferenca = chars_corrigida - chars_original
    print("\nResumo da análise:")
    print(f"Caracteres reconhecidos antes:  {chars_original}")
    print(f"Caracteres reconhecidos depois: {chars_corrigida}")
    print(f"Diferença: {diferenca:+} caracteres")


main()
