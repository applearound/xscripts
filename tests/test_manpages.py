import logging

from xscripts.manpages import fetch_manpages_info, save_manpages_info_to_csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_fetch_manpages_info():
    manpages_info = fetch_manpages_info()

    logger.debug("Fetched manpage section number: %d", len(manpages_info))
    assert len(manpages_info) > 0


def test_save_manpages_info_to_csv():
    manpages_info = fetch_manpages_info()
    save_manpages_info_to_csv("manpages.csv", manpages_info)
