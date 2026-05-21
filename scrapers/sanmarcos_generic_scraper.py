import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pandas import DataFrame
import pandas as pd
from urllib.parse import urljoin

class SanMarcosGenericScraper:
    def __init__(self, url:str, process_name:str = None):
        self.url = url

        if not process_name:
            raise Exception("Debe proporcionar un nombre para el proceso de scrapping")

        self.process_name = process_name

    def _scrape_page(self, base_url) -> list:
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
                
            cols = []
            for td in row.find_all("td"):
                text = td.get_text(strip=True)

                span_ofuscated = td.find("span", class_="obfuscated")
                if not text and span_ofuscated and span_ofuscated.has_attr("data-auth"):
                    try:
                        base64_text = span_ofuscated["data-auth"]
                        text = base64.b64decode(base64_text).decode("utf-8")
                    except Exception as e:
                        text = ""

                
                if not text and td.has_attr("data-score"):
                    text = td["data-score"]
                if not text and td.has_attr("data-merit"):
                    text = td["data-merit"]
                
                cols.append(text)
            
            if not cols or all(c == "" for c in cols):
                continue

            if len(cols) < 5:
                continue

            data.append(cols)
        print(f"Datos scrapeados en {base_url}: filas({len(data)}) - columnas({len(data[0]) if data else 0})")
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
                if  data:
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
        columns= ["CODIGO", "NOMBRES Y APELLIDOS", 
                 "ESCUELA PROFESIONAL", "PUNTAJE", 
                 "ORDEN DE MÉRITO", "RESULTADO", 
                 "ESCUELA SEGUNDA OPCION"] if len(data[0]) == 7 else ["CODIGO", "NOMBRES Y APELLIDOS",
                    "ESCUELA PROFESIONAL", "PUNTAJE", "ORDEN DE MÉRITO"]
        df = pd.DataFrame(data, )
        return df

    def __str__(self):
        return self.process_name



if __name__ == "__main__":
    # url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/A/011/0.html"
    url = "https://admision.unmsm.edu.pe/Res_20231_Area_A/"
    scrapper = SanMarcosScrapper(url, "resultados-admision-2023-1")
    result = scrapper.scrape()
    print("Cantidad de filas: ", len(result))

