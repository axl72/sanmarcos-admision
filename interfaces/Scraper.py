from typing import Protocol

class Scraper(Protocol):
    def scrape(self) -> str:
        ...
