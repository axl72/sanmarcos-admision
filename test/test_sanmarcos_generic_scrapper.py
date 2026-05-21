import unittest
from unittest.mock import patch, MagicMock
# Reemplaza 'tu_archivo_script' por el nombre real de tu archivo .py (sin el .py)
from scrapers import SanMarcosGenericScrapper 

path = "scrappers.sanmarcos_generic_scrapper" # Reemplaza con el path correcto a tu clase

class TestSanMarcosScrapper(unittest.TestCase):

    def setUp(self):
        """Este método se ejecuta antes de CADA test. Ideal para inicializar el objeto."""
        self.url_base = "https://admision.unmsm.edu.pe/Website20262/A/091/results.html"
        self.scrapper = SanMarcosGenericScrapper(self.url_base, process_name="test_proceso")

    @patch(path + ".requests.get") # Simulamos requests.get
    def test_scrape_pagina_normal(self, mock_get):
        """Caso 1: Probar que procesa correctamente una fila HTML normal estándar"""
        html_normal = """
        <table>
            <tr>
                <td>123456</td>
                <td>PEREZ GOMEZ, JUAN</td>
                <td>MEDICINA</td>
                <td>950.500</td>
                <td>1</td>
                <td>ALCANZO VACANTE</td>
            </tr>
        </table>
        """
        # Configuramos el falso 'requests.get' para que devuelva nuestro HTML
        mock_response = MagicMock()
        mock_response.text = html_normal
        mock_get.return_value = mock_response

        # Ejecutamos solo el método que queremos testear
        resultado = self.scrapper._scrape_page(self.url_base)

        # Asertos (Validaciones)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][0], "123456")
        self.assertEqual(resultado[0][1], "PEREZ GOMEZ, JUAN")
        self.assertEqual(resultado[0][3], "950.500")

    # @patch(path + ".requests.get")
    # def test_scrape_pagina_ofuscada(self, mock_get):
    #     """Caso 2: Probar el HTML con Base64 y atributos data-score extraído de tu bug"""
    #     html_ofuscado = """
    #     <table>
    #         <tr class="">
    #             <td class="text-center dt-type-numeric">656550</td>
    #             <td><span class="obfuscated" data-auth="QUJBRCBTQUxHQURPLCBTT0ZJQSBFU1RSRUxMQQ=="></span></td>
    #             <td class="text-center"><span class="obfuscated" data-auth="QURNSU5JU1RSQUNJw5NO"></span></td>
    #             <td class="text-center" data-score="461.375"></td>
    #             <td class="text-center" data-merit=""></td>
    #             <td class="text-center"></td>
    #         </tr>
    #     </table>
    #     """
    #     mock_response = MagicMock()
    #     mock_response.text = html_ofuscado
    #     mock_get.return_value = mock_response

    #     resultado = self.scrapper._scrape_page(self.url_base)

    #     # Verificaciones del comportamiento con decodificación
    #     self.assertEqual(len(resultado), 1)
    #     self.assertEqual(resultado[0][0], "656550")
    #     self.assertEqual(resultado[0][1], "ABAD SALGADO, SOFIA ESTRELLA")  # Verificamos Base64 decodificado
    #     self.assertEqual(resultado[0][2], "ADMINISTRACIÓN")               # Verificamos tildes UTF-8
    #     self.assertEqual(resultado[0][3], "461.375")                     # Verificamos data-score

    # @patch(path + ".requests.get")
    # def test_ignora_filas_cabecera_y_subtitulos(self, mock_get):
    #     """Caso 3: Probar que el filtro descarta basura de la tabla (colspan o th)"""
    #     html_con_basura = """
    #     <table>
    #         <tr><th>CODIGO</th><th>POSTULANTE</th></tr> 
    #         <tr><td colspan="5">EDUCACIÓN BÁSICA REGULAR (EBR)</td></tr> 
    #     </table>
    #     """
    #     mock_response = MagicMock()
    #     mock_response.text = html_con_basura
    #     mock_get.return_value = mock_response

    #     resultado = self.scrapper._scrape_page(self.url_base)

    #     # Debería ignorar ambas filas y devolver una lista vacía
    #     self.assertEqual(len(resultado), 0)

if __name__ == "__main__":
    unittest.main()