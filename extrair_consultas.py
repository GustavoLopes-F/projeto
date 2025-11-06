import pdfplumber
import re
import json
import os

PASTA_PDFS = "relatorios"
ARQUIVO_SAIDA = "consultas.json"

def extrair_dados_pdf(caminho_pdf):
    dados = []
    data_atual = None
    local_atual = None

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if not texto:
                continue

            linhas = texto.split("\n")

            for linha in linhas:
                
                # Captura data
                data_match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", linha)
                if data_match:
                    data_atual = data_match.group(0)
                    continue

                # Captura local
                if re.search(r"HOSPITAL|CLINICA|INSTITUTO|CSVIR|POLICLINICA|CENTRO", linha, re.IGNORECASE):
                    local_atual = linha.strip()
                    continue

                # Captura telefone e nome
                tel_match = re.findall(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", linha)
                if tel_match:
                    if "não informado" in linha.lower():
                        linha = re.sub(r"Não informado\(a\)", "", linha, flags=re.IGNORECASE)
                    
                    partes = linha.split(tel_match[0])
                    nome = partes[0].strip()

                    # 🔧 Remove números antes do nome (ex: "78995 vitor" -> "vitor")
                    nome = re.sub(r"^\d+\s*", "", nome)

                    for tel in tel_match:
                        dados.append({
                            "data": data_atual,
                            "local": local_atual,
                            "nome": nome,
                            "telefone": tel,
                        })
    return dados

def processar_pdfs(pasta):
    todos_dados = []
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho = os.path.join(pasta, arquivo)
            print(f"📄 Processando {arquivo}...")
            dados = extrair_dados_pdf(caminho)
            todos_dados.extend(dados)

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(todos_dados, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Concluído! {len(todos_dados)} registros salvos em '{ARQUIVO_SAIDA}'.")

if __name__ == "__main__":
    processar_pdfs(PASTA_PDFS)
