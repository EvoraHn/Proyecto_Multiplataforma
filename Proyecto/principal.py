# -*- coding: utf8 -*-
# Programa: Laminas Educativas (sistema de Inventario)
# Objetivo: Organizar laminas educativas
# Autor: Grupo BPB
# Fecha: 24/marzo/2020
from PyQt5 import QtWidgets
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

        self.txtbuscar = QLabel("Buscar una Lámina Educativa : ")
        self.input_busqueda = QLineEdit()
        #self.image = QLabel()

        self.lista_producto = QListWidget()
        #self.lista_producto.clicked()
        self.btn_inventario = QPushButton("Inventario")
        self.btn_inventario.clicked.connect(self.add_producto)
        self.btn_ventas = QPushButton("Ventas")
        #self.btn_ventas.clicked.connect(self.hacer_venta)
        self.btn_compras = QPushButton("Compras")
        self.btn_compras.clicked.connect(self.hacer_compra)
        
        self.btn_buscar = QPushButton("Buscar Lámina")
        self.btn_buscar.clicked.connect(self.set_Buscar_list)
        self.label_cantidad= QLabel("Cantidad: ")
        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad")

    def layouts(self):
        """ Layouts que componen la aplicación. """
        # Layouts
        # Main layouts
        self.principal_layout = QVBoxLayout()
        self.arriba_layout = QVBoxLayout()
        self.left_layout = QFormLayout()
        self.abajo_layout = QVBoxLayout()
        self.izquierda_layout = QHBoxLayout()
        self.derecha_layout = QHBoxLayout()
     

        # Agregar los widgets (childrens) al main_layout
        self.principal_layout.addLayout(self.arriba_layout)

        #self.principal_layout.addLayout(self.abajo_layout)
        self.principal_layout.addLayout(self.izquierda_layout)
        self.principal_layout.addLayout(self.derecha_layout)
        self.principal_layout.addLayout(self.left_layout, 40)

        # Agregar los widgets al arriba_layout
        self.arriba_layout.addWidget(self.txtbuscar)
        self.arriba_layout.addWidget(self.input_busqueda)
        self.arriba_layout.addWidget(self.btn_buscar)

        #Agregar los botones a izquierda_layout 
        self.izquierda_layout.addWidget(self.btn_inventario)
        self.izquierda_layout.addWidget(self.btn_compras)
        self.izquierda_layout.addWidget(self.btn_ventas)

        # Agregar el listado a derecha_layout
        self.arriba_layout.addWidget(self.label_cantidad)
        self.arriba_layout.addWidget(self.input_cantidad)
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
    
    def set_Buscar_list(self):
        """ Obtiene las tuplas de empleados y las muestra en la lista """
       
        #print((self.input_busqueda.text()))
        if (self.input_busqueda.text()==""):
            print("<ERROR> Ingrese el nombre o descripcion para hacer la busqueda <ERROR>")
        else:
            productos = self.producto_db.Busqueda(self.input_busqueda.text())
        
        #productos = self.producto_db.Busqueda(self.input_busqueda.text())
        

        if productos:
            #limpia la lista y muestra los productos que cumplan con la condición
            self.lista_producto.clear()
            
            for producto in productos:
                self.lista_producto.addItem(
                    "{0} <-> {1} <-> {2}".format(producto[1], producto[2], producto[3]))

    def hacer_compra(self):
        """Hace una Compra"""


class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        
        self.connection = self.create_connection(db_filename)
        self.producto_query = """ CREATE TABLE IF NOT EXISTS producto (
                                    id_producto integer UNIQUE PRIMARY KEY,
                                    codigo text UNIQUE NOT NULL,
                                    nombre text NOT NULL,
                                    descripcion text,
                                    categoria integer NOT NULL,
                                    proveedor integer NOT NULL
                                  );
                                """
        self.create_table(self.connection, self.producto_query)
        
        
    def crear_vista_principal(self):
        """Genera la vista para el menú Principal"""
        self.vista_Principal_Query = """CREATE VIEW IF NOT EXIST vista_principal as 
        Select
            p.id_producto,
            p.codigo,
            p.nombre,
            s.Cantidad,
            pr.nombre_proveedor,
            c.nombre_categoria
        from 
            producto p
            INNER JOIN Categoria c ON s.idCategoria = p.categoria
            INNER JOIN proveedor pr ON idProveedor = P.proveedor
            INNER JOIN stock s ON p.id_producto = s.id_producto

            """


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
        Realiza una inserción a la tabla de producto.
        :param producto: Una estructura que contiene
                         los datos del producto.
        :return:
        """
        sqlInsert = """
                    INSERT INTO producto(
                         nombre,codigo, descripcion,
                        categoria, proveedor)
                     VALUES(?, ?, ?, ?,?)
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, producto)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)
        
    def update_producto(self,productos):
        """
        Realiza una modificación a la tabla de producto.
        :param producto: Una estructura que contiene
                         los datos del producto.
        :return:
        """
        sqlUpdate = """
                    UPDATE producto
                        SET codigo = ?,nombre = ?,descripcion = ?
                        ,categoria = ?,proveedor = ?
                        WHERE id_producto = ?
                        
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlUpdate,productos)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def delete_producto(self,codigo):
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
        

    def get_all_producto(self):
        """ Obtiene todas las tuplas de la tabla producto """

        sqlQuery = "select * from producto ORDER BY ROWID ASC "

        try:
            cursor = self.connection.cursor()
            productos = cursor.execute(sqlQuery).fetchall()

            return productos
        except Error as e:
            print(e)

        return None

    def Obtener_Producto(self, id):
        """
        Busca un producto mediante el valor del Código.

        param: Code: Codigo unico para identificar cada lámina.
        :return: Un arreglo con los atributos del producto.
        """
        sqlQuery = " SELECT * FROM producto WHERE codigo = ?"

        try:
            cursor = self.connection.cursor()
            # fetchone espera que se retorne una tupla (1,)
            producto = cursor.execute(sqlQuery, (id,)).fetchone()

            return producto
        except Error as e:
            print(e)

        return None

    def Busqueda(self,id):
        """ Obtiene todas las tuplas de la tabla producto que cumplan
         con la condicion en el campo nombre o descripción"""
        
        sqlQuery = """select * from producto where (nombre LIKE '%'
                    || ? || '%' or descripcion LIKE '%' || ? || '%') """
        print(id)
        try:
           
            cursor = self.connection.cursor()
            productos = cursor.execute(sqlQuery,(id,id,)).fetchall()
            
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
        self.setGeometry(150, 50, 750, 600)
        self.UI()
        self.show()

    def UI(self):
        """ Cargar los layouts de diseño de la ventana """
        self.mainDesing()
        self.layouts()
        self.set_producto_list()

    def mainDesing(self):
        """ Crear los widgets que conforman la interfaz """
        self.product_list = QListWidget()
        self.product_list.itemClicked.connect(self.Mostrar_Producto)
        # Top Layout Widgets
        self.title = QLabel("Agregar producto ")
        self.image = QLabel()
        self.image.setPixmap(QPixmap("images/orden.png"))

        # Bottom Layout Widgets
        #Empieza Un label y textbox con valores por defecto
        self.label_idProducto= QLabel("Id Producto: ")
        self.input_idProducto = QLineEdit()
        self.input_idProducto.setPlaceholderText("00000000")
        self.input_idProducto.setReadOnly(True)
        #termina label y textbox 
        self.label_codigo= QLabel("Código: ")
        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("CS 0000")

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
        self.btn_editarProducto.clicked.connect(self.Habilitar_edicion)
        #self.btn_editarProducto.hide()

        self.btn_eliminarProducto = QPushButton("Eliminar")
        self.btn_eliminarProducto.clicked.connect(self.delete)

        self.btn_Aceptar = QPushButton("Aceptar")
        self.btn_Aceptar.clicked.connect(self.aceptar_edicion)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar_edicion)

        self.btn_Volver = QPushButton("↢⁂ Volver al Formulario Principal ⁂↣  ")
        self.btn_Volver.clicked.connect(self.volver)

        self.btn_Agregar_Categoría = QPushButton("Agregar Categoría")
        #self.btn_Agregar_Categoría.clicked.connect()

        self.btn_Agregar_Proveedor = QPushButton("Agregar Proveedor")
        #self.btn_Agregar_Proveedor.clicked.connect()

        self.btn_Stock = QPushButton("Stock")
        #self.btn_Stock.clicked.connect()
        

    def layouts(self):
        """ Define la estructura de los elementos en pantalla """
        # Main layouts
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.left_layout = QFormLayout()
        self.botones_layout = QHBoxLayout()
        self.botonesForm_layout = QHBoxLayout()

        # Agregar los widgets (childrens) al main_layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.botonesForm_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.main_layout.addLayout(self.botones_layout)

        #self.main_layout.addLayout(self.left_layout, 40)

        # Agregar los widgets al top layout
        #self.top_layout.addWidget(self.title)
        #self.top_layout.addWidget(self.image)

        # Agregar los widgets al bottom layout
        self.bottom_layout.addRow(self.btn_Volver)
        self.bottom_layout.addRow(self.label_idProducto, self.input_idProducto)
        self.bottom_layout.addRow(self.label_codigo, self.input_codigo)
        self.bottom_layout.addRow(self.label_nombre, self.input_nombre)
        self.bottom_layout.addRow(self.label_descripcion, self.input_descripcion)
        self.bottom_layout.addRow(self.label_categoria, self.input_categoria)
        self.bottom_layout.addRow(self.label_proveedor, self.input_proveedor)
        self.bottom_layout.addWidget(self.product_list)
        self.botones_layout.addWidget(self.btn_agregarProducto)
        self.botones_layout.addWidget(self.btn_editarProducto)
        self.botones_layout.addWidget(self.btn_eliminarProducto)
        self.botones_layout.addWidget(self.btn_Aceptar)
        self.btn_cancelar.hide()
        self.btn_Aceptar.hide()
        self.botones_layout.addWidget(self.btn_cancelar)
        self.botonesForm_layout.addWidget(self.btn_Agregar_Categoría)
        self.botonesForm_layout.addWidget(self.btn_Agregar_Proveedor)
        self.botonesForm_layout.addWidget(self.btn_Stock)
                
                
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

    def volver(self):
        """Manda al usuario al menu Principal"""
        self.close()
        self.main = Main()

    def delete(self):
        """Elimina Una tupla, previamente seleccionada en el datagrid (lista)"""
        if self.product_list.selectedItems():
            producto = self.product_list.currentItem().text()
            id = producto.split(" --- ")[0]
            producto = self.producto_db.Obtener_Producto(id)
            yes = QMessageBox.Yes

            if producto:
                question_text = f"¿Está seguro de eliminar el producto {producto[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.producto_db.delete_producto(producto[0])
                    self.product_list.clear()
                    self.set_producto_list()
                    self.limpiar()
                    QMessageBox.information(self, "Información", "¡Producto eliminado satisfactoriamente!")
                    

            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a eliminar")

    def insert(self):
        """ Insertar los valores del formulario a la tabla de producto """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_nombre.text() or
                self.input_proveedor.text() or self.input_categoria.text()
                 or self.input_codigo.text() != ""):
            producto = (self.input_nombre.text(),self.input_codigo.text(),
                        self.input_descripcion.text(), self.input_categoria.text(),
                        self.input_proveedor.text())

            try:
                self.producto_db.add_producto(producto)
                QMessageBox.information(
                    self, "Información", "producto agregado correctamente")
                self.product_list.clear()
                self.set_producto_list()
                self.limpiar()
                #self.close()
                #self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de agregar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")

    def update(self,identificador):
        """ Editar los valores del formulario a la tabla de producto """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_nombre.text() or
                self.input_proveedor.text() or self.input_categoria.text()
                 or self.input_codigo.text() or self.input_nombre.text() != ""):

            producto = (self.input_nombre.text(),self.input_codigo.text(),
                        self.input_descripcion.text(), self.input_categoria.text(),
                        self.input_proveedor.text(),self.input_idProducto.text())

            try:
                
                self.producto_db.update_producto(producto)
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
        if self.product_list.selectedItems():
            producto = self.product_list.currentItem().text()
            id = producto.split(" --- ")[0]
            producto = self.producto_db.Obtener_Producto(id)
            yes = QMessageBox.Yes

            if producto:

                question_text = f"¿Está seguro de editar el producto {producto[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.btn_editarProducto.hide()
                    self.btn_agregarProducto.hide()
                    self.btn_eliminarProducto.hide()
                    self.Bloquear_Inputs(False)
                    self.btn_Aceptar.show()
                    self.btn_cancelar.show()
            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a editar")

    def aceptar_edicion(self):
        """Edita los parametros que han cambiado en los textbox"""
        if self.product_list.selectedItems():
            producto = self.product_list.currentItem().text()
            id = producto.split(" --- ")[0]
            producto = self.producto_db.Obtener_Producto(id)
            if producto:
                self.update(producto[0])
                
                self.product_list.clear()
                self.set_producto_list()
                self.limpiar()
            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")
        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a editar")


    def cancelar_edicion(self):
        """Cancela la edicion y envia al usuario a la ventana Principal"""
        self.product_list.clear()
        self.set_producto_list()
        self.limpiar()
        self.Bloquear_Inputs(False)
        self.btn_editarProducto.show()
        self.btn_agregarProducto.show()
        self.btn_eliminarProducto.show()
        self.btn_Aceptar.hide()
        self.btn_cancelar.hide()

    def get_all_producto(self):
        """ Obtiene todas las tuplas de la tabla producto """

        sqlQuery = "select * from producto ORDER BY ROWID ASC "

        try:
            cursor = self.connection.cursor()
            productos = cursor.execute(sqlQuery).fetchall()

            return productos
        except Error as e:
            print(e)

        return None

    def Bloquear_Inputs(self,estado):
        """Deshabilita los QwidgetsInputs para solo dejarlos
         en modo lectura.
         
         parametro estado: recibe True o false para habilitar o no 
         los textbox (inputs) """

        #self.input_idProducto.setReadOnly(estado)
        self.input_codigo.setReadOnly(estado)
        self.input_nombre.setReadOnly(estado)
        self.input_descripcion.setReadOnly(estado)
        self.input_proveedor.setReadOnly(estado)
        self.input_categoria.setReadOnly(estado)

    def set_producto_list(self):
        """ Obtiene las tuplas de Productos y las muestra en la lista """
        productos = self.producto_db.get_all_producto()

        if productos:
            for producto in productos:
                self.product_list.addItem(
                    "{0} --- {1}".format(producto[1], producto[2]))

    def Mostrar_Producto(self):
        """ Muestra los atributos del producto que se encuentra seleccionado """
        producto = self.product_list.currentItem().text()
        id = producto.split(" --- ")[0]
        #QMessageBox.information(self,"este es el Id {0}",str(id))
        producto = self.producto_db.Obtener_Producto(id)
        
        if producto:
            #se deshabilitan los textbox
            self.Bloquear_Inputs(True)
            id_producto =  producto[0]
            codigo =  producto[1]
            nombre =  producto[2]
            descripcion =  producto[3]
            proveedor =  producto[4]
            categoria =  producto[5]
            #se muestran los valores en los text
            self.input_idProducto.setText((str(id_producto)))
            self.input_codigo.setText((str(codigo)))
            self.input_nombre.setText((str(nombre)))
            self.input_descripcion.setText((str(descripcion)))
            self.input_proveedor.setText((str(proveedor)))
            self.input_categoria.setText((str(categoria)))

    def limpiar(self):
        self.input_idProducto.setText("")
        self.input_codigo.setText("")
        self.input_nombre.setText("")
        self.input_categoria.setText("")
        self.input_proveedor.setText("")
        self.input_descripcion.setText("")
    

def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

def Hels():
    app = QApplication(sys.argv)
    window = AddProducto()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
Hels()
