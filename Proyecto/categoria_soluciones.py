# -*- coding: utf8 -*-
# Programa: categoria.py
# Objetivo: Desarrollar un CRUD con PyQt5
# Autor: Fernando Martinez Diaz
# Fecha: 16/marzo/2020

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import sqlite3
from sqlite3 import Error


categoria_Id = None


class Main(QWidget):
    """ Ventana principal de la Aplicación. """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CATEGORIA")
        self.setGeometry(400, 100, 700, 550)
        self.UI()
        self.show()
        # Crear o abrir la conexión a la base de datos
        self.categoria_db = CategoriaDB("categoria.db")
    
    def main_desing(self):
        """ Diseño principal de la aplicación. """
        self.employee_list = QListWidget()
        self.btn_new = QPushButton("Categoria")
        self.btn_new.clicked.connect(self.add_employee)
        