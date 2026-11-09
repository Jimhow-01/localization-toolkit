import csv
import threading
import tkinter as tk
from tkinter import filedialog, messagebox


# Função para identificar e salvar as chaves, SourceLocation, hashtags, msgid e traduções no CSV
def identificar_e_salvar_dados(diretorio, nome_arquivo_txt, nome_arquivo_txt_pt, nome_arquivo_txt_es, nome_arquivo_txt_fr, nome_arquivo_txt_ru, nome_arquivo_txt_pl, nome_arquivo_txt_ge, nome_csv):
    caminho_arquivo = f"{diretorio}/{nome_arquivo_txt}"
    caminho_arquivo_pt = f"{diretorio}/{nome_arquivo_txt_pt}"
    caminho_arquivo_es = f"{diretorio}/{nome_arquivo_txt_es}"
    caminho_arquivo_fr = f"{diretorio}/{nome_arquivo_txt_fr}"
    caminho_arquivo_ru = f"{diretorio}/{nome_arquivo_txt_ru}"
    caminho_arquivo_pl = f"{diretorio}/{nome_arquivo_txt_pl}"
    caminho_arquivo_ge = f"{diretorio}/{nome_arquivo_txt_ge}"
    
    chaves = []
    locations = []
    hashtags = []
    msgctxts = []
    msgids = []
    traducoes = {
        "PT": {},
        "ES": {},
        "FR": {},
        "RU": {},
        "PL": {},
        "DE": {}
    }
    
    try:
        # Leitura do arquivo original
        def ler_arquivo(caminho):
            with open(caminho, encoding='utf-8') as f:
                for i, linha in enumerate(f):
                    if i < 15:  # Ignora as 15 primeiras linhas
                        continue
                    if "#. Key:" in linha:
                        partes = linha.split(":")
                        chave = partes[1].strip() if len(partes) > 1 else ""
                        chaves.append(chave)

                    elif "#. SourceLocation:" in linha:
                        partes = linha.split(":")
                        location = partes[1].strip() if len(partes) > 1 else ""
                        locations.append(location)

                    elif "#:" in linha:
                        partes = linha.split(":")
                        hashtag = partes[1].strip() if len(partes) > 1 else ""
                        hashtags.append(hashtag)

                    elif "msgctxt" in linha:
                        partes = linha.split('"')
                        msgctxt = partes[1].strip() if len(partes) > 1 else ""
                        msgctxts.append(msgctxt)

                    elif "msgid" in linha:
                        partes = linha.split('"')
                        msgid = partes[1].strip() if len(partes) > 1 else ""
                        msgids.append(msgid)

        # Leitura do arquivo original
        ler_arquivo(caminho_arquivo)

        # Função auxiliar para ler traduções alinhadas
        def ler_traducao(caminho):
            msgstrs = {}
            chave_atual = ""
            with open(caminho, encoding='utf-8') as f:
                for i, linha in enumerate(f):
                    if i < 15:  # Ignora as 15 primeiras linhas
                        continue

                    if "#. Key:" in linha:
                        partes = linha.split(":")
                        chave_atual = partes[1].strip() if len(partes) > 1 else ""

                    elif "msgstr" in linha and chave_atual:
                        partes = linha.split('"')
                        msgstr = partes[1].strip() if len(partes) > 1 else ""
                        msgstrs[chave_atual] = msgstr
            return msgstrs

        # Leitura de traduções de cada arquivo de idioma
        traducoes["PT"] = ler_traducao(caminho_arquivo_pt)
        traducoes["ES"] = ler_traducao(caminho_arquivo_es)
        traducoes["FR"] = ler_traducao(caminho_arquivo_fr)
        traducoes["RU"] = ler_traducao(caminho_arquivo_ru)
        traducoes["PL"] = ler_traducao(caminho_arquivo_pl)
        traducoes["DE"] = ler_traducao(caminho_arquivo_ge)

        # Salvar dados no CSV
        with open(nome_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Key", "SourceLocation", "#", "msgctxt", "msgid", "PT", "ES", "FR", "RU", "PL", "DE"])
            
            max_len = max(len(chaves), len(locations), len(hashtags), len(msgctxts), len(msgids))
            for i in range(max_len):
                linha = [
                    chaves[i] if i < len(chaves) else "",
                    locations[i] if i < len(locations) else "",
                    hashtags[i] if i < len(hashtags) else "",
                    msgctxts[i] if i < len(msgctxts) else "",
                    msgids[i] if i < len(msgids) else "",
                    traducoes["PT"].get(chaves[i], "") if i < len(chaves) else "",
                    traducoes["ES"].get(chaves[i], "") if i < len(chaves) else "",
                    traducoes["FR"].get(chaves[i], "") if i < len(chaves) else "",
                    traducoes["RU"].get(chaves[i], "") if i < len(chaves) else "",
                    traducoes["PL"].get(chaves[i], "") if i < len(chaves) else "",
                    traducoes["DE"].get(chaves[i], "") if i < len(chaves) else "",
                ]
                writer.writerow(linha)

        messagebox.showinfo("Sucesso", f"Planilha '{nome_csv}' criada com sucesso.")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Um dos arquivos de tradução não foi encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para selecionar a pasta e executar o processamento
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta contendo os arquivos .po")
    if pasta:
        nome_arquivo_txt = "Game_DE_ger.po"
        nome_arquivo_txt_pt = "Game_PT_por-BR.po"
        nome_arquivo_txt_es = "Game_ES_spa.po"
        nome_arquivo_txt_fr = "Game_FR_fre.po"
        nome_arquivo_txt_ru = "Game_RU_rus.po"
        nome_arquivo_txt_pl = "Game_PL_pol.po"
        nome_arquivo_txt_ge = "Game_DE_ger.po"
        nome_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if nome_csv:
            # Executa o processamento em uma nova thread
            threading.Thread(target=identificar_e_salvar_dados, args=(pasta, nome_arquivo_txt, nome_arquivo_txt_pt, 
                                                                      nome_arquivo_txt_es, nome_arquivo_txt_fr, nome_arquivo_txt_ru, 
                                                                      nome_arquivo_txt_pl, nome_arquivo_txt_ge, nome_csv)).start()

# Interface Tkinter
def iniciar_interface():
    root = tk.Tk()
    root.title("Selecionar Pasta para Processamento")
    root.geometry("400x200")

    label = tk.Label(root, text="Clique no botão para selecionar a pasta onde estão os arquivos .po", pady=20)
    label.pack()

    btn_selecionar = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
    btn_selecionar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    # Iniciar interface
    iniciar_interface()
