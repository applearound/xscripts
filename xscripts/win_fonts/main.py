import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

import requests
from bs4 import BeautifulSoup

WIN11_FONTS_LIST_PAGE_URL: Final[str] = (
    "https://learn.microsoft.com/en-us/typography/fonts/windows_11_font_list"
)
WIN11_SYS_FONTS_FOLDER: Final[str] = "C:\\Windows\\Fonts"


@dataclass
class FontDef:
    font_family: str = field()
    font_name: str = field()
    file_name: str = field()
    version: str = field()


def fetch_win11_fonts_list() -> dict[str, list[FontDef]]:
    web = requests.get(WIN11_FONTS_LIST_PAGE_URL)
    soup = BeautifulSoup(web.text, "html.parser")

    tables = soup.select(".content table")
    if not tables:
        raise ValueError("No tables found on the page.")

    first_table = tables[0]

    rows = first_table.select("tr")[2:]
    font_family = ""
    font_dict = defaultdict(list)
    for row in rows:
        cols = row.select("td")

        font_family_empty = cols[0].text.strip()
        if font_family_empty:
            font_family = font_family_empty

        font_name = cols[1].text.strip()
        file_name = cols[2].text.strip()
        version = cols[3].text.strip()

        font_dict[font_family].append(
            FontDef(
                font_family=font_family,
                font_name=font_name,
                file_name=file_name,
                version=version,
            )
        )

    return font_dict


def copy_win11_fonts(font_dict: dict[str, list[FontDef]], dest: str = ".") -> None:
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)

    win_sys_fonts_folder_path = Path(WIN11_SYS_FONTS_FOLDER)

    for font_family, fonts in font_dict.items():
        family_dest_path = dest_path / font_family
        family_dest_path.mkdir(parents=True, exist_ok=True)

        for font_def in fonts:
            file_name = font_def.file_name

            system_font_path = win_sys_fonts_folder_path / file_name
            if system_font_path.is_file():
                shutil.copy(system_font_path, family_dest_path)
            else:
                print(f"{font_family}: file {file_name} not found.")
