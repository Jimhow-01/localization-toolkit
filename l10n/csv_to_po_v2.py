import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def gerar_po_de_traducao(nome_csv, caminho_saida):
    traducoes = {
        "PT": [],
        "ES": [],
        "FR": [],
        "RU": [],
        "PL": [],
        "DE": [],
        "EN": []  # Adiciona o idioma inglês
    }

    # Lê o arquivo CSV e organiza as traduções
    try:
        with open(nome_csv, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = row["Key"]
                source_location = row["SourceLocation"]
                msgctxt = row["msgctxt"]
                msgid = row["msgid"]
                
                # Para cada idioma, se a tradução estiver presente, adiciona ao dicionário
                for lang in traducoes.keys():
                    if lang == "EN":  # Para o idioma inglês
                        traducoes["EN"].append({
                            "key": key,
                            "source_location": source_location,
                            "msgctxt": msgctxt,
                            "msgid": msgid if msgid else "msgid \"\"",
                            "msgstr": msgid if msgid else ""  # msgstr será igual a msgid
                        })
                    elif row[lang]:  # Verifica se a tradução não está vazia
                        traducoes[lang].append({
                            "key": key,
                            "source_location": source_location,
                            "msgctxt": msgctxt,
                            "msgid": msgid if msgid else "msgid \"\"",
                            "msgstr": row[lang]
                        })

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo CSV não encontrado.")
        return
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        return

    # Mapeamento dos nomes dos arquivos .po
    nome_arquivos = {
        "PT": "Game_PT_por-BR.po",
        "ES": "Game_ES_spa.po",
        "FR": "Game_FR_fre.po",
        "RU": "Game_RU_rus.po",
        "PL": "Game_PL_pol.po",
        "DE": "Game_DE_ger.po",
        "EN": "Game_EN_eng.po"  # Nome do arquivo para inglês
    }

    # Cria os arquivos .po para cada idioma
    for lang, entries in traducoes.items():
        if entries:
            nome_arquivo_po = f"{caminho_saida}/{nome_arquivos[lang]}"
            try:
                with open(nome_arquivo_po, 'w', encoding='utf-8') as f:
                    # Cabeçalho específico por idioma
                    f.write(f'# Game {lang} translation.\n')
                    f.write("# Copyright (c) All Rights Reserved.\n\n")
                    f.write('msgid ""\n')
                    f.write('msgstr ""\n')
                    f.write('"Project-Id-Version: Game\\n"\n')
                    f.write('"POT-Creation-Date: 2024-10-07 13:30\\n"\n')
                    f.write('"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n')
                    f.write(f'"Language: {lang.lower()}\\n"\n')
                    f.write('"MIME-Version: 1.0\\n"\n')
                    f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
                    f.write('"Content-Transfer-Encoding: 8bit\\n"\n\n')

                    # Escreve as entradas de tradução
                    for entry in entries:
                        f.write(f"#. Key:\t{entry['key']}\n")
                        f.write(f"#. SourceLocation:\t{entry['source_location']}\n")
                        f.write(f"#:\t{entry['source_location']}\n")
                        f.write(f'msgctxt "{entry["msgctxt"]}"\n')
                        f.write(f'msgid "{entry["msgid"]}"\n')
                        f.write(f'msgstr "{entry["msgstr"]}"\n\n')

                messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo_po}' criado com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao criar '{nome_arquivo_po}': {e}")

# Função para selecionar o arquivo CSV e o diretório de saída
def selecionar_csv():
    nome_csv = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV Files", "*.csv")])
    if nome_csv:
        caminho_saida = filedialog.askdirectory(title="Selecione o diretório de saída")
        if caminho_saida:
            gerar_po_de_traducao(nome_csv, caminho_saida)

# Interface Tkinter
def iniciar_interface():
    root = tk.Tk()
    root.title("Gerar Arquivos .po de Tradução")
    root.geometry("400x200")

    label = tk.Label(root, text="Clique no botão para selecionar o arquivo CSV", pady=20)
    label.pack()

    btn_selecionar = tk.Button(root, text="Selecionar CSV", command=selecionar_csv)
    btn_selecionar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    # Iniciar interface
    iniciar_interface()
