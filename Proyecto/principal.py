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

        self.title = QLabel("Buscar una Lamina Educativa : ")
        self.input_busqueda = QLineEdit()
        #self.image = QLabel()

        self.lista_producto = QListWidget()
        self.btn_inventario = QPushButton("Inventario")
        #self.btn_new.clicked.connect(self.add_employee)
        self.btn_ventas = QPushButton("Ventas")
        self.btn_compras = QPushButton("Compras")
        self.btn_buscar = QPushButton("Buscar Lámina")

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        # Main layouts
        self.principal_layout = QVBoxLayout()
        self.arriba_layout = QVBoxLayout()
        self.abajo_layout = QFormLayout()
        self.izquierda_layout = QHBoxLayout()
        self.derecha_layout = QHBoxLayout()
     

        # Agregar los widgets (childrens) al main_layout
        self.principal_layout.addLayout(self.arriba_layout)
        #self.principal_layout.addLayout(self.abajo_layout)
        self.principal_layout.addLayout(self.izquierda_layout)
        self.principal_layout.addLayout(self.derecha_layout)

        # Agregar los widgets al arriba_layout
        self.arriba_layout.addWidget(self.title)
        self.arriba_layout.addWidget(self.input_busqueda)
        self.arriba_layout.addWidget(self.btn_buscar)

        #Agregar los botones a izquierda_layout 
        self.izquierda_layout.addWidget(self.btn_inventario)
        self.izquierda_layout.addWidget(self.btn_compras)
        self.izquierda_layout.addWidget(self.btn_ventas)

        # Agregar el listado a derecha_layout
        self.derecha_layout.addWidget(self.lista_producto)
        

        # Agregar widgets a los layouts
        #self.abajo_layout.addRow(self.btn_inventario,self.lista_producto)
        #self.abajo_layout.addRow(self.btn_compras,self.btn_ventas)


        # Colocar el layout principal en la ventana principal
        self.setLayout(self.principal_layout)

def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
