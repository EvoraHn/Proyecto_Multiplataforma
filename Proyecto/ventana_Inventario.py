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
#from Stock import ProductoDB


class Main(QWidget):
    """ Ventana principal de la Aplicación. """
       
    def __init__(self):
        super().__init__()
        # Crear o abrir la conexión a la base de datos
        self.producto_db = ProductoDB("laminas.db")

        self.setWindowTitle("Ventana Inventario")
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
        self.inventario_list.itemClicked.connect(self.Mostrar_Producto)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self.insert)

        self.btn_editar = QPushButton("Editar")

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.delete)

        self.btn_buscar = QPushButton("Buscar")

        self.label_id = QLabel("ID Producto: ")
        self.input_id = QLineEdit()

        self.label_notas = QLabel("Notas: ")
        self.input_notas = QLineEdit()

        self.label_precio_unitario = QLabel("Precio unitario: ")
        self.input_precio_unitario = QLineEdit()

        self.label_cantidad = QLabel("Cantidad: ")
        self.input_cantidad = QLineEdit()

        self.label_fecha_actualizacion = QLabel("Fecha de actualización : ")
        self.input_fecha_actualizacion = QLineEdit()

        self.label_vacia = QLabel(" ")

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        self.main_layout = QHBoxLayout()
        self.right_main_layout = QVBoxLayout()
        self.right_top_layout =  QFormLayout()
        self.right_bottom_layout = QHBoxLayout()
        self.top_layout = QVBoxLayout()
        self.left_bottom_layout = QHBoxLayout()

        # Agregar los layouts hijos al layout padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
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
        self.right_top_layout.addRow(self.label_id, self.input_id)
        self.right_top_layout.addRow(self.label_notas, self.input_notas)
        self.right_top_layout.addRow(self.label_precio_unitario, self.input_precio_unitario)
        self.right_top_layout.addRow(self.label_cantidad, self.input_cantidad)
        self.right_top_layout.addRow(self.label_fecha_actualizacion, self.input_fecha_actualizacion)

        #self.right_top_layout.addRow(self.btn_agregar, self.btn_editar, self.btn_eliminar)


        # Colocar el layout principal en la ventana principal
        self.setLayout(self.main_layout)

    def delete(self):
        """Elimina Una tupla, previamente seleccionada en el datagrid (lista)"""
        if self.inventario_list.selectedItems():
            stock = self.inventario_list.currentItem().text()
            id = stock.split(" --- ")[0]
            stock = self.producto_db. Obtener_Stock(id)
            yes = QMessageBox.Yes

            if stock:
                question_text = f"¿Está seguro de eliminar el producto {stock[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.producto_db.delete_producto(stock[0])
                    self.inventario_list.clear()
                    self.set_inventario_list()
                    self.limpiar()
                    QMessageBox.information(self, "Información", "¡Producto eliminado satisfactoriamente!")
                    

            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a eliminar")


    def insert(self):
        """ Insertar los valores del formulario a la tabla de Stock """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_id.text() or
                self.input_notas.text() or
                self.input_precio_unitario.text() or 
                 self.input_cantidad or self.input_fecha_actualizacion != ""):
            Stock = (self.input_id.text(),self.input_notas.text(),
                      self.input_precio_unitario.text(),
                       self.input_cantidad.text(),self.input_fecha_actualizacion.text())

            try:
                self.producto_db.add_Stock(Stock)
                QMessageBox.information(
                self, "Información", "inventario agregado correctamente")
                self.inventario_list.clear()
                self.set_Stock_list()
                self.limpiar()
                #self.close()
                #self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de agregar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")

    
    
    def Mostrar_Producto(self):
        """ Muestra los atributos del producto que se encuentra seleccionado """
        Stock = self.inventario_list.currentItem().text()
        id = Stock.split(" --- ")[0]

        Stock = self.producto_db.Obtener_Producto(id)
        
        if Stock:
            #se deshabilitan los textbox
            self.Bloquear_Inputs(True)
            id_producto =  Stock[0]
            notas =  Stock[1]
            precio_unitario =  Stock[2]
            cantidad =  Stock[3]
            fecha_actualizacion =  Stock[4]
            

            #se muestran los valores en los text
            self.input_id.setText((str(id_producto)))
            self.input_notas .setText((str(notas)))
            self.input_precio_unitario .setText((str(precio_unitario)))
            self.input_cantidad .setText((str(cantidad)))
            self.input_fecha_actualizacion .setText((str(fecha_actualizacion)))
            

    def limpiar(self):
        self.input_id.setText("")
        self.input_notas.setText("")
        self.input_precio_unitario .setText("")
        self.input_cantidad.setText("")
        self.input_fecha_actualizacion.setText("")




class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        self.connection = self.create_connection(db_filename)
        self.Stock_query = """ CREATE TABLE IF NOT EXISTS Stock (
                                    id_stock integer PRIMARY KEY autoincrement,
                                    id_producto integer,
                                    Notas text NOT NULL,
                                    Precio_unitario integer,
                                    Cantidad integer NOT NULL,
                                    Fecha_Actualizacion DATETIME,
                                    foreign key(id_producto) references producto(id_producto)
                                  );
                                """
        self.create_table(self.connection, self.Stock_query)

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

    def add_Stock(self, Stock):
        """
        Realiza una inserción a la tabla de empleados.
        :param producto: Una estructura que contiene
                         los datos del Stock.
        :return:
        """
        sqlInsert = """
                    INSERT INTO Stock(
                        id_producto, Notas, Precio_unitario,
                        Cantidad, Fecha_Actualizacion)
                     VALUES(?, ?, ?, ?, ?)
                    """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, Stock)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def update_Stock(self,productos):
        """
        Realiza una modificación a la tabla de Stock.
        :param producto: Una estructura que contiene
                         los datos del producto.
        :return:
        """
        sqlUpdate = """
                    UPDATE producto
                        SET = id_producto?,Notas = ?,Precio_unitario = ?
                        ,Cantidad = ?,Fecha_Actualizacion = ?
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlUpdate,productos)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def delete_Stock(self,codigo):
        """
        Realiza una eliminación a la tabla de producto.
        :param id: identificador para la tupla
        :return:
        """
        #QMessageBox.information("ESTE ES EL CODIGO",str(codigo))
        sqlDelete = """
                    delete from producto where id_producto = ?
                    """
        try:
           
            cursor = self.connection.cursor()
            cursor.execute(sqlDelete,(codigo,))
            self.connection.commit()
            return True
        except Error as e:
            print(e)

        return None


    def get_all_Stock(self):
        """ Obtiene todas las tuplas de la tabla producto """
        sqlQuery = " SELECT * FROM  Stock ORDER BY ROWID ASC "

        try:
            cursor = self.connection.cursor()
            productos = cursor.execute(sqlQuery).fetchall()

            return productos
        except Error as e:
            print(e)

        return None

    




def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


