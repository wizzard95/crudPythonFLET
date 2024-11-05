import flet as ft

# Importamos la libreria para descargar datos en pdf
from fpdf import FPDF

# Importamos la libreria para descargar los archivos en excel
import pandas as pd

# Importamos hora y fecha
import datetime

# Importamos el contenido del archivo contact_manager.py
from contact_manager import ContactManager

# Inicializamos la clase pdf
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Tabla de datos", 0, 1, "C")
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")

class Form(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        
        # Creamos la variable para poder obtener los métodos
        self.data = ContactManager()
        
        # Creamos la variable para obtener dos datos de la fila presionando el checkbox
        self.selected_row = None
        
        # Creando variables para los campos de texto
        self.name = ft.TextField(label="Nombre", border_color="red")
        
        # Creando variables para campos numéricos
        self.age = ft.TextField(label="Edad", border_color="red",
                                input_filter=ft.NumbersOnlyInputFilter(),
                                max_length=2)
        
        self.email = ft.TextField(label="Correo", border_color="red")                      
        
        self.phone = ft.TextField(label="Teléfono", border_color="red",
                                  input_filter=ft.NumbersOnlyInputFilter(),
                                  max_length=9)
       
        # Variable para buscar algún archivo 
        self.search_filed = ft.TextField(
            label="Buscar por nombre",
            suffix_icon=ft.icons.SEARCH,
            border=ft.InputBorder.UNDERLINE,
            border_color="white",
            label_style=ft.TextStyle(color="white"), 
            on_change=self.search_data,
        )
        
        # Variable para la tabla
        self.data_table = ft.DataTable(
            expand=True,
            border=ft.border.all(2, "red"),
            data_row_color={ft.MaterialState.SELECTED: "red",
                            ft.MaterialState.PRESSED: "black"},
            border_radius=10,
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("Nombre", color="red", weight="bold")),
                ft.DataColumn(ft.Text("Edad", color="red", weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Correo", color="red", weight="bold")),
                ft.DataColumn(ft.Text("Teléfono", color="red", weight="bold"), numeric=True),
            ]
        )
        
        # Ejecutamos el método show_data de más abajo
        self.show_data()
        
        # Estructura del formulario
        self.form = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            col=4,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Ingrese sus datos",
                            size=40,
                            text_align="center",
                            font_family="Arial"),
                    self.name,
                    self.age,
                    self.email,
                    self.phone,
                    # Botones de Guardar, Actualizar, Borrar
                    ft.Container(
                        content=ft.Row(
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.TextButton(text="Guardar",
                                              icon=ft.icons.SAVE,
                                              style=ft.ButtonStyle(
                                                  color="white", bgcolor="red"
                                              ),
                                              # Llamamos a la función add_data dentro del botón
                                              on_click=self.add_data),
                                ft.TextButton(text="Actualizar",
                                              icon=ft.icons.UPDATE,
                                              style=ft.ButtonStyle(
                                                  color="white", bgcolor="red"
                                              ),
                                              # Llamamos al funcion para actualizar los datos
                                              on_click=self.update_data),
                                ft.TextButton(text="Borrar",
                                              icon=ft.icons.DELETE,
                                              style=ft.ButtonStyle(
                                                  color="white", bgcolor="red"
                                              ),
                                            # Llamamos a la funcion para borrar
                                            on_click=self.delete_data,
                                              )
                            ]
                        )
                    )
                ]
            )
        )
        
        # Aquí se mostrarán los datos
        self.table = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            col=8, 
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                # Campo de texto para el buscador                        
                                self.search_filed,
                                ft.IconButton(tooltip="Editar",
                                              icon=ft.icons.EDIT,
                                              icon_color="white",
                                              on_click=self.edit_filed_text),
                                            
                                ft.IconButton(tooltip="Descargar en PDF",
                                              icon=ft.icons.PICTURE_AS_PDF,
                                              icon_color="white",
                                              on_click=self.save_pdf),
                                            
                                ft.IconButton(tooltip="Descargar en EXCEL",
                                              icon=ft.icons.SAVE_ALT,
                                              icon_color="white",
                                              on_click=self.save_excel),
                            ]
                        )
                    ),
                    # Agregamos la tabla
                    ft.Column(
                        expand=True,
                        scroll="auto",
                        controls=[ft.ResponsiveRow([self.data_table])]
                    )
                ]
            )
        )
        
        # Aquí vamos a capturar los datos que nos pasará el usuario
        self.conent = ft.ResponsiveRow(
            controls=[self.form, self.table]
        )
        
    # Función para que se muestren los datos al iniciar el programa    
    def show_data(self):
        self.data_table.rows = []
        # Recorremos el objeto data para obtener los valores de la tabla
        for x in self.data.get_contact():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed= self.get_index,
                    cells= [
                        ft.DataCell(ft.Text(x[1])),
                        ft.DataCell(ft.Text(str(x[2]))),
                        ft.DataCell(ft.Text(x[3])),
                        ft.DataCell(ft.Text(str(x[4]))),
                    ]
                )
            )
        # Actualizamos la tabla
        self.update()

    # Método para agregar los datos a la BD        
    def add_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value)
    
        # Verificamos que los valores tengan al menos 1 carácter
        if len(name) and len(age) and len(email) and len(phone) > 0:
            contact_exists = False
            for row in self.data.get_contact():
                if row[1] == name:
                    contact_exists = True
                    break
            if not contact_exists:
                self.clean_fields()
                self.data.add_contact(name, age, email, phone)
                self.show_data()
    
    # Metodo para marcar el checkbox            
    def get_index(self, e):
        if e.control.selected:
            e.control.selected = False
        else:
            e.control.selected = True
        
        # Creamos una variable para señalar la fila que será afectada y el valor que obtendremos
        name = e.control.cells[0].content.value
        #print(name)
        # Recorreremos todas filas para obtener los datos desde la BD
        for row in self.data.get_contact():
            if row[1] == name:
                self.selected_row = row
                break
        # Obtenemos toda la columna    
        #print(self.selected_row)    
        self.update()
    
    # Metodo para editar la fila
    def edit_filed_text(self, e):
        try:
            self.name.value = self.selected_row[1]
            self.age.value = self.selected_row[2]
            self.email.value = self.selected_row[3]
            self.phone.value = self.selected_row[4]
            self.update()
        except TypeError:
            print("ERROR")
            
    # Metodo para capturar y actualizar los datos 
    def update_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value)  
        
        if len(name) and len(age) and len(email) and len(phone) > 0: 
            self.clean_fields()
            self.data.update_contact(self.selected_row[0], name, age, email, phone)
            self.show_data()
            
    # Metodo para borrar datos de la BD        
    def delete_data(self, e):
        self.data.delete_contact(self.selected_row[1])
        self.show_data()
            
            
     # Metodo para buscar contactos
    def search_data(self, e):
        search = self.search_filed.value.lower()
        name = list( filter(lambda x: search in x[1].lower(), self.data.get_contact()))
        self.data_table.rows =[]
        if not self.search_filed.value == "":
            if len(name) >0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed= self.get_index, 
                            cells= [
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(str(x[2]))),
                                ft.DataCell(ft.Text(x[3])),
                                ft.DataCell(ft.Text(str(x[4]))),
                            ]
                        )
                    )
                    self.update()
        else:
            self.show_data()
            
            
                    
    # Método para borrar los campos de texto
    def clean_fields(self):
        self.name.value = ""
        self.age.value = ""
        self.email.value = ""
        self.phone.value = ""
        
        
    # Metodo para exportar datos en PDF    
    def save_pdf(self, e):
        pdf = PDF()
        pdf.add_page()
        column_widths = [10,40, 20, 80, 40]
        
        # Agregar filas a la tabla
        data = self.data.get_contact()
        header = ("ID", "NOMBRE", "EDAD", "CORREO", "TELEFONO")
        data.insert(0, header)
        for row in data:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()
        file_name =  datetime.datetime.now()
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)        

    # Metodo para exportar datos en excel
    def save_excel(self, e):
        file_name =  datetime.datetime.now()
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        contacts = self.data.get_contact()
        df = pd.DataFrame(contacts, columns=["ID", "Nombre", "Edad", "Correo", "Teléfono"])
        df.to_excel(file_name, index=False)
    
       
    # Método build se utiliza para retornar el contenido de la clase content
    def build(self):
        return self.conent

# Función principal de pantalla
def main(page: ft.Page):
    page.bgcolor = "black"
    page.title = "CRUD SQLite"
    page.window_min_height = 500
    page.window_min_width = 1100

    page.add(Form(page))  # Llamamos a la clase de arriba que contiene el formulario

# Llamada a la aplicación Flet
ft.app(target=main)


