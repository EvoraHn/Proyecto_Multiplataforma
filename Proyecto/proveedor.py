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
        # Crear o abrir la conexión a la base de datos
        self.producto_db = ProductoDB("laminas.db")
        self.setWindowTitle("Formulario Proveedor")
        self.setGeometry(700,400,750,450)
        self.UI()
        self.show()
        


    def UI(self):
        self.mainDesing()
        self.layouts()
        self.set_Proveedor_list()

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
        self.lista_proveedor.itemClicked.connect(self.Mostrar_Proveedor)

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
        self.btn_Agregar.clicked.connect(self.insert)
        #self.btn_Agregar.clicked.connect()
        self.btn_Agregar.setGeometry(5,50,50,15)
        self.btn_Agregar.setStyleSheet("font-size: 15px; background-color: gray; color: white;")

        # widget para btn eliminar
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.delete)
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
        self.btn_layout.addRow("",self.btn_eliminar)

        self.setLayout(self.main_layout)

    def insert(self):
        """ Insertar los valores del formulario a la tabla de Stock """
        # Verificar si los valores requeridos fueron agregados
        if (self.input_IdProv.text() or 
                self.input_nombre.text() or
                    self.input_telefono.text() != ""):
            Proveedor = (self.input_IdProv.text(), self.input_nombre.text(),self.input_telefono.text())

            try:
                self.producto_db.add_Proveedor(Proveedor)
                QMessageBox.information(
                self, "Información", "Proveedor agregado correctamente")
                self.lista_proveedor.clear()
                self.set_Proveedor_list()
                self.limpiar()
                #self.close()
                #self.main = Main()
            except Error as e:
                QMessageBox.information(
                    self, "Error", "Error al momento de agregar el producto")
        else:
            QMessageBox.information(
                self, "Advertencia", "Debes ingresar toda la información")


    def delete(self):
        """Elimina Una tupla, previamente seleccionada en el datagrid (lista)"""
        if self.lista_proveedor.selectedItems():
            Proveedor = self.lista_proveedor.currentItem().text()
            id = Proveedor.split(" --- ")[0]
            Proveedor = self.producto_db.Obtener_Proveedores(id)
            yes = QMessageBox.Yes

            if Proveedor:
                question_text = f"¿Está seguro de eliminar el Proveedor {Proveedor[1]}?"
                question = QMessageBox.question(self, "Advertencia", question_text,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
               

                if question == QMessageBox.Yes:
                    self.producto_db.delete_Proveedor(Proveedor[0])
                    self.lista_proveedor.clear()
                    self.set_Proveedor_list()
                    self.limpiar()
                    QMessageBox.information(self, "Información", "¡Proveedor eliminado satisfactoriamente!")
                    

            else:
                QMessageBox.information(self, "Advertencia", "Ha ocurrido un error. Reintente nuevamente")

        else:
            QMessageBox.information(self, "Advertencia", "Favor seleccionar un Producto a eliminar")


    def set_Proveedor_list(self):
        """ Obtiene las tuplas de Productos y las muestra en la lista """
        proveedores = self.producto_db.get_all_Proveedor()

        if proveedores:
            for Proveedor in proveedores:
                self.lista_proveedor.addItem(
                    "{0} --- {1}---{2}".format(Proveedor[0], Proveedor[1], Proveedor[2]))


    def Mostrar_Proveedor(self):
        """ Muestra los atributos del producto que se encuentra seleccionado """
        Proveedor = self.lista_proveedor.currentItem().text()
        id = Proveedor.split(" --- ")[0]
        #QMessageBox.information(self,"este es el id {0}",str(id))
        Proveedor = self.producto_db.Obtener_Proveedores(id)
        
        if Proveedor:
            #se deshabilitan los textbox
            #self.Bloquear_Inputs(True)
            #id_Stock = Stock[0]
            Id_Proveedor =  Proveedor[0]
            Nombre =  Proveedor[1]
            Numero_de_Telefono =  Proveedor[2]
            

            #se muestran los valores en los text
            self.input_IdProv.setText((str(Id_Proveedor)))
            self.input_nombre .setText((str(Nombre)))
            self.input_telefono .setText((str(Numero_de_Telefono)))
            

    def limpiar(self):
        self.input_IdProv.setText("")
        self.input_nombre.setText("")
        self.input_telefono .setText("")
        

class ProductoDB:
    """ Base de datos SQLite para los productos. """

    def __init__(self, db_filename):
        """ Inicializador de la clase """
        self.connection = self.create_connection(db_filename)
        self.Proveedor_query = """ CREATE TABLE IF NOT EXISTS Proveedor (
                                    Id_Proveedor integer PRIMARY KEY autoincrement,
                                    Nombre text NOT NULL,
                                    Numero_de_telefono integer
                                  );
                                """
        self.create_table(self.connection, self.Proveedor_query)

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

    def add_Proveedor(self, Proveedor):
        """
        Realiza una inserción a la tabla de empleados.
        :param producto: Una estructura que contiene
                         los datos del Proveedor.
        :return:
        """
        sqlInsert = """
                    INSERT INTO Proveedor(
                        Id_Proveedor, Nombre, Numero_de_telefono)
                     VALUES(?, ?, ?)
                    """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlInsert, Proveedor)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def Obtener_Proveedores(self, id):
        """
        Busca un proveedor mediante el valor del Código.

        param: Code: Codigo unico para identificar cada lámina.
        :return: Un arreglo con los atributos de proveedores.
        """
        sqlQuery = " SELECT * FROM Proveedor WHERE Id_Proveedor = ?"

        try:
            cursor = self.connection.cursor()
            # fetchone espera que se retorne una tupla (1,)
            proveedores = cursor.execute(sqlQuery, (id,)).fetchone()

            return proveedores
        except Error as e:
            print(e)

        return None

    def update_Proveedor(self,Proveedor):
        """
        Realiza una modificación a la tabla de Proveedor.
        :param producto: Una estructura que contiene
                         los datos de proveedores.
        :return:
        """
        sqlUpdate = """
                    UPDATE Proveedor
                        SET Nombre = ?, Numero_de_Telefono = ?
                        WHERE Id_Proveedor = ?
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlUpdate,Proveedor)
            # Indicarle al motor de base de datos
            # que los cambios sean persistentes
            self.connection.commit()
        except Error as e:
            print(e)

    def delete_Proveedor(self,codigo):
        """
        Realiza una eliminación a la tabla de Proveedor.
        :param id: identificador para la tupla
        :return:
        """
        #QMessageBox.information("ESTE ES EL CODIGO",str(codigo))
        sqlDelete = """
                    delete from Proveedor where Id_Proveedor = ?
                    """
        try:
           
            cursor = self.connection.cursor()
            cursor.execute(sqlDelete,(codigo,))
            self.connection.commit()
            return True
        except Error as e:
            print(e)

        return None


    def get_all_Proveedor(self):
        """ Obtiene todas las tuplas de la tabla proveedor """
        sqlQuery = " SELECT * FROM  Proveedor ORDER BY ROWID ASC "

        try:
            cursor = self.connection.cursor()
            proveedores = cursor.execute(sqlQuery).fetchall()

            return proveedores
        except Error as e:
            print(e)

        return None            


def main():
    app = QApplication(sys.argv)
    window = AgregarProveedor()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
