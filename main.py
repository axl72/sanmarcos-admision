from scrappers import Scrapper20231
from interfaces import Scraper
from pathlib import Path

OUTPUT_DIR = Path("./results/")

def scrape(scraper: Scraper):
    
    df = scraper.scrape()
    file_name = f"{scraper}.csv"
    df.to_csv(OTPUT_DIR / file_name, index=False)
    print(f"{file_name} scrapeado correctamente")


if __name__ == "__main__":
    url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/index.html"
    scraper = Scrapper20231(url)
    scrape(scraper)

