from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import sqlite3
from sqlite3 import Error
#from PIL import Image
#from Stock import ProductoDB



class AgregarProveedor(QWidget):

    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulario Proveedor")
        self.setGeometry(500,200,450,250)
        self.UI()
        self.show()
        


    def UI(self):
        self.mainDesing()
        self.layouts()

    def mainDesing(self):
        
        #Titulo del widget
        self.Titulo = QLabel("Agregar Distribuidor")
        self.Titulo.setFont(QFont('SansSerif',25))
        #self.Titulo.setText("LikeGreeks")


        self.imgUser = QLabel()
        self.imgUser.setPixmap(QPixmap("team.png"))

        #Botones del widget para clientes
        # widget para nombre
        self.lista_proveedor = QListWidget()
        self.label_nombre = QLabel("Nombre:")
        self.label_nombre.setFont(QFont("Arial",12))
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("---------------")
        self.input_nombre.setStyleSheet("background-color: white; color: Black;")

        # widget para telefono
        self.label_telefono = QLabel("Telefono:")
        self.label_telefono.setFont(QFont("Arial",12))
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("0000-0000")
        self.input_telefono.setStyleSheet("background-color: white; color: Black;")

        # widget para ID Proveedor
        self.label_IdProv = QLabel("ID del Proveedor:")
        self.label_IdProv.setFont(QFont("Arial",12))
        self.input_IdProv = QLineEdit()
        self.input_IdProv.setPlaceholderText("0000-0000-0000")
        self.input_IdProv.setStyleSheet("background-color: white; color: Black;")

        # widget para btn aceptar
        self.btn_Agregar = QPushButton("Agregar")
        #self.btn_Agregar.clicked.connect()
        self.btn_Agregar.setGeometry(5,50,50,15)
        self.btn_Agregar.setStyleSheet("font-size: 15px; background-color: gray; color: white;")

        # widget para btn regresar
        self.btn_regresar = QPushButton("Regresar")
        #self.btn_regresar.clicked.connect()
        self.btn_regresar.setGeometry(5,50,50,15)
        self.btn_regresar.setStyleSheet("font-size: 15px; background-color: gray; color: white;")

        # widget para btn regresar
        self.btn_eliminar = QPushButton("Eliminar")
        #self.btn_regresar.clicked.connect()
        self.btn_eliminar.setGeometry(5,50,50,15)
        self.btn_eliminar.setStyleSheet("font-size: 15px; background-color: gray; color: white;")



    def layouts(self):

        #Main layout
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.btn_layout = QFormLayout()
        self.left_bottom_layout = QHBoxLayout()

        #Agregar los widgets hijos al padre (main_layout)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addLayout(self.left_bottom_layout)


        #agregar los widgets al top_layout
        self.left_bottom_layout.addWidget(self.lista_proveedor)
        self.top_layout.addWidget(self.imgUser)
        self.top_layout.addWidget(self.Titulo)
        

        #agregar los widgets al btn_layout
        self.btn_layout.addRow(self.label_nombre, self.input_nombre)
        self.btn_layout.addRow(self.label_telefono, self.input_telefono)
        self.btn_layout.addRow(self.label_IdProv, self.input_IdProv)
        self.btn_layout.addRow("",self.btn_Agregar)
        self.btn_layout.addRow("",self.btn_regresar)
        self.btn_layout.addRow("",self.btn_eliminar)

        self.setLayout(self.main_layout)


def main():
    app = QApplication(sys.argv)
    window = AgregarProveedor()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
