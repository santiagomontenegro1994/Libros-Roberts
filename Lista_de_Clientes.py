from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3


class ListaDeClientes():
    
    db_nombre = 'database.db'
    with sqlite3.connect(db_nombre) as conn:
            cursor = conn.cursor() 
    
    def __init__(self,window):
        self.wind=window
        self.wind.title("Lista de Clientes")
        
        self.seleccion=tk.IntVar()
        
        #creando contenedor
        frame=LabelFrame(self.wind, text = 'Registra un nuevo Cliente')
        frame.grid(row=0, column=0, columnspan=3, pady = 20)
        frame1=LabelFrame(self.wind, text = 'Busqueda')
        frame1.grid(row=1, column=0, columnspan=3, pady = 20)
        
        #nombre cliente
        Label(frame, text='Nombre: ' ).grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        
        #telefono cliente
        Label(frame, text='Telefono: ' ).grid(row=2, column=0)
        self.telefono = Entry(frame)
        self.telefono.grid(row=2, column=1)
        
        #cuit cliente
        Label(frame, text='Cuit: ' ).grid(row=3, column=0)
        self.cuit = Entry(frame)
        self.cuit.grid(row=3, column=1)
        
        #boton agregar cliente
        ttk.Button(frame, text="Guardar Cliente", command = self.add_clientes).grid(row= 4, columnspan=2, sticky=W + E)
        
        #mensajes de notificacion
        self.mensaje = Label(self.wind,text = '', fg = 'red')
        self.mensaje.grid(row=3, column=0, columnspan=3, sticky=W + E)
        
        #------------------------------Seccion de busqueda
        
        self.ent = Entry(frame1)
        self.ent.grid(row=0, column=0,columnspan=2, sticky= W+E)
        self.btn = Button(frame1, text="busqueda", command=self.search)
        self.btn.grid(row=0, column=2)
        self.lbtn = Button(frame1, text="Limpiar",command=self.get_clientes)
        self.lbtn.grid(row=0, column=3)
        self.rbotonTrabajo = tk.Radiobutton(frame1, text="Nombre", variable=self.seleccion, value=1, command=self.search)
        self.rbotonTrabajo.grid(row=1, column=0, padx=15, pady=5)
        self.rbotonTrabajo = tk.Radiobutton(frame1, text="Telefono", variable=self.seleccion, value=2, command=self.search)
        self.rbotonTrabajo.grid(row=1, column=1, padx=15, pady=5) 
        self.rbotonFecha = tk.Radiobutton(frame1, text="Cuit", variable=self.seleccion, value=3, command=self.search)
        self.rbotonFecha.grid(row=1, column=2, padx=15, pady=5)
        
        
        #tabla de clientes
        self.tabla = ttk.Treeview(self.wind, columns=("tel", "cuit"))
        self.tabla.grid(row=6, column=0, columnspan=3)
        self.tabla.heading('#0', text= 'Nombre', anchor=CENTER)
        self.tabla.heading('#1', text= 'Telefono', anchor=CENTER)
        self.tabla.heading('#2', text= 'Cuit', anchor=CENTER)
        
        #Agregando la scrollbar
        self.yscrollbar=ttk.Scrollbar(self.wind, orient="vertical", command=self.tabla.yview)
        self.yscrollbar.grid(row=6,column=4,  sticky=N + S)
        self.tabla.configure(yscrollcommand=self.yscrollbar.set)
        
        #boton para eliminar y Editar
        ttk.Button(self.wind,text = 'Eliminar', command = self.delete_cliente).grid(row=5, column=0, sticky=W + E)
        ttk.Button(self.wind, text = 'Editar', command= self.edit_clientes).grid(row=5, column=1, sticky=W + E)
        
        #llenando las filas de la tabla 
        self.get_clientes()
        
    def run_query(self, query, parameters =()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result        

    def get_clientes(self):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos    
        query = 'SELECT * FROM Clientes ORDER BY nombre ASC'
        db_rows=self.run_query(query)
        #rellenando los datos
        for row in db_rows:
            self.tabla.insert('', 0, text = row[1], value = (row[2], row[3]))
    
    def search(self):
        if self.seleccion.get()==1:
            q2='%'+self.ent.get().upper()+'%'
            #limpiando la tabla
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #consultando los datos    
            query = 'SELECT * FROM Clientes WHERE nombre LIKE ?'
            db_rows=self.run_query(query,[q2])
            #rellenando los datos
            for row in db_rows:
                self.tabla.insert('', 0, text = row[1], value = (row[2], row[3])) 
        elif self.seleccion.get()==2:
            q2='%'+self.ent.get().upper()+'%'
            #limpiando la tabla
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #consultando los datos    
            query = 'SELECT * FROM Clientes WHERE telefono LIKE ?'
            db_rows=self.run_query(query,[q2])
            #rellenando los datos
            for row in db_rows:
                self.tabla.insert('', 0, text = row[1], value = (row[2], row[3])) 
        elif self.seleccion.get()==3:
            q2=self.ent.get().upper()
            #limpiando la tabla
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #consultando los datos    
            query = 'SELECT * FROM Clientes WHERE cuit = ?'
            db_rows=self.run_query(query,[q2])
            #rellenando los datos
            for row in db_rows:
                self.tabla.insert('', 0, text = row[1], value = (row[2], row[3]))    
        else:    
            self.mensaje['text'] = 'Parametros de busqueda son requeridos'
    
    def validacion(self): #valida para que no pase un dato vacio
        return len(self.nombre.get()) != 0 and len(self.telefono.get()) !=0      
        
    def add_clientes(self):  #metodo para agregar clientes
        if self.validacion():
            query = 'INSERT INTO Clientes VALUES(NULL, ?, ?, ?)'
            parameters = (self.nombre.get().upper(), self.telefono.get(), self.cuit.get())
            self.run_query(query, parameters)
            self.mensaje['text'] = 'Cliente: {} agregado'.format(self.nombre.get())
            self.nombre.delete(0,END)
            self.telefono.delete(0,END)
            self.cuit.delete(0,END)
            self.get_clientes()
        else:
            self.mensaje['text'] = 'Nombre y Telefono son requeridos'
            self.get_clientes()
    
    def delete_cliente(self):
        self.mensaje['text'] = '' # vacio la casilla del mensaje
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Porfavor selecciona un cliente'
            return
        self.mensaje['text'] = '' # vacio la casilla del mensaje
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM Clientes WHERE nombre = ?'
        self.run_query(query, (nombre,))
        self.mensaje['text'] = 'Cliente: {} se elimino satisfactoriamente'.format(nombre)
        self.get_clientes()
    
    def edit_clientes(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Porfavor selecciona un cliente'
            return
        
        old_nombre = self.tabla.item(self.tabla.selection())['text']
        old_telefono = self.tabla.item(self.tabla.selection())['values'][0]
        old_cuit = self.tabla.item(self.tabla.selection())['values'][1]
        self.ventana_editar = Toplevel() # ventana de editar
        self.ventana_editar.title = 'Editar Producto'
        
        # Nombre Anterior
        Label(self.ventana_editar, text = 'Nombre anterior: ').grid(row=0, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_nombre), state = 'readonly').grid(row=0, column=2)
        # Nombre Nuevo
        Label(self.ventana_editar, text ='Nuevo Nombre').grid(row=1, column=1)
        nuevo_nombre = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_nombre))
        nuevo_nombre.grid(row=1, column=2)
        
        # Telefono Anterior
        Label(self.ventana_editar, text = 'Telefono anterior: ').grid(row=2, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_telefono), state = 'readonly').grid(row=2, column=2)
        # Telefono Nuevo
        Label(self.ventana_editar, text ='Nuevo Telefono').grid(row=3, column=1)
        nuevo_telefono = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_telefono))
        nuevo_telefono.grid(row=3, column=2)
        
        # Cuit Anterior
        Label(self.ventana_editar, text = 'Cuit anterior: ').grid(row=4, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_cuit), state = 'readonly').grid(row=4, column=2)
        # Cuit Nuevo
        Label(self.ventana_editar, text ='Nuevo Cuit').grid(row=5, column=1)
        nuevo_cuit = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_cuit))
        nuevo_cuit.grid(row=5, column=2)
        
        #boton para agregar 
        Button(self.ventana_editar, text='Editar', command=lambda: self.edit_records(nuevo_nombre.get(), old_nombre, nuevo_telefono.get(), old_telefono, nuevo_cuit.get())).grid(row=6, column=2, sticky=W + E)
    
    def edit_records(self, nuevo_nombre, old_nombre, nuevo_telefono, old_telefono, nuevo_cuit,):
        if  len(nuevo_nombre) != 0 and len(nuevo_telefono) !=0:  #valido que no le pasen valores vacios
            query= 'UPDATE Clientes set nombre = ?, telefono = ?, cuit = ? WHERE nombre = ? AND telefono = ?'
            parameters = (nuevo_nombre.upper(), nuevo_telefono, nuevo_cuit, old_nombre, old_telefono)
            self.run_query(query, parameters) #le paso la consulta
            self.ventana_editar.destroy() #cierro la ventana editar
            self.mensaje['text'] = 'Datos del cliente {} modificados correctamente'.format(nuevo_nombre)
            self.get_clientes()
        else:
            self.mensaje['text'] = 'Nombre y Telefono son requeridos'