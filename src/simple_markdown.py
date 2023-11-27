from typing import List
from enum import Enum

MdCellAlign = Enum('MdCellAlign', 'left center right')

CELL_ALIGN = {MdCellAlign.left: '-----', MdCellAlign.right: '----:', MdCellAlign.center: ':---:'}
CELL_DELIM = '|'


def h1(s: str) -> str:
    return f"# {s}"


def h2(s: str) -> str:
    return f"## {s}"


def h3(s: str) -> str:
    return f"### {s}"


def h4(s: str) -> str:
    return f"#### {s}"


def h5(s: str) -> str:
    return f"##### {s}"


def h6(s: str) -> str:
    return f"###### {s}"


def hr() -> str:
    return "___"


def bold(s: str) -> str:
    return f"**{s}**"


def italic(s: str) -> str:
    return f"_{s}_"


def ul(s: str) -> str:
    return f"- {s}"


def line(s: str) -> str:
    return f"{s}  "


def link(text: str, url: str) -> str:
    return f"[{text}]({url})"


def table_header(field_names: List[str], cells_align: List[str] = None) -> str:
    if not isinstance(field_names, list):
        raise TypeError('field_names is not a list')

    aligns = cells_align or [MdCellAlign.left for _ in range(len(field_names))]
    header = f" {CELL_DELIM} ".join(field_names)
    cells_alignment = f" {CELL_DELIM} ".join([CELL_ALIGN[align] for align in aligns])
    return f"{CELL_DELIM} {header} |\n| {cells_alignment} {CELL_DELIM}"


def table_row(row: List[str]) -> str:
    try:
        trow = f" {CELL_DELIM} ".join([cell.replace('\n', '<br/>') for cell in row])
    except AttributeError as e:
        print("===")
        print(e)
        print(row)
        raise e
    return f"{CELL_DELIM} {trow} {CELL_DELIM}"


def blockquote(s: str) -> str:
    return f"> {s}"
