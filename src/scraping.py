# -*- coding: utf-8 -*-

# Modulos
from tabulate import tabulate
from urllib import request

from bs4 import BeautifulSoup
from colorama import Fore

# Producto a buscar
producto = input("Ingrese el nombre de un producto: ").replace(" ","%20")


class Scraping:
     def __init__(self, producto):
          self.producto = producto
     
     # Generar links de busqueda
     def generar_link(self):
          # Paginas a cosultar
          toledo = "https://toledodigital.com.ar/storeview_saavedra/catalogsearch/result//?q="+self.producto
          dia = "https://diaonline.supermercadosdia.com.ar/busca/?ft="+self.producto
          return ([toledo,dia])

     # Consultar la pagina
     def consulta(self, links):
          html_toledo = request.urlopen(links[0]).read().decode()
          html_dia = request.urlopen(links[1]).read().decode()
          return ([html_toledo, html_dia])

     # Precios Toledo
     def filtrar_toledo(self,html_toledo): 
          i, list_prices = 0, []
          soup = BeautifulSoup(html_toledo, features="html.parser")
          prices = soup("span",{"class", "price"})
          titles = soup("a",{"class", "product-item-link"})
          for title in titles:
               list_prices.append([title.string, prices[i].string])                 
               i = i + 1

          print(tabulate(list_prices, headers=[Fore.BLUE + "Producto en TOLEDO", "Precio"])) #  Print table

     # Precios Dia
     def filtrar_dia(self, html_dia):
          i, list_prices = 0, []
          soup = BeautifulSoup(html_dia, features="html.parser")
          prices = soup.body("span",{"class", "best-price"})
          titles = soup.body("div", {"class", "product-name"})
          for title in titles:
               list_prices.append([title.a["title"], prices[i].string]) 
               i = i + 1
     
          print(tabulate(list_prices, headers=[Fore.RED + "Producto en DIA", "Precio"])) #  Print table

     # Iniciar scraping
     def iniciar(self):
          links = self.generar_link()
          htmls = self.consulta(links)
          self.filtrar_toledo(htmls[0])
          self.filtrar_dia(htmls[1])
          
precios = Scraping(producto)
precios.iniciar()


