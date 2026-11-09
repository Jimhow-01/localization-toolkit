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
        "DE": []
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
                    if row[lang]:  # Verifica se a tradução não está vazia
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
        "DE": "Game_DE_ger.po"
    }

    # Cria os arquivos .po para cada idioma
    for lang, entries in traducoes.items():
        if entries:
            nome_arquivo_po = f"{caminho_saida}/{nome_arquivos[lang]}"
            try:
                with open(nome_arquivo_po, 'w', encoding='utf-8') as f:
                    # Cabeçalho específico por idioma
                    if lang == "FR":
                        f.write('# Game French translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: fr\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=2; plural=(n > 1);\\n"\n\n')
                    
                    elif lang == "DE":
                        f.write('# Game German translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: de\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n\n')
                    
                    elif lang == "RU":
                        f.write('# Game Russian translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: ru\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\\n"\n\n')
                    
                    
                    elif lang == "ES":
                        f.write('# Game Spanish translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: es\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n\n')

                    elif lang == "PT":
                        f.write('# Game Portuguese translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: pt\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n\n')
                        
                    elif lang == "PL":
                        f.write('# Game Polish translation.\n'
                                 "# Copyright (c) All Rights Reserved.\n\n"
                                 '#\n'
                                 'msgid ""\n'
                                 'msgstr ""\n'
                                 '"Project-Id-Version: Game\\n"\n'
                                 '"POT-Creation-Date: 2024-10-07 13:30\\n"\n'
                                 '"PO-Revision-Date: 2024-10-23 17:17+0200\\n"\n'
                                 '"Language-Team: \\n"\n'
                                 '"Language: pl\\n"\n'
                                 '"MIME-Version: 1.0\\n"\n'
                                 '"Content-Type: text/plain; charset=UTF-8\\n"\n'
                                 '"Content-Transfer-Encoding: 8bit\\n"\n'
                                 '"Plural-Forms: nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\\n"\n\n')


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
