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
#from producto import ProductoDB


class Main(QWidget):
    """ Ventana principal de la Aplicación. """

    def __init__(self):
        super().__init__()
         # Crear o abrir la conexión a la base de datos
        self.producto_db = ProductoDB("laminas.db")

        self.setWindowTitle("Pantalla Principal")
        self.setGeometry(550, 150, 650, 600)
        self.UI()
        self.show()
       

    def UI(self):
        """ Definimos los objetos que componen la interfaz de usuario. """
        self.main_desing()
        self.layouts()
        self.set_producto_list()

    def main_desing(self):
        """ Diseño principal de la aplicación. """

        self.title = QLabel("Buscar una Lámina Educativa : ")
        self.input_busqueda = QLineEdit()
        #self.image = QLabel()

        self.lista_producto = QListWidget()
        self.btn_inventario = QPushButton("Inventario")
        self.btn_inventario.clicked.connect(self.add_producto)
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

    def add_producto(self):
        """ Inicia el formulario de ingreso de datos del empleado """
        self.new_producto = AddProducto(self.producto_db)
        self.close()
        
    def set_producto_list(self):
        """ Obtiene las tuplas de empleados y las muestra en la lista """
        productos = self.producto_db.get_all_producto()

        if productos:
            for producto in productos:
                self.lista_producto.addItem(
                    "{0} --- {1}".format(producto[1], producto[2]))

class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        self.connection = self.create_connection(db_filename)
        self.producto_query = """ CREATE TABLE IF NOT EXISTS producto (
                                    id_producto integer PRIMARY KEY,
                                    nombre text NOT NULL,
                                    descripcion text,
                                    categoria integer NOT NULL,
                                    proveedor integer NOT NULL
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

    def add_producto(self, producto):
        """
        Realiza una inserción a la tabla de empleados.
        :param producto: Una estructura que contiene
                         los datos del producto.
        :return:
        """
        sqlInsert = """
                    INSERT INTO producto(
                         nombre, descripcion,
                        categoria, proveedor)
                     VALUES(?, ?, ?, ?)
                    """


        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, producto)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def get_all_producto(self):
        #ORDER BY ROWID ASC
        """ Obtiene todas las tuplas de la tabla producto """

        sqlQuery = "select * from producto "

        try:
            cursor = self.connection.cursor()
            productos = cursor.execute(sqlQuery).fetchall()

            return productos
        except Error as e:
            print(e)

        return None

class AddProducto(QWidget):
    """ Muestra la ventana para agregar nuevos empleados. """

    def __init__(self, producto_db):
        super().__init__()
        # Conexión a la base de datos
        self.producto_db = producto_db
        self.setWindowTitle("Agregar un producto")
        self.setGeometry(450, 150, 750, 600)
        self.UI()
        self.show()

    def UI(self):
        """ Cargar los layouts de diseño de la ventana """
        self.mainDesing()
        self.layouts()

    def mainDesing(self):
        """ Crear los widgets que conforman la interfaz """
        # Top Layout Widgets
        self.title = QLabel("Agregar producto ")
        self.image = QLabel()
        self.image.setPixmap(QPixmap("images/orden.png"))

        # Bottom Layout Widgets
        #Empieza Un label y textbox con valores por defecto
        self.label_idProducto= QLabel("Id Producto: ")
        self.input_idProducto = QLineEdit()
        self.input_idProducto.setPlaceholderText("00000000")
        #termina label y textbox 
        self.label_nombre= QLabel("Nombre : ")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Lámina Educativa")

        self.label_descripcion= QLabel("Descripción : ")
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Esta es una lámina educativa")

        self.label_categoria= QLabel("Categoría : ")
        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("00000")

        self.label_proveedor= QLabel("Proveedor : ")
        self.input_proveedor = QLineEdit()
        self.input_proveedor.setPlaceholderText("00000")

        self.btn_agregarProducto = QPushButton("Agregar")
        self.btn_agregarProducto.clicked.connect(self.insert)

        self.btn_editarProducto = QPushButton("Editar")
        #self.btn_editarProducto.clicked.connect(self.update_producto)

        self.btn_eliminarProducto = QPushButton("Eliminar")
        #self.btn_eliminarProducto.clicked.connect(self.delete_producto)

    def layouts(self):
        """ Define la estructura de los elementos en pantalla """
        # Main layouts
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()

        # Agregar los widgets (childrens) al main_layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        # Agregar los widgets al top layout
        #self.top_layout.addWidget(self.title)
        #self.top_layout.addWidget(self.image)

        # Agregar los widgets al bottom layout
        self.bottom_layout.addRow(self.label_idProducto, self.input_idProducto)
        self.bottom_layout.addRow(self.label_nombre, self.input_nombre)
        self.bottom_layout.addRow(self.label_descripcion, self.input_descripcion)
        self.bottom_layout.addRow(self.label_categoria, self.input_categoria)
        self.bottom_layout.addRow(self.label_proveedor, self.input_proveedor)
        self.bottom_layout.addWidget(self.btn_agregarProducto)
        self.bottom_layout.addWidget(self.btn_editarProducto)
        self.bottom_layout.addWidget(self.btn_eliminarProducto)
                

        


        # Establecer el layout principal de la ventana
        self.setLayout(self.main_layout)

    def upload_image(self):
        """ Permite subir una imagen de perfil del empleado """
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(
            self, "Agregar foto perfil", "", "Imágenes (*.jpg *.png)")

        # Si el usuario acepta el cuadro de diálogo seleccionando
        # una imagen.
        if ok:
            self.fullpath = os.path.basename(self.filename)
            # Implementar PIL (Python Imaging Library) para abrir
            # la imagen, cambiarle el tamaño y almacenarla.
            image = Image.open(self.filename)
            image = image.resize(size)
            image.save(f"images/{self.fullpath}")

    def insert(self):
        """ Insertar los valores del formulario a la tabla de producto """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_nombre.text() or
                self.input_proveedor.text() or self.input_categoria.text() != ""):
            producto = (self.input_nombre.text(),
                        self.input_descripcion.text(), self.input_categoria.text(),
                        self.input_proveedor.text())

            try:
                self.producto_db.add_producto(producto)
                QMessageBox.information(
                    self, "Información", "producto agregado correctamente")
                self.close()
                self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de agregar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")





def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
