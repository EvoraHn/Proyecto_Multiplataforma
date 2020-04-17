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


class ventana_Categoria(QWidget):
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
        self.set_categoria_list()

    def main_desing(self):
        """ Diseño principal de la aplicación. """
        self.label_buscar = QLabel("Buscar: ")
        self.input_buscar = QLineEdit()
        self.inventario_list = QListWidget()
        self.inventario_list.itemClicked.connect(self.Mostrar_Producto)

        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.clicked.connect(self.insert)

        self.btn_editar = QPushButton("Editar")
        self.btn_editar.clicked.connect(self.Habilitar_edicion)

        self.btn_Aceptar = QPushButton("Aceptar")
        self.btn_Aceptar.clicked.connect(self.aceptar_edicion)
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar_edicion)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.delete)

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
        self.botones_layout = QHBoxLayout()
        self.botonesForm_layout = QHBoxLayout()

        # Agregar los layouts hijos al layout padre
        self.right_main_layout.addLayout(self.right_top_layout)
        self.right_main_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_main_layout)
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.left_bottom_layout)
        self.main_layout.addLayout(self.botonesForm_layout)
        self.main_layout.addLayout(self.botones_layout)

        # Agregar widgets a los layouts
        self.left_bottom_layout.addWidget(self.inventario_list)
        self.right_bottom_layout.addWidget(self.btn_agregar)

        self.right_bottom_layout.addWidget(self.btn_editar)
        self.right_bottom_layout.addWidget(self.btn_eliminar)
        #self.bottom_layout.addRow("", self.btn_agregarProducto, self. btn_editarProducto, self.btn_eliminarProducto)

        self.botones_layout.addWidget(self.btn_Aceptar)
        self.btn_cancelar.hide()
        self.btn_Aceptar.hide()
        self.botones_layout.addWidget(self.btn_cancelar)
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
        """ Insertar los valores del formulario a la tabla de categoria """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_idCategoria.text() or self.input_tipoCategoria.text() or
                self.input_descripcion.text() !=""):
            categoria = (self.input_idCategoria.text(), self.input_tipoCategoria.text(),self.input_descripcion.text())
                        
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
    
    def Bloquear_Inputs(self,estado):
        """Deshabilita los QwidgetsInputs para solo dejarlos
         en modo lectura.
         
         parametro estado: recibe True o false para habilitar o no 
         los textbox (inputs) """

        #self.input_idProducto.setReadOnly(estado)
        self.input_idCategoria.setReadOnly(estado)
        self.input_tipoCategoria.setReadOnly(estado)
        self.input_descripcion.setReadOnly(estado)



    def delete(self):
        """Elimina Una tupla, previamente seleccionada en el datagrid (lista)"""
        if self.inventario_list.selectedItems():
            categoria = self.inventario_list.currentItem().text()
            id = categoria.split(" --- ")[0]
            categoria = self.producto_db.Obtener_Producto(id)
            yes = QMessageBox.Yes

            if categoria:
                question_text = f"¿Está seguro de eliminar el producto {categoria[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.producto_db.delete_producto(categoria[0])
                    self.inventario_list.clear()
                    self.set_categoria_list()
                    self.limpiar()
                    QMessageBox.information(self, "Información", "¡Producto eliminado satisfactoriamente!")
                    

            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a eliminar")

    def update(self,identificador):
        """ Editar los valores del formulario a la tabla de producto """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_idCategoria.text() or self.input_tipoCategoria.text() or
                self.input_descripcion.text() !=""):
            categoria = (self.input_tipoCategoria.text(),self.input_descripcion.text(),self.input_idCategoria.text())

            try:
                #QMessageBox.information(self,"este",stock)
                self.producto_db.update_categoria(categoria)
                QMessageBox.information(
                    self, "Información", "producto modificado correctamente")
                
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de editar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")
            
    def Habilitar_edicion(self):
        """verifica que tenga seleccionado un producto y habilita los txt"""
        if self.inventario_list.selectedItems():
            categoria = self.inventario_list.currentItem().text()
            id = categoria.split(" --- ")[0]
            categoria = self.producto_db.Obtener_Producto(id)
            yes = QMessageBox.Yes

            if categoria:
                question_text = f"¿Está seguro de editar la categoria {categoria[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.btn_editar.hide()
                    self.btn_agregar.hide()
                    self.btn_eliminar.hide()
                    self.Bloquear_Inputs(False)
                    self.btn_Aceptar.show()
                    self.btn_cancelar.show()
            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a editar")

    def aceptar_edicion(self):
        """Edita los parametros que han cambiado en los textbox"""
        if self.inventario_list.selectedItems():
            categoria = self.inventario_list.currentItem().text()
            id = categoria.split(" --- ")[0]
            stock = self.producto_db.Obtener_Producto(id)
            if stock:
                self.update(categoria[0])
                self.inventario_list.clear()
                self.set_categoria_list()
                self.limpiar()
            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")
        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a editar")


    def cancelar_edicion(self):
        """Cancela la edicion y envia al usuario a la ventana Principal"""
        self.inventario_list.clear()
        self.set_categoria_list()
        self.limpiar()
        self.Bloquear_Inputs(False)
        self.btn_editar.show()
        self.btn_agregar.show()
        self.btn_eliminar.show()
        self.btn_Aceptar.hide()
        self.btn_cancelar.hide()

    def Bloquear_Inputs(self,estado):
        """Deshabilita los QwidgetsInputs para solo dejarlos
         en modo lectura.
         
         parametro estado: recibe True o false para habilitar o no 
         los textbox (inputs) """

        #self.input_idProducto.setReadOnly(estado)
        self.input_idCategoria.setReadOnly(estado)
        self.input_tipoCategoria.setReadOnly(estado)
        self.input_descripcion.setReadOnly(estado)

    def set_categoria_list(self):
        """ Obtiene las tuplas de Productos y las muestra en la lista """
        productos = self.producto_db.get_all_categoria()

        if productos:
            for  categoria in productos:
                self.inventario_list.addItem(
                    "{0} --- {1} --- {2} ".format(categoria[0], categoria[1], categoria[2]))

    def Mostrar_Producto(self):
        """ Muestra los atributos del producto que se encuentra seleccionado """
        producto = self.inventario_list.currentItem().text()
        id = producto.split(" --- ")[0]

        QMessageBox.information(self,"este es el ID{0}",str (id[0]))
 
        producto = self.producto_db.Obtener_Producto(id)
        
        if producto:
            #se deshabilitan los textbox
            self.Bloquear_Inputs(True)
            idCategoria =  producto[0]
            tipoCategoria =  producto[1]
            descripcion =  producto[2] 
            #se muestran los valores en los text
            self.input_idCategoria.setText((str(idCategoria)))
            self.input_tipoCategoria.setText((str(tipoCategoria)))
            self.input_descripcion.setText((str(descripcion)))


    def limpiar(self):
        self.input_idCategoria.setText("")
        self.input_tipoCategoria.setText("")
        self.input_descripcion.setText("")
     
     
    #def Mostrar_Producto(self):
     #   """ Muestra los atributos del producto que se encuentra seleccionado """
      #  categoria = self.inventario_list.currentItem().text()
       # id = categoria.split("---")[0]
        #Codigo = id.split("---")[0]

        #QMessageBox.information(self,"este es el ID{0}",str (Codigo[0]))
        

        #categoria = self.producto_db.Obtener_Producto(id[0])
        
        
        
        #if categoria:
            #se deshabilitan los textbox
         #   self.Bloquear_Inputs(True)
          #  idCategoria =  categoria[0]
           # tipoCategoria =  categoria[1]
            #descripcion =  categoria[2]
            #se muestran los valores en los text
            #self.input_idCategoria.setText((str(idCategoria)))
            #self.input_tipoCategoria.setText((str(tipoCategoria)))
            #self.input_descripcion.setText((str(descripcion)))

    #def limpiar(self):
     #   self.input_idCategoria.setText("")
      #  self.input_tipoCategoria.setText("")
       # self.input_descripcion.setText("")

class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        self.connection = self.create_connection(db_filename)
        self.producto_query = """ CREATE TABLE IF NOT EXISTS categoria (
                                    idCategoria integ unique primary key,
                                    tipoCategoria TEXT,
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
                        idCategoria, tipoCategoria, Descripcion)
                     VALUES(?, ?, ?)
                    """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, categoria)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def Obtener_Producto(self, id):
        """
        Busca un producto mediante el valor del Código.

        param: Code: Codigo unico para identificar cada lámina.
        :return: Un arreglo con los atributos del producto.
        """
        sqlQuery = " SELECT * FROM categoria WHERE idCategoria = ?"

        try:
            cursor = self.connection.cursor()
            # fetchone espera que se retorne una tupla (1,)
            producto = cursor.execute(sqlQuery, (id,)).fetchone()

            return producto
        except Error as e:
            print(e)

        return None
    
    def update_categoria(self,categoria):
        """
        Realiza una modificación a la tabla de categoria.
        :param producto: Una estructura que contiene
                         los datos del producto.
        :return:
        """
        sqlUpdate = """
                    UPDATE categoria
                        SET tipoCategoria = ?
                        ,descripcion = ?
                        WHERE idCategoria = ?
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlUpdate,categoria)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)
    
    def delete_producto(self,codigo):
        """
        Realiza una eliminación a la tabla de categoria.
        :param id: identificador para la tupla
        :return:
        """
        #QMessageBox.information("ESTE ES EL CODIGO",str(codigo))
        sqlDelete = """
                    delete from categoria where idCategoria = ?
                    """
        try:
           
            cursor = self.connection.cursor()
            cursor.execute(sqlDelete,(codigo,))
            self.connection.commit()
            return True
        except Error as e:
            print(e)

        return None
    

        

    
    
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
    window = ventana_Categoria()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()