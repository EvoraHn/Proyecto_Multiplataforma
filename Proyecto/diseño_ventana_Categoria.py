# -*- coding: utf8 -*-
# Programa: diseño_ventana_Categotia.py
# Objetivo: Desarrollar un CRUD con PyQt5
# Autor: Fernando Martinez Diaz
# Fecha: 16/marzo/2020



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
        self.setWindowTitle("DISEÑO CATEGORIA")
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
        #top layout widgets
        self.title = QLabel("MainCategoria")
        self.move(15,10)

        #posterior de los top layout
        self.label_id = QLabel("CATEGORIA: ")
        self.input_id = QLineEdit()
        self.label_name = QLabel("Tipo de categoria: ")
        self.input_name = QLineEdit()

 
        #self.btn_new.clicked.connect(self.add_employee)
        self.btn_inventario = QPushButton("regresar")
        self.btn_ventas = QPushButton("SELECCIONAR")
        self.btn_compras = QPushButton("AGREGAR")
        """ BOTON CATEGORIA FERNANDO MARTINEZ. """
        self.btn_Categoria = QPushButton("ELIMINAR")
        
        # Crear o abrir la conexión a la base de datos
        

    

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

        # Layouts estos sirven  parara tectos y cajas 
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()

        # Agregar los layouts hijos al layout padre
  
        self.right_main_layout.addLayout(self.right_top_layout,50)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.left_main_layout.addLayout(self.left_bottom_layout)
        self.left_main_layout.addLayout(self.left_top_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_main_layout)

        # Agregar widgets a los layouts

        self.right_top_layout.addWidget(self.title)
        self.right_top_layout.addWidget(self.label_id)
        self.right_bottom_layout.addWidget(self.btn_inventario)
        self.right_top_layout.addWidget(self.label_name)
        self.right_bottom_layout.addWidget(self.btn_ventas)
        self.right_bottom_layout.addWidget(self.btn_compras)
        self.right_bottom_layout.addWidget(self.btn_Categoria)

        # Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
