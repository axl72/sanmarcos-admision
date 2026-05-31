from scrapers import SanMarcosGenericScraper
from interfaces import Scraper
from pathlib import Path
from parser import Parser

OUTPUT_DIR = Path("./results/")


parser = Parser()
args = parser.parse()

def scrape(scraper: Scraper):
    
    df = scraper.scrape()
    file_name = f"{scraper}.csv"
    df.to_csv(OUTPUT_DIR / file_name, index=False)
    print(f"{file_name} scrapeado correctamente")


if __name__ == "__main__":
    dict_process = {
        "2023-1": {
        "url": "https://admision.unmsm.edu.pe/Res_20231_Area_A/index.html",
        "process_name": "resultados-admision-2023-1"},

        "2023-2": {
          "url": "https://admision.unmsm.edu.pe/WebsiteExa_20232/",
          "process_name": "resultados-admision-2023-2" 
        },

        "2024-1": {
            "url": "https://admision.unmsm.edu.pe/Website20241/",
            "process_name": "resultados-admision-2024-1"
        },

        "2024-2": {
            "url": "https://admision.unmsm.edu.pe/Website20242/",
            "process_name": "resultados-admision-2024-2"
        },

        "2025-1": {
            "url": "https://admision.unmsm.edu.pe/Website20251/",
            "process_name": "resultados-admision-2025-1"
        },

        "2025-2": {
            "url": "https://admision.unmsm.edu.pe/Website20252GeneralA/index.html",
            "process_name": "resultados-admision-2025-2"
        },

        "2026-1": {
            "url": "https://admision.unmsm.edu.pe/Website20261/",
            "process_name": "resultados-admision-2026-1"
        },

        "2026-2": {
            "url": "https://admision.unmsm.edu.pe/Website20262/",
            "process_name": "resultados-admision-2026-2"
        },
    }

    url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/index.html"

    args = parser.parse()
    args_process_name = args.process_name
    process = dict_process[args_process_name]
    scraper = SanMarcosGenericScraper(process["url"], process["process_name"])
    scrape(scraper)

