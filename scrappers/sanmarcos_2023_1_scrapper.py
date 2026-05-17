import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pandas import DataFrame
import pandas as pd
from urllib.parse import urljoin

class Scrapper20231:
    def __init__(self, url:str):
        self.url = url
        self.process_name = "resultados-admision-2023-1"

    def _scrape_page(self, base_url):
        """Función encargada de scrappear los nodos hijos del árbol de links"""
        r = requests.get(base_url)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        data = []
        for row in rows:
            if row.find("th"):
                continue
                
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if not cols or all( c == "" for c in cols):
                continue

            data.append(cols)
        return data


    def _get_links(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            full = urljoin(url, a["href"])
            links.append(full)
        return links

    def _crawl(self, seed_url):
        visited = set()
        to_visit = [seed_url]
        print(f"Link base: {seed_url}")
        final_data = [] 

        while to_visit:
            url = to_visit.pop()

            if url in visited:
                continue

            visited.add(url)
            links = self._get_links(url) # Obtiene los links de la hoja
            links = [l for l in links if l.startswith("http") and l not in visited] # Se queda con los links absolutos
            print(f"Link scrapeado: ", url)

            if not links: # si no hay links significa que es un nodo hoja
                data = self._scrape_page(url)
                final_data.extend(data)
                print(f"Cantidad de datos agregados: filas({len(data)}) - columnas({len(data[0])})")
                print(f"Datos totales: {len(final_data)}")
                continue


            if not links:
                final_data.append(self._scrape_page(url))
                continue

            for link in links: # Agrega a los links por visitar los nuevos links
                to_visit.append(link)

        return final_data


    def scrape(self) -> DataFrame:
        data = self._crawl(self.url)
        df = pd.DataFrame(data, columns=["CODIGO", "NOMBRES Y APELLIDOS", "ESCUELA PROFESIONAL", "PUNTAJE", "ORDEN DE MÉRITO", "RESULTADO"])
        return df

    def __str__(self):
        return self.process_name



if __name__ == "__main__":
    url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/A/011/0.html"
    # url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/"
    scrapper = Scrapper20231(url)
    result = scrapper._scrape_page(url)
    print("Cantidad de filas: ", len(result))
