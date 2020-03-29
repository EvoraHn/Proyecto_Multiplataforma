# -*- coding: utf8 -*-
# Programa: Inventario
# Objetivo: 
# Autor: Saudy Zavala 
# Fecha: 26/marzo/2020

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import sqlite3
from sqlite3 import Error
from PIL import Image

employee_id = None


class Main(QWidget):
    """ Ventana principal de la Aplicación. """

    def __init__(self):
        super().__init__()
        self.setGeometry(450, 150, 750, 600)
        self.UI()
        self.show()

    def UI(self):
        """ Definimos los objetos que componen la interfaz de usuario. """
        self.main_desing()
        self.layouts()
  

    def main_desing(self):
        """ Diseño principal de la aplicación. """
        self.inventario_list = QListWidget()
        self.btn_new = QPushButton("Agregar")
        self.label_id = QLabel("ID Categoria: ")
        self.input_id = QLineEdit()
        self.label_name = QLabel("Nombre: ")
        self.input_name = QLineEdit()
        self.label_descripcion = QLabel("Descripcion: ")
        self.input_descripcion = QLineEdit()

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()
        self.top_layout = QVBoxLayout()
        self.left_bottom_layout = QFormLayout()

        # Agregar los layouts hijos al layout padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout, 40)
        self.main_layout.addLayout(self.right_main_layout, 60)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.left_bottom_layout)

        # Agregar widgets a los layouts
        self.right_top_layout.addWidget(self.inventario_list)
        self.right_bottom_layout.addWidget(self.btn_new)
        self.left_bottom_layout.addRow(self.label_id, self.input_id)
        self.left_bottom_layout.addRow(self.label_name, self.input_name)
        self.left_bottom_layout.addRow(self.label_descripcion, self.input_descripcion)


        # Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

   



def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()