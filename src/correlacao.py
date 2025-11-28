import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PASTA_COMPARACAO = os.path.join(BASE_DIR, "fotos", "comparacao")
PASTA_RESULTADO = os.path.join(BASE_DIR, "fotos", "resultado_correlacao")

def verificar_e_carregar(caminho_imagem):
  imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
  if imagem is None:
    raise FileNotFoundError(f"Erro ao carregar imagem: {caminho_imagem}")
  return imagem

def extrair_descritores(imagem):
  detector = cv2.SIFT_create()
  pontos_chave, descritores = detector.detectAndCompute(imagem, None)
  return pontos_chave, descritores

def encontrar_correspondencias(descritores_a, descritores_b):
  FLANN_INDEX_KDTREE = 1
  parametros_indice = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
  parametros_busca = dict(checks=50)
  casador = cv2.FlannBasedMatcher(parametros_indice, parametros_busca)
  pares = casador.knnMatch(descritores_a, descritores_b, k=2)
  aprovados = []
  for melhor, segundo in pares:
    if melhor.distance < 0.7 * segundo.distance:
      aprovados.append(melhor)
  return pares, aprovados

def desenhar_resultado(img_a, kp_a, img_b, kp_b, matches_filtrados, espessura_linha=2):
  # Converte para BGR para desenhar em cores
  vis_a = cv2.cvtColor(img_a, cv2.COLOR_GRAY2BGR)
  vis_b = cv2.cvtColor(img_b, cv2.COLOR_GRAY2BGR)

  altura = max(vis_a.shape[0], vis_b.shape[0])
  largura_total = vis_a.shape[1] + vis_b.shape[1]
  canvas = np.zeros((altura, largura_total, 3), dtype=np.uint8)
  canvas[0:vis_a.shape[0], 0:vis_a.shape[1]] = vis_a
  canvas[0:vis_b.shape[0], vis_a.shape[1]:vis_a.shape[1]+vis_b.shape[1]] = vis_b

  desloc_x = vis_a.shape[1]

  for m in matches_filtrados:
    pt_a = tuple(map(int, kp_a[m.queryIdx].pt))
    pt_b = tuple(map(int, kp_b[m.trainIdx].pt))
    pt_b_desloc = (pt_b[0] + desloc_x, pt_b[1])

    cv2.circle(canvas, pt_a, 4, (0, 255, 0), -1)
    cv2.circle(canvas, pt_b_desloc, 4, (0, 255, 0), -1)
    cv2.line(canvas, pt_a, pt_b_desloc, (255, 0, 0), espessura_linha, cv2.LINE_AA)

  return canvas

def analisar_pares(caminho_a, caminho_b, destino):
  img_a = verificar_e_carregar(caminho_a)
  img_b = verificar_e_carregar(caminho_b)

  kp_a, desc_a = extrair_descritores(img_a)
  kp_b, desc_b = extrair_descritores(img_b)

  todos, bons = encontrar_correspondencias(desc_a, desc_b)

  print(f"Total de matches encontrados: {len(todos)}")
  print(f"Matches bons (aprovados): {len(bons)}")

  visualizacao = desenhar_resultado(img_a, kp_a, img_b, kp_b, bons)

  os.makedirs(os.path.dirname(destino), exist_ok=True)
  cv2.imwrite(destino, visualizacao)
  print("Imagem salva em:", destino)

  if len(bons) >= 15:
    print("Provavelmente é o mesmo local.")
  else:
    print("Provavelmente não é o mesmo local.")

  return len(bons)

def obter_duas_imagens_da_pasta(pasta):
  extensoes = (".jpg", ".jpeg", ".png", ".bmp")
  arquivos = [
    os.path.join(pasta, nome)
    for nome in sorted(os.listdir(pasta))
    if nome.lower().endswith(extensoes)
  ]
  if len(arquivos) < 2:
    raise FileNotFoundError("É necessário pelo menos duas imagens em fotos/comparacao")
  return arquivos[0], arquivos[1]

def executar_correlacao():
  print("\nCorrelacionador de imagens (SIFT + FLANN)\n")

  if not os.path.isdir(PASTA_COMPARACAO):
    raise FileNotFoundError("Pasta fotos/comparacao não encontrada")

  img1, img2 = obter_duas_imagens_da_pasta(PASTA_COMPARACAO)
  destino = os.path.join(PASTA_RESULTADO, "resultado.jpg")

  print("Processando...")
  analisar_pares(img1, img2, destino)
  print("Concluído. Resultado salvo em fotos/resultado_correlacao/resultado.jpg")

if __name__ == "__main__":
  executar_correlacao()