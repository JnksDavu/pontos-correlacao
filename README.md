Pontos de correlação

Visão geral
- O script lê duas imagens da pasta `fotos/comparacao` e gera uma visualização dos pontos correspondentes na pasta `fotos/resultado_correlacao`.
- Usa SIFT para detectar e descrever pontos e FLANN para fazer a correspondência. O objetivo é indicar se as duas imagens provavelmente mostram o mesmo local, com base na quantidade de correspondências filtradas.

Estrutura de pastas
- `fotos/comparacao`: coloque aqui pelo menos duas imagens (`.jpg`, `.jpeg`, `.png`, `.bmp`). O script usa as duas primeiras em ordem alfabética.
- `fotos/resultado_correlacao`: pasta de saída. Será criada automaticamente. O arquivo gerado é `resultado.jpg` com as correspondências desenhadas.

Preparação do ambiente
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Execução
```powershell
python .\src\correlacao.py
```

Resultado
- O script imprime o total de correspondências encontradas e quantas foram aprovadas pelo filtro de razão (Lowe, 0.7).
- Salva `fotos/resultado_correlacao/resultado.jpg` com linhas entre pontos equivalentes.
- Exibe uma indicação simples baseada em um limiar de 15 correspondências aprovadas.

Como funciona
- Leitura: carrega duas imagens em tons de cinza de `fotos/comparacao`.
- Extração: detecta pontos e descritores via `cv2.SIFT_create().detectAndCompute`.
- Correspondência: usa `cv2.FlannBasedMatcher` com índice KD-Tree e busca com 50 verificações.
- Filtro: aplica a regra de razão (0.7) para aceitar correspondências mais confiáveis.
- Visualização: desenha as correspondências aprovadas com `cv2.drawMatches`.
- Saída: cria a pasta de resultado se necessário e grava `resultado.jpg`.

Resultados:

Imagens para comparação

  - Imagem 1:
  
<img width="1086" height="652" alt="image" src="https://github.com/user-attachments/assets/f3583a07-40f2-4271-a44d-8dba70b99a97" />

  - Imagem 2:

<img width="239" height="324" alt="image" src="https://github.com/user-attachments/assets/df8ee406-078c-4df6-a6b2-df542cdbd691" />

  Resultado:

<img width="321" height="328" alt="image" src="https://github.com/user-attachments/assets/0b750cec-6d20-49cb-9adb-555c1cbfdb76" />

Observações
- Para melhores resultados, use imagens com conteúdo rico em textura.
- Se houver mais de duas imagens na pasta de comparação, apenas as duas primeiras em ordem alfabética serão utilizadas.
