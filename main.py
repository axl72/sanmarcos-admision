from scrappers import Scrapper20231

if __name__ == "__main__":
    url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/index.html"
    scrapper = Scrapper20231(url)
    data = scrapper.scrape()
    print(data.head())

