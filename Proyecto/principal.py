# -*- coding: utf8 -*-
# Programa: Laminas Educativas (sistema de Inventario)
# Objetivo: Organizar laminas educativas
# Autor: Grupo BPB
# Fecha: 24/marzo/2020

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import sqlite3
from sqlite3 import Error



class Main(QWidget):
    """ Ventana principal de la Aplicación. """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pantalla Principal")
        self.setGeometry(450, 150, 750, 600)
        self.UI()
        self.show()
        # Crear o abrir la conexión a la base de datos
        #self.employee_db = EmployeeDB("employee.db")

    def UI(self):
        """ Definimos los objetos que componen la interfaz de usuario. """
        self.main_desing()
        self.layouts()

    def main_desing(self):
        """ Diseño principal de la aplicación. """
        self.lista_producto = QListWidget()
        self.btn_inventario = QPushButton("Inventario")
        #self.btn_new.clicked.connect(self.add_employee)
        self.btn_ventas = QPushButton("Ventas")
        self.btn_compras = QPushButton("Compras")

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.left_main_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.left_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()
        self.left_bottom_layout = QHBoxLayout()

        # Agregar los layouts hijos al layout padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.left_main_layout.addLayout(self.left_bottom_layout)
        self.left_main_layout.addLayout(self.left_top_layout)
        self.main_layout.addLayout(self.left_layout, 40)
        self.main_layout.addLayout(self.right_main_layout, 60)

        # Agregar widgets a los layouts
        self.right_top_layout.addWidget(self.lista_producto)
        self.right_bottom_layout.addWidget(self.btn_inventario)
        self.right_bottom_layout.addWidget(self.btn_ventas)
        self.right_bottom_layout.addWidget(self.btn_compras)

        # Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
