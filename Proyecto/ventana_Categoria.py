# -*- coding: utf8 -*-
# Programa: Categoria Programa
# Objetivo: 
# Autor: Fernando Martinez 
# Fecha: 29/marzo/2020

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
        self.label_buscar = QLabel("Buscar: ")
        self.input_buscar = QLineEdit()
        self.inventario_list = QListWidget()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_buscar = QPushButton("BUSCAR")
        self.label_idCategoria = QLabel("ID Categoria: ")
        self.input_idCategoria = QLineEdit()
        self.label_tipoCategoria = QLabel("Tipo Categoria: ")
        self.input_tipoCategoria = QLineEdit()
        self.label_descripcion = QLabel("Descripcion: ")
        self.input_descripcion = QLineEdit()
        self.label_vacia = QLabel(" ")

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout =  QFormLayout()
        self.right_bottom_layout = QHBoxLayout()
        self.top_layout = QVBoxLayout()
        self.left_bottom_layout = QHBoxLayout()

        # Agregar los layouts hijos al layout padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_main_layout)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.left_bottom_layout)

        # Agregar widgets a los layouts
        self.left_bottom_layout.addWidget(self.inventario_list)
        self.right_bottom_layout.addWidget(self.btn_agregar)
        self.right_bottom_layout.addWidget(self.btn_editar)
        self.right_bottom_layout.addWidget(self.btn_eliminar)
        #self.bottom_layout.addRow("", self.btn_agregarProducto, self. btn_editarProducto, self.btn_eliminarProducto)
        self.right_top_layout.addRow(self.label_buscar, self.input_buscar)
        self.right_top_layout.addRow("", self.btn_buscar)
        self.right_top_layout.addRow("", self.label_vacia)
        self.right_top_layout.addRow("", self.label_vacia)
        self.right_top_layout.addRow("", self.label_vacia)
        self.right_top_layout.addRow(self.label_idCategoria, self.input_idCategoria)
        self.right_top_layout.addRow(self.label_tipoCategoria, self.input_tipoCategoria)
        self.right_top_layout.addRow(self.label_descripcion, self.input_descripcion)
        #self.right_top_layout.addRow(self.btn_agregar, self.btn_editar, self.btn_eliminar)


        # Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

   



def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()