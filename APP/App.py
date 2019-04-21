from tkinter import ttk
from tkinter import *

import sqlite3

class Inventary:
    db_name = 'Basedatos.db'


    def __init__(self, Window):
        self.wind = Window
        self.wind.title('Inventario')

        # crear un contenedor frame
        frame = LabelFrame(self.wind, text='Registra un nuevo contacto')
        frame.grid(row = 0, column = 0, columnspan = 6, pady = 20)

        # entrada de nombre
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0 )
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # entrada de telefono
        Label(frame, text = 'Telefono: ').grid(row = 2, column = 0 )
        self.telefono = Entry(frame)
        self.telefono.grid(row = 2, column = 1)

        # entrada de ciudad
        Label(frame, text = 'Ciudad: ').grid(row = 3, column = 0 )
        self.ciudad = Entry(frame)
        self.ciudad.grid(row = 3, column = 1)

        # entrada de email
        Label(frame, text = 'Email: ').grid(row = 4, column = 0 )
        self.email = Entry(frame)
        self.email.grid(row = 4, column = 1)

        # Boton para añadir
        ttk.Button(frame, text = 'Guardar contacto', command = self.añadir_contacto).grid(row = 5, columnspan = 2, sticky = W + E)

        # Salida de mensajes
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Crear tabla
        self.tree = ttk.Treeview(height = 20, columns = ("Nombre", "Telefono", "Ciudad",))
        self.tree.grid(row = 5, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Telefono', anchor = CENTER)
        self.tree.heading('#2', text = 'Ciudad', anchor = CENTER)
        self.tree.heading('#3', text = 'Email', anchor = CENTER)

        # Botones
        ttk.Button(text = 'Eliminar', command = self.eliminar_contacto).grid(row = 6, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.editar_contacto).grid(row = 6, column = 1, sticky = W + E)
        
        # Rellenar filas
        self.obtener_contacto()

    def run_requery(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor() 
            result = cur.execute(query, parameters) 
            conn.commit()
        return result    

    def obtener_contacto(self):
        # Limpiando la tabla
        records = self.tree.get_children()
        for elements in records:
            self.tree.delete(elements)
        # Quering(consultando) data
        query = 'SELECT * FROM Inventario ORDER BY NOMBRE DESC'
        db_rows = self.run_requery(query)
        # llenar datos
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], value = row[2:])

    def validacion(self):
        return len(self.name.get()) != 0 and len(self.telefono.get()) != 0 and len(self.ciudad.get()) != 0 and len(self.email.get()) != 0
    
    def añadir_contacto(self):
        if self.validacion():
            query = 'INSERT INTO Inventario VALUES (NULL, ?, ?, ?, ?)'
            parameters = (self.name.get()),(self.telefono.get()),(self.ciudad.get()),(self.email.get())
            self.run_requery(query, parameters)
            self.mensaje['text'] = 'Contacto {} añadido correctamente' .format(self.name.get())
            self.name.delete(0, END)
            self.telefono.delete(0, END)
            self.ciudad.delete(0, END)
            self.email.delete(0, END)
        else:
            self.mensaje['text'] = 'Se requiere ingresar todos los datos' 
        self.obtener_contacto()

    def eliminar_contacto(self):
        self.mensaje['text'] = ''
        try:    
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un item'
            return
        self.mensaje['text'] = ''    
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Inventario WHERE NOMBRE = ?'
        self.run_requery(query, (name, ))
        self.mensaje['text'] = 'Contacto {} eliminado satisfactoriamente'.format(name)
        self.obtener_contacto()

    def editar_contacto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un item'
            return
        name = self.tree.item(self.tree.selection())['text']
        telefono = self.tree.item(self.tree.selection())['values'][0]
        ciudad = self.tree.item(self.tree.selection())['values'][1]
        email = self.tree.item(self.tree.selection())['values'][2]
        self.editar = Toplevel()
        self.editar.title = 'Editar conacto'

        # Editar Nombre
        Label(self.editar, text = 'Nombre viejo:').grid(row = 0, column = 1)
        Entry(self.editar, textvariable = StringVar(self.editar, value = name), state = 'readonly').grid(row = 0, column = 2)

        Label(self.editar, text = 'Nuevo nombre:').grid(row = 1, column = 1)
        new_name = Entry(self.editar)
        new_name.grid(row = 1, column = 2)

        # Editar Telefono
        Label(self.editar, text = 'Telefono viejo:').grid(row = 2, column = 1)
        Entry(self.editar, textvariable = StringVar(self.editar, value = telefono), state = 'readonly').grid(row = 2, column = 2)

        Label(self.editar, text = 'Telefono nuevo:').grid(row = 3, column = 1)
        new_telefono = Entry(self.editar)
        new_telefono.grid(row = 3, column = 2)

        # Editar Ciudad
        Label(self.editar, text = 'Antigua ciudad:').grid(row = 4, column = 1)
        Entry(self.editar, textvariable = StringVar(self.editar, value = ciudad), state = 'readonly').grid(row = 4, column = 2)

        Label(self.editar, text = 'Ciudad nueva:').grid(row = 5, column = 1)
        new_ciudad = Entry(self.editar)
        new_ciudad.grid(row = 5, column = 2)

        # Editar Email
        Label(self.editar, text = 'Email viejo:').grid(row = 6, column = 1)
        Entry(self.editar, textvariable = StringVar(self.editar, value = email), state = 'readonly').grid(row = 6, column = 2)

        Label(self.editar, text = 'Nuevo email:').grid(row = 7, column = 1)
        new_email = Entry(self.editar)
        new_email.grid(row = 7, column = 2)

        #Boton    
        Button(self.editar, text = 'Actualizar', command = lambda: self.editar_item(new_name.get(), name, new_telefono.get(), telefono, new_ciudad.get(), ciudad, new_email.get(), email)).grid(row = 8, column = 2, sticky = W)
        self.editar.mainloop()

    def editar_item(self, new_name, name, new_telefono, telefono, new_ciudad, ciudad, new_email, email):
        query = 'UPDATE Inventario SET Nombre = ?, Telefono = ?, Ciudad = ?, Email = ? WHERE NOMBRE = ? AND TELEFONO = ? AND CIUDAD = ? AND EMAIL = ?'
        parameters = (new_name, new_telefono, new_ciudad, new_email, name, telefono, ciudad, email)
        self.run_requery(query, parameters)
        self.editar.destroy()
        self.mensaje['text'] = 'Contacto {} actualizado correctamente.'.format(name)
        self.obtener_contacto()
        

if __name__ == '__main__':
    window = Tk()
    aplicacion = Inventary(window)
    window.mainloop()