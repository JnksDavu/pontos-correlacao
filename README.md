Pontos de correlação

Visão geral
- O script lê duas imagens da pasta `fotos/comparacao` e gera uma visualização dos pontos correspondentes na pasta `fotos/resultado_correlacao`.
- Usa SIFT para detectar e descrever pontos e FLANN para fazer a correspondência. O objetivo é indicar se as duas imagens provavelmente mostram o mesmo local, com base na quantidade de correspondências filtradas.

Estrutura de pastas
- `fotos/comparacao`: coloque aqui pelo menos duas imagens (`.jpg`, `.jpeg`, `.png`, `.bmp`). O script usa as duas primeiras em ordem alfabética.
- `fotos/resultado_correlacao`: pasta de saída. Será criada automaticamente. O arquivo gerado é `resultado.jpg` com as correspondências desenhadas.

Preparação do ambiente (Windows PowerShell v5.1)
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

Observações
- Para melhores resultados, use imagens com conteúdo rico em textura.
- Se houver mais de duas imagens na pasta de comparação, apenas as duas primeiras em ordem alfabética serão utilizadas.

# pontos-correlacao