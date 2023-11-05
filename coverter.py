import textwrap

import pandas as pd


def colorify(x: str) -> str:
    if "[f]" in x:
        c = "255, 0, 0"
    elif "[mi]" in x:
        c = "0, 0, 255"
    elif "[ma]" in x:
        c = "79, 216, 186"
    elif "[n]" in x:
        c = "0, 255, 0"
    else:
        return x
    return f'<span style="color: rgb({c});">{x}</span>'


def ankify(d: pd.DataFrame) -> str:
    d["deck"] = d.apply(
        lambda r: f"Czech::Czech Step by Step A1-A2::Lekce-{r['lesson']:02}", axis=1
    )
    d["notetype"] = "Basic (and reversed card)"
    d["tags"] = d.apply(lambda r: f"lekce-{r['lesson']:02} strana-{r['page']:03}", axis=1)
    d["front"] = d["czech"].apply(colorify)
    d["back"] = d["english"]

    header = textwrap.dedent("""\
    #separator:tab
    #html:true
    #deck column:1
    #notetype column:2
    #tags column:3
    """)
    body = d[["deck", "notetype", "tags", "front", "back"]].to_csv(
        sep="\t", header=False, index=False, encoding="utf8", lineterminator="\n"
    )
    return header + body


if __name__ == "__main__":
    fp_in = "Glossary.tsv"
    fp_out = "anki-deck.tsv"

    d = pd.read_csv(fp_in, sep="\t")
    content_out = ankify(d)
    with open(fp_out, "w", encoding="utf8") as f:
        f.write(content_out)
