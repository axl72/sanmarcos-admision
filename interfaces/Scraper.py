from typing import Protocol
from pandas import DataFrame

class Scraper(Protocol):
    def scrape(self) -> DataFrame:
        ...
