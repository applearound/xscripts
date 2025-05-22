import csv
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Final
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


LINUX_MAN_PAGES_INFO_SITE_HOST_PREFIX: Final[str] = "https://man7.org/linux/man-pages/"
LINUX_MAN_PAGES_INFO_SITE: Final[str] = (
    f"{LINUX_MAN_PAGES_INFO_SITE_HOST_PREFIX}dir_all_by_section.html"
)
LINK_CONTENT_PATTERN_STR: Final[str] = r"(.+?)\((.+)\)"
DESCRIPTION_SUB_PATTERN_STR: Final[str] = r"^-\s*"

LINK_CONTENT_PATTERN: re.Pattern = re.compile(LINK_CONTENT_PATTERN_STR)
DESCRIPTION_SUB_PATTERN: re.Pattern = re.compile(DESCRIPTION_SUB_PATTERN_STR)

logger = logging.getLogger(__name__)

@dataclass
class ManPageInfo:
    section: str
    name: str
    description: str
    url: str


def fetch_manpages_info() -> dict[str, ManPageInfo]:
    site_html = __fetch_site()

    soup = BeautifulSoup(site_html, "html.parser")

    result = defaultdict(list)
    for pre_tag in soup.find_all("pre"):
        for info in __parse_pre_tag(pre_tag):
            result[info.section].append(info)

    return result


def save_manpages_info_to_csv(file_path: str, manpages_info: list[ManPageInfo]) -> None:
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["section", "name", "description", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _, infos in manpages_info.items():
            for info in infos:
                writer.writerow(
                    {
                        "section": info.section,
                        "name": info.name,
                        "description": info.description,
                        "url": urljoin(LINUX_MAN_PAGES_INFO_SITE_HOST_PREFIX, info.url),
                    }
                )


def __fetch_site(site_url: str = LINUX_MAN_PAGES_INFO_SITE) -> str:
    # Fetch man pages info from the site
    response = requests.get(site_url)

    # Check if the request was successful, and raise an error if not
    response.raise_for_status()

    return response.text


def __parse_pre_tag(pre_tag: Tag) -> list[ManPageInfo]:
    manpage_info_list = []

    for link_tag in pre_tag.find_all("a"):
        try:
            manpage_info_list.append(__parse_link(link_tag))
        except Exception as e:
            logger.error(f"Failed to resolve: {link_tag} - {str(e)}")
            continue

    return manpage_info_list


def __parse_link(link: Tag) -> ManPageInfo:
    link_text = link.get_text()
    name_part, section_part = LINK_CONTENT_PATTERN.match(link_text).groups()

    description = link.next_sibling.strip()
    description = DESCRIPTION_SUB_PATTERN.sub("", description)

    return ManPageInfo(
        section=section_part,
        name=name_part.strip(),
        description=description,
        url=link["href"],
    )
