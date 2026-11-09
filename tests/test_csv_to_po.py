"""Testes do ciclo CSV -> .po -> CSV do kit de localizacao.

Cobrem o que o kit promete: cabecalho .po valido por idioma (quoted, com
Plural-Forms corretos para as linguas de tres formas) e o caminho de volta
preservando Key, SourceLocation, referencia `#:` e msgctxt.
"""
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "l10n"))

# csv_to_po abre Tkinter e usa messagebox ao gerar; stub para rodar sem GUI.
_stub = types.SimpleNamespace(
    showinfo=lambda *a, **k: None,
    showerror=lambda *a, **k: pytest.fail(f"geracao falhou: {a}"),
)
import tkinter  # noqa: E402

tkinter.messagebox = _stub
sys.modules["tkinter.messagebox"] = _stub

import csv_to_po  # noqa: E402

CSV_CONTENT = (
    "Key,SourceLocation,msgctxt,msgid,PT,ES,FR,RU,PL,DE\n"
    "UI_START,ui.cpp:12,action,Start,Iniciar,Empezar,Démarrer,Начать,Start,Start\n"
    "UI_ITEMS,ui.cpp:20,plural,{0} items,{0} itens,{0} artículos,{0} éléments,"
    "{0} элементов,{0} przedmiotów,{0} Elemente\n"
)


@pytest.fixture
def csv_file(tmp_path):
    f = tmp_path / "trad.csv"
    f.write_text(CSV_CONTENT, encoding="utf-8")
    return f


def headers_of(po_path):
    """Retorna as linhas de header (entre msgstr "" e a primeira linha em branco)."""
    lines = po_path.read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(lines) if l == 'msgstr ""') + 1
    out = []
    while i < len(lines) and lines[i].strip():
        out.append(lines[i])
        i += 1
    return out


class TestGeneratedPoFiles:
    EXPECTED = [
        "Game_PT_por-BR.po",
        "Game_ES_spa.po",
        "Game_FR_fre.po",
        "Game_RU_rus.po",
        "Game_PL_pol.po",
        "Game_DE_ger.po",
    ]

    def test_generates_one_file_per_language(self, csv_file, tmp_path):
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        produced = sorted(p.name for p in tmp_path.glob("Game_*.po"))
        assert produced == sorted(self.EXPECTED)

    @pytest.mark.parametrize("name", EXPECTED)
    def test_header_lines_are_quoted_gettext_syntax(self, csv_file, tmp_path, name):
        """Header invalido (sem aspas) e rejeitado por msgfmt - bug que ja existiu aqui."""
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        for line in headers_of(tmp_path / name):
            assert line.startswith('"'), f"{name}: linha de header sem aspas: {line!r}"

    @pytest.mark.parametrize("name", EXPECTED)
    def test_header_declares_language_and_utf8(self, csv_file, tmp_path, name):
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        header = "\n".join(headers_of(tmp_path / name))
        assert "charset=UTF-8" in header
        assert "Language:" in header

    def test_plural_forms_are_correct_for_ru_and_pl(self, csv_file, tmp_path):
        """Russo e polones tem tres formas plurais; a regra precisa estar no header."""
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        for name in ("Game_RU_rus.po", "Game_PL_pol.po"):
            header = "\n".join(headers_of(tmp_path / name))
            assert "nplurals=3" in header
            assert "n%10" in header  # regra de duas/decenas

    def test_plural_forms_are_binary_for_the_others(self, csv_file, tmp_path):
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        for name in ("Game_PT_por-BR.po", "Game_ES_spa.po", "Game_FR_fre.po", "Game_DE_ger.po"):
            header = "\n".join(headers_of(tmp_path / name))
            assert "nplurals=2" in header


class TestEntryMetadata:
    def test_entries_keep_key_source_location_and_msgctxt(self, csv_file, tmp_path):
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        body = (tmp_path / "Game_PT_por-BR.po").read_text(encoding="utf-8")
        assert "#. Key:\tUI_START" in body
        assert "#. SourceLocation:\tui.cpp:12" in body
        assert "#:\tui.cpp:12" in body
        assert 'msgctxt "action"' in body
        assert 'msgid "Start"' in body
        assert 'msgstr "Iniciar"' in body

    def test_every_language_gets_its_own_translation(self, csv_file, tmp_path):
        csv_to_po.gerar_po_de_traducao(str(csv_file), str(tmp_path))
        expected = {
            "Game_ES_spa.po": "Empezar",
            "Game_FR_fre.po": "Démarrer",
            "Game_RU_rus.po": "Начать",
            "Game_DE_ger.po": "Start",
        }
        for name, translation in expected.items():
            body = (tmp_path / name).read_text(encoding="utf-8")
            assert f'msgstr "{translation}"' in body, name
