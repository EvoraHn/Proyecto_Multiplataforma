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

        self.producto_db = ProductoDB("laminas.db")

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
        #self.inventario_list.connect(self.Mostrar_producto)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self.insert)

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

    
    def insert(self):
        """ Insertar los valores del formulario a la tabla de producto """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_tipoCategoria.text() or
                self.input_descripcion.text() !=""):
            categoria = (self.input_tipoCategoria.text(),self.input_descripcion.text())
                        
            try:
                self.producto_db.add_categoria(categoria)
                QMessageBox.information(
                    self, "Información", "su categoria se agreg correctamente")
                self.inventario_list.clear()
                self.set_categoria_list()
                self.limpiar()
                #self.close()
                #self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de agregar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")

    def set_categoria_list(self):
        """ Obtiene las tuplas de Productos y las muestra en la lista """
        productos = self.producto_db.get_all_categoria()

        if productos:
            for  categoria in productos:
                self.inventario_list.addItem(
                    "{0} -- {1} -- {2}".format(categoria[1], categoria[2],categoria[2]))
     
     
    def Mostrar_categoria(self):
        """ Muestra los atributos del producto que se encuentra seleccionado """
        categoria = self.inventario_list.currentItem().text()
        id = categoria.split(" --- ")[0]

        producto = self.producto_db.Obtener_Producto(id)
        
        if producto:
            #se deshabilitan los textbox
            self.Bloquear_Inputs(True)
            idCategoria =  categoria[0]
            tipoCategoria =  categoria[1]
            descripcion =  categoria[2]
            #se muestran los valores en los text
            self.input_idCategoria.setText((str(idCategoria)))
            self.input_nombre.setText((str(tipoCategoria)))
            self.input_descripcion.setText((str(descripcion)))

    def limpiar(self):
        self.input_idCategoria.setText("")
        self.input_tipoCategoria.setText("")
        self.input_descripcion.setText("")

class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        self.connection = self.create_connection(db_filename)
        self.producto_query = """ CREATE TABLE IF NOT EXISTS categoria (
                                    idCategoria integ unique primary key,
                                    NombreCategoria TEXT,
                                    Descripcion TEXT
                                  );
                                """
        self.create_table(self.connection, self.producto_query)
    
    
    def create_connection(self, db_filename):
        """ Crear una conexión a la base de datos SQLite """
        conn = None

        # Tratar de conectarse con SQLite y crear la base de datos
        try:
            conn = sqlite3.connect(db_filename)
            print("Conexión realizada. Versión {}".format(sqlite3.version))
        except Error as e:
            print(e)
        finally:
            return conn

    def create_table(self, conn, query):
        """
        Crea una tabla basado en los valores de query.
        :param conn: Conexión con la base de datos.
        :param query: La instrucción CREATE TABLE.
        :return:
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query)
        except Error as e:
            print(e)

    def add_categoria(self, categoria):
        """
        Realiza una inserción a la tabla de categoria.
        :param producto: Una estructura que contiene
                         los datos de categoria.
        :return:
        """
        sqlInsert = """
                    INSERT INTO categoria(
                         idCategoria, NombreCategoria, Descripcion)
                     VALUES(?, ?)
                    """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, categoria)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)
    
    
    def get_all_categoria(self):
        """ Obtiene todas las tuplas de la tabla categoria """
        sqlQuery = " SELECT * FROM categoria ORDER BY ROWID ASC "

        try:
            cursor = self.connection.cursor()
            categoria = cursor.execute(sqlQuery).fetchall()

            return categoria
        except Error as e:
            print(e)

        return None


def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()