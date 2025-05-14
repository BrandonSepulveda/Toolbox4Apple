import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

class AplicacionToolboXBS:
    def __init__(self, root):
        self.root = root
        root.title("ToolboXBS")
        root.geometry("900x650")
        
        # Colores de la aplicación - Esquema blanco y negro con acento azul
        self.color_primario = "#000000"      # Negro
        self.color_secundario = "#333333"    # Gris oscuro
        self.color_acento = "#0078D7"        # Azul Windows
        self.color_fondo = "#F0F0F0"         # Gris muy claro
        self.color_texto = "#000000"         # Negro
        self.color_texto_claro = "#FFFFFF"   # Blanco
        
        # Configurar el color de fondo
        root.configure(bg=self.color_fondo)
        
        # Crear frame para la barra de navegación
        self.nav_frame = tk.Frame(root, bg=self.color_primario, height=70)
        self.nav_frame.pack(fill=tk.X)
        
        # Efecto de "shadow" debajo de la barra de navegación
        self.shadow_frame = tk.Frame(root, bg="#CCCCCC", height=3)
        self.shadow_frame.pack(fill=tk.X)
        
        # Intentar cargar el logo desde la URL
        try:
            logo_url = "https://github.com/BrandonSepulveda/BrandonSepulveda.github.io/blob/main/logo/Logo-30.png?raw=true"
            response = requests.get(logo_url)
            logo_image = Image.open(BytesIO(response.content))
            logo_image = logo_image.resize((40, 40), Image.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_image)
            
            self.logo_label = tk.Label(self.nav_frame, image=self.logo_tk, bg=self.color_primario)
            self.logo_label.pack(side=tk.LEFT, padx=15, pady=10)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            # Si hay error al cargar el logo, usar un logo alternativo
            self.logo_label = tk.Label(self.nav_frame, text="🧰", font=("Arial", 24), 
                                      bg=self.color_primario, fg=self.color_acento)
            self.logo_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Nombre de la aplicación
        self.titulo = tk.Label(self.nav_frame, text="ToolboXBS", font=("Consolas", 20, "bold"), 
                              bg=self.color_primario, fg=self.color_texto_claro)
        self.titulo.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Separador vertical
        ttk.Separator(self.nav_frame, orient="vertical").pack(side=tk.LEFT, fill="y", padx=15, pady=10)
        
        # Botones de navegación con efecto hover - Nuevas secciones
        self.botones_nav = []
        for texto in ["Información", "Descargas", "Reparación", "Tweaks"]:
            boton_frame = tk.Frame(self.nav_frame, bg=self.color_primario)
            boton_frame.pack(side=tk.LEFT, padx=5, pady=10)
            
            boton = tk.Label(boton_frame, text=texto, font=("Consolas", 12), 
                            bg=self.color_primario, fg=self.color_texto_claro, cursor="hand2")
            boton.pack(pady=5)
            
            # Indicador de selección (inicialmente invisible)
            indicador = tk.Frame(boton_frame, bg=self.color_acento, height=3, width=0)
            indicador.pack(side=tk.BOTTOM, fill="x")
            
            # Vincular eventos
            boton.bind("<Button-1>", lambda e, t=texto: self.cambiar_seccion(t))
            boton.bind("<Enter>", lambda e, ind=indicador: self.hover_enter(ind))
            boton.bind("<Leave>", lambda e, ind=indicador: self.hover_leave(ind))
            
            self.botones_nav.append((boton, indicador))
        
        # Botones de acción en el lado derecho
        self.boton_buscar = self.crear_boton_icono(self.nav_frame, "🔍", "Buscar")
        self.boton_buscar.pack(side=tk.RIGHT, padx=(0, 15), pady=10)
        
        self.boton_perfil = self.crear_boton_icono(self.nav_frame, "⚙️", "Configuración")
        self.boton_perfil.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # Frame principal para el contenido con scroll
        self.main_container = tk.Frame(root, bg=self.color_fondo)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para permitir scroll
        self.canvas = tk.Canvas(self.main_container, bg=self.color_fondo, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empaquetar scrollbar y canvas
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame dentro del canvas para el contenido
        self.main_frame = tk.Frame(self.canvas, bg=self.color_fondo)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Banner principal con imagen
        self.banner_frame = tk.Frame(self.main_frame, bg=self.color_fondo, height=200)
        self.banner_frame.pack(fill=tk.X, pady=(0, 20), padx=30)
        
        # Configurar evento de redimensionamiento
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.main_frame.bind('<Configure>', self.on_frame_configure)
        
        # Permitir scroll con la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Contenido inicial
        self.contenido_actual = "Información"
        self.mostrar_contenido()
    
    def on_canvas_configure(self, event):
        """Ajustar el ancho del frame interno al cambiar el tamaño del canvas"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def on_frame_configure(self, event):
        """Ajustar la región de desplazamiento al cambiar el tamaño del frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Permitir desplazamiento con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def crear_boton_icono(self, parent, icono, tooltip):
        """Crear un botón con ícono y tooltip"""
        boton = tk.Label(parent, text=icono, font=("Helvetica", 16), 
                        bg=self.color_primario, fg=self.color_texto_claro, cursor="hand2")
        
        # Tooltip personalizado
        def mostrar_tooltip(event):
            x, y = event.x_root, event.y_root
            self.tooltip = tk.Toplevel(parent)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.geometry(f"+{x+10}+{y+10}")
            tk.Label(self.tooltip, text=tooltip, bg="#333", fg="white", padx=5, pady=2).pack()
        
        def ocultar_tooltip(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        boton.bind("<Enter>", mostrar_tooltip)
        boton.bind("<Leave>", ocultar_tooltip)
        
        return boton
    
    def hover_enter(self, indicador):
        """Efecto al pasar el mouse sobre un botón de navegación"""
        indicador.config(width=30)
    
    def hover_leave(self, indicador):
        """Efecto al retirar el mouse de un botón de navegación"""
        if not hasattr(indicador, 'seleccionado') or not indicador.seleccionado:
            indicador.config(width=0)
    
    def cambiar_seccion(self, seccion):
        """Cambiar a la sección seleccionada"""
        self.contenido_actual = seccion
        
        # Actualizar indicadores de selección
        for boton, indicador in self.botones_nav:
            if boton.cget("text") == seccion:
                indicador.config(width=30, bg=self.color_acento)
                indicador.seleccionado = True
            else:
                indicador.config(width=0)
                indicador.seleccionado = False
        
        # Mostrar contenido y restablecer posición de scroll al inicio
        self.mostrar_contenido()
        self.canvas.yview_moveto(0)
    
    def crear_tarjeta(self, parent, titulo, descripcion, icono=None, boton_texto="Ver más"):
        """Crear una tarjeta elegante para mostrar contenido"""
        tarjeta = tk.Frame(parent, bg="white", bd=0, relief=tk.RAISED, padx=15, pady=15)
        tarjeta.pack(fill=tk.X, pady=10, padx=5, ipady=5)
        
        # Añadir sombra (efecto visual)
        def on_enter(e):
            tarjeta.config(relief=tk.RAISED, bd=1)
        
        def on_leave(e):
            tarjeta.config(relief=tk.FLAT, bd=0)
        
        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
        
        # Contenido de la tarjeta
        titulo_frame = tk.Frame(tarjeta, bg="white")
        titulo_frame.pack(fill=tk.X, anchor="w")
        
        # Icono junto al título
        if icono:
            icono_label = tk.Label(titulo_frame, text=icono, font=("Arial", 24), 
                                 bg="white", fg=self.color_acento)
            icono_label.pack(side=tk.LEFT, padx=(0, 10))
        
        titulo_label = tk.Label(titulo_frame, text=titulo, font=("Consolas", 14, "bold"), 
                               bg="white", fg=self.color_texto)
        titulo_label.pack(side=tk.LEFT)
        
        # Línea separadora
        separador = tk.Frame(tarjeta, height=2, bg=self.color_acento, width=50)
        separador.pack(anchor="w", pady=5)
        
        desc_label = tk.Label(tarjeta, text=descripcion, bg="white", font=("Consolas", 10),
                             fg=self.color_texto, wraplength=650, justify="left")
        desc_label.pack(anchor="w", pady=5)
        
        # Botón estilizado
        boton = tk.Button(tarjeta, text=boton_texto, font=("Consolas", 10), 
                         bg=self.color_acento, fg=self.color_texto_claro, 
                         bd=0, padx=15, pady=5, cursor="hand2",
                         activebackground=self.color_secundario, activeforeground=self.color_texto_claro)
        boton.pack(anchor="e", pady=(10, 0))
        
        return tarjeta
    
    def mostrar_contenido(self):
        """Mostrar el contenido de la sección actual"""
        # Limpiar el frame principal (excepto el banner)
        for widget in self.main_frame.winfo_children():
            if widget != self.banner_frame:
                widget.destroy()
        
        # Contenido específico según la sección
        if self.contenido_actual == "Información":
            # Banner de información del sistema
            banner_frame = tk.Frame(self.banner_frame, bg=self.color_secundario)
            banner_frame.place(relwidth=1, relheight=1)
            
            tk.Label(banner_frame, text="Información del Sistema", font=("Consolas", 24, "bold"),
                   bg=self.color_secundario, fg=self.color_texto_claro).pack(pady=(30, 10))
            
            tk.Label(banner_frame, text="Diagnóstico y monitoreo de recursos", font=("Consolas", 12),
                   bg=self.color_secundario, fg=self.color_texto_claro).pack()
            
            # Panel principal de información
            info_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
            info_frame.pack(fill=tk.BOTH, expand=True, padx=30)
            
            # Panel de resumen
            resumen_frame = tk.Frame(info_frame, bg="white", bd=1, relief=tk.SOLID)
            resumen_frame.pack(fill=tk.X, pady=10, ipady=10)
            
            tk.Label(resumen_frame, text="Resumen del Sistema", font=("Consolas", 14, "bold"),
                   bg="white", fg=self.color_texto).pack(anchor="w", padx=20, pady=(10, 15))
            
            # Información del sistema en columnas
            datos_frame = tk.Frame(resumen_frame, bg="white")
            datos_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Columna izquierda
            col_izq = tk.Frame(datos_frame, bg="white")
            col_izq.pack(side=tk.LEFT, fill=tk.Y, expand=True)
            
            info_sistema = [
                ("Sistema Operativo:", "Windows 11 Pro"),
                ("Versión:", "22H2 Build 22621.2283"),
                ("Arquitectura:", "64 bits"),
                ("Procesador:", "Intel Core i7-12700K")
            ]
            
            for label, valor in info_sistema:
                fila = tk.Frame(col_izq, bg="white")
                fila.pack(fill=tk.X, pady=3)
                
                tk.Label(fila, text=label, font=("Consolas", 10), width=20, anchor="w",
                       bg="white", fg=self.color_secundario).pack(side=tk.LEFT)
                
                tk.Label(fila, text=valor, font=("Consolas", 10, "bold"), anchor="w",
                       bg="white", fg=self.color_texto).pack(side=tk.LEFT)
            
            # Columna derecha
            col_der = tk.Frame(datos_frame, bg="white")
            col_der.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
            
            info_recursos = [
                ("Memoria RAM:", "16 GB (8 GB disponible)"),
                ("Almacenamiento:", "512 GB SSD (128 GB libre)"),
                ("Tarjeta Gráfica:", "NVIDIA GeForce RTX 3060"),
                ("VRAM:", "8 GB GDDR6")
            ]
            
            for label, valor in info_recursos:
                fila = tk.Frame(col_der, bg="white")
                fila.pack(fill=tk.X, pady=3)
                
                tk.Label(fila, text=label, font=("Consolas", 10), width=20, anchor="w",
                       bg="white", fg=self.color_secundario).pack(side=tk.LEFT)
                
                tk.Label(fila, text=valor, font=("Consolas", 10, "bold"), anchor="w",
                       bg="white", fg=self.color_texto).pack(side=tk.LEFT)
            
            # Botones de acción para información del sistema
            botones_frame = tk.Frame(info_frame, bg=self.color_fondo)
            botones_frame.pack(fill=tk.X, pady=15)
            
            acciones = [
                ("📊", "Monitor de Rendimiento", "Visualiza el uso de CPU, RAM y GPU en tiempo real"),
                ("🔍", "Diagnóstico Completo", "Analiza el estado de salud del sistema y sus componentes"),
                ("💾", "Información de Discos", "Estado, espacio y rendimiento de unidades de almacenamiento")
            ]
            
            for icono, titulo, desc in acciones:
                self.crear_tarjeta(info_frame, titulo, desc, icono)
                
        elif self.contenido_actual == "Descargas":
            # Banner de descargas
            banner_frame = tk.Frame(self.banner_frame, bg=self.color_acento)
            banner_frame.place(relwidth=1, relheight=1)
            
            tk.Label(banner_frame, text="Descargas de Aplicaciones", font=("Consolas", 24, "bold"),
                   bg=self.color_acento, fg=self.color_texto_claro).pack(pady=(30, 10))
            
            tk.Label(banner_frame, text="Software esencial para tu sistema", font=("Consolas", 12),
                   bg=self.color_acento, fg=self.color_texto_claro).pack()
            
            # Contenedor principal con padding
            descargas_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
            descargas_frame.pack(fill=tk.BOTH, expand=True, padx=30)
            
            # Sección de búsqueda y categorías
            busqueda_frame = tk.Frame(descargas_frame, bg="white", bd=1, relief=tk.SOLID)
            busqueda_frame.pack(fill=tk.X, pady=10, ipady=10)
            
            # Buscador
            tk.Label(busqueda_frame, text="Buscar aplicaciones:", font=("Consolas", 12),
                   bg="white", fg=self.color_texto).pack(side=tk.LEFT, padx=20)
            
            entry_frame = tk.Frame(busqueda_frame, bg="white", bd=1, relief=tk.SOLID)
            entry_frame.pack(side=tk.LEFT, padx=10)
            
            busqueda_entry = tk.Entry(entry_frame, width=30, font=("Consolas", 10), bd=0, bg="white")
            busqueda_entry.pack(side=tk.LEFT, padx=5, ipady=5)
            
            tk.Button(busqueda_frame, text="Buscar", bg=self.color_acento, fg=self.color_texto_claro,
                    font=("Consolas", 10), bd=0, padx=15, pady=5).pack(side=tk.LEFT)
            
            # Categorías en pestañas
            categorias_frame = tk.Frame(descargas_frame, bg=self.color_fondo)
            categorias_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Estilo para las pestañas
            estilo = ttk.Style()
            estilo.configure("TNotebook", background=self.color_fondo, borderwidth=0)
            estilo.configure("TNotebook.Tab", font=("Consolas", 10), padding=[10, 5])
            estilo.map("TNotebook.Tab", background=[("selected", self.color_acento)], 
                     foreground=[("selected", self.color_texto_claro)])
            
            notebook = ttk.Notebook(categorias_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Contenido de cada categoría
            categorias = {
                "Utilidades": [
                    ("⚡", "CPU-Z", "Información detallada del procesador y placa base"),
                    ("🔧", "CCleaner", "Limpieza y optimización del sistema"),
                    ("🔒", "Malwarebytes", "Protección contra malware y virus")
                ],
                "Multimedia": [
                    ("🎬", "VLC Media Player", "Reproductor multimedia compatible con múltiples formatos"),
                    ("🎵", "Audacity", "Editor de audio profesional"),
                    ("📺", "OBS Studio", "Software para streaming y grabación de pantalla")
                ],
                "Desarrollo": [
                    ("💻", "Visual Studio Code", "Editor de código ligero y potente"),
                    ("🐍", "Python", "Lenguaje de programación interpretado"),
                    ("🐙", "Git", "Sistema de control de versiones")
                ],
                "Productividad": [
                    ("📝", "LibreOffice", "Suite ofimática de código abierto"),
                    ("📊", "Notion", "Organizador de tareas y proyectos"),
                    ("🔄", "Syncthing", "Sincronización de archivos entre dispositivos")
                ]
            }
            
            for categoria, apps in categorias.items():
                # Frame para la categoría con scroll
                cat_frame = tk.Frame(notebook, bg=self.color_fondo)
                notebook.add(cat_frame, text=categoria)
                
                # Lista de aplicaciones
                for icono, nombre, desc in apps:
                    app_frame = tk.Frame(cat_frame, bg="white", bd=0)
                    app_frame.pack(fill=tk.X, pady=10, ipady=10)
                    
                    # Efecto hover
                    def on_enter(e, frame=app_frame):
                        frame.config(bd=1, relief=tk.RAISED)
                    
                    def on_leave(e, frame=app_frame):
                        frame.config(bd=0, relief=tk.FLAT)
                    
                    app_frame.bind("<Enter>", on_enter)
                    app_frame.bind("<Leave>", on_leave)
                    
                    # Icono
                    icono_label = tk.Label(app_frame, text=icono, font=("Arial", 28),
                                        bg="white", fg=self.color_acento)
                    icono_label.pack(side=tk.LEFT, padx=20)
                    
                    # Información de la app
                    info_frame = tk.Frame(app_frame, bg="white")
                    info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
                    
                    tk.Label(info_frame, text=nombre, font=("Consolas", 12, "bold"),
                           bg="white", fg=self.color_texto).pack(anchor="w")
                    
                    tk.Label(info_frame, text=desc, font=("Consolas", 10),
                           bg="white", fg=self.color_secundario).pack(anchor="w", pady=(5, 0))
                    
                    # Botones de acción
                    botones_frame = tk.Frame(app_frame, bg="white")
                    botones_frame.pack(side=tk.RIGHT, padx=20)
                    
                    tk.Button(botones_frame, text="Descargar", font=("Consolas", 10),
                            bg=self.color_acento, fg=self.color_texto_claro,
                            padx=10, pady=3, bd=0).pack(side=tk.TOP, pady=(0, 5))
                    
                    tk.Button(botones_frame, text="Más info", font=("Consolas", 10),
                            bg=self.color_fondo, fg=self.color_texto,
                            padx=10, pady=3, bd=0).pack(side=tk.BOTTOM)
            
        elif self.contenido_actual == "Reparación":
            # Banner de reparación
            banner_frame = tk.Frame(self.banner_frame, bg="#D32F2F")  # Rojo
            banner_frame.place(relwidth=1, relheight=1)
            
            tk.Label(banner_frame, text="Reparación del Sistema", font=("Consolas", 24, "bold"),
                   bg="#D32F2F", fg=self.color_texto_claro).pack(pady=(30, 10))
            
            tk.Label(banner_frame, text="Soluciones para problemas comunes", font=("Consolas", 12),
                   bg="#D32F2F", fg=self.color_texto_claro).pack()
            
            # Contenedor principal con padding
            reparacion_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
            reparacion_frame.pack(fill=tk.BOTH, expand=True, padx=30)
            
            # Panel de asistente de diagnóstico
            diagnostico_frame = tk.Frame(reparacion_frame, bg="white", bd=1, relief=tk.SOLID)
            diagnostico_frame.pack(fill=tk.X, pady=10, ipady=15)
            
            tk.Label(diagnostico_frame, text="⚕️ Asistente de Diagnóstico", font=("Consolas", 16, "bold"),
                   bg="white", fg=self.color_texto).pack(pady=(10, 5))
            
            tk.Label(diagnostico_frame, text="Selecciona el tipo de problema que estás experimentando:",
                   font=("Consolas", 10), bg="white", fg=self.color_texto).pack(pady=(0, 15))
            
            # Opciones de problemas
            opciones_frame = tk.Frame(diagnostico_frame, bg="white")
            opciones_frame.pack(pady=10)
            
            problemas = [
                "Rendimiento lento", "Error de inicio", "Problema de red",
                "Error de aplicación", "Problema de audio", "Problema de vídeo"
            ]
            
            var_problema = tk.StringVar()
            var_problema.set(problemas[0])
            
            for problema in problemas:
                rb = tk.Radiobutton(opciones_frame, text=problema, font=("Consolas", 10),
                                 variable=var_problema, value=problema,
                                 bg="white", fg=self.color_texto, selectcolor="white",
                                 activebackground="white")
                rb.pack(anchor="w", padx=20, pady=3)
            
            tk.Button(diagnostico_frame, text="Iniciar Diagnóstico", font=("Consolas", 10, "bold"),
                    bg="#D32F2F", fg=self.color_texto_claro, padx=15, pady=8, bd=0).pack(pady=15)
            
            # Herramientas de reparación común
            tk.Label(reparacion_frame, text="Herramientas de Reparación Comunes", font=("Consolas", 14, "bold"),
                   bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(20, 10))
            
            herramientas = [
                ("🔄", "Restaurar Sistema", "Regresa el sistema a un estado anterior cuando funcionaba correctamente"),
                ("🧹", "Limpieza de Disco", "Elimina archivos temporales y basura del sistema para mejorar el rendimiento"),
                ("🔍", "Verificador de Archivos", "Analiza la integridad de los archivos del sistema y repara los dañados")
            ]
            
            for icono, titulo, desc in herramientas:
                self.crear_tarjeta(reparacion_frame, titulo, desc, icono, "Ejecutar")
            
            # Soporte técnico
            soporte_frame = tk.Frame(reparacion_frame, bg="#EEEEEE", bd=1, relief=tk.SOLID)
            soporte_frame.pack(fill=tk.X, pady=(20, 10), ipady=10)
            
            tk.Label(soporte_frame, text="¿Necesitas ayuda profesional?", font=("Consolas", 12, "bold"),
                   bg="#EEEEEE", fg=self.color_texto).pack(pady=(10, 5))
            
            tk.Label(soporte_frame, text="Contacta con nuestro equipo de soporte técnico para asistencia personalizada.",
                   font=("Consolas", 10), bg="#EEEEEE", fg=self.color_texto).pack()
            
            tk.Button(soporte_frame, text="Contactar Soporte", font=("Consolas", 10),
                    bg=self.color_acento, fg=self.color_texto_claro, padx=15, pady=5, bd=0).pack(pady=10)
            
        elif self.contenido_actual == "Tweaks":
            # Banner de tweaks
            banner_frame = tk.Frame(self.banner_frame, bg="#673AB7")  # Púrpura
            banner_frame.place(relwidth=1, relheight=1)
            
            tk.Label(banner_frame, text="Tweaks y Optimización", font=("Consolas", 24, "bold"),
                   bg="#673AB7", fg=self.color_texto_claro).pack(pady=(30, 10))
            
            tk.Label(banner_frame, text="Mejora el rendimiento y personaliza tu sistema", font=("Consolas", 12),
                   bg="#673AB7", fg=self.color_texto_claro).pack()
            
            # Contenedor principal con padding
            tweaks_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
            tweaks_frame.pack(fill=tk.BOTH, expand=True, padx=30)
            
            # Estilo para las pestañas
            estilo = ttk.Style()
            estilo.configure("TNotebook", background=self.color_fondo, borderwidth=0)
            estilo.configure("TNotebook.Tab", font=("Consolas", 10), padding=[10, 5])
            estilo.map("TNotebook.Tab", background=[("selected", "#673AB7")], 
                     foreground=[("selected", self.color_texto_claro)])
            
            notebook = ttk.Notebook(tweaks_frame)
            notebook.pack(fill=tk.BOTH, expand=True, pady=10)
            
            # Contenido de cada categoría de tweaks
            categorias = {
                "Rendimiento": [
                    {
                        "nombre": "Optimización de Inicio",
                        "desc": "Acelera el arranque del sistema deshabilitando programas innecesarios",
                        "opciones": [
                            ("Deshabilitar programas de inicio automático", True),
                            ("Optimizar servicios de arranque", False),
                            ("Reducir tiempo de espera de inicio", True)
                        ]
                    },
                    {
                        "nombre": "Ajustes de Memoria",
                        "desc": "Configura el uso de memoria para mejorar la respuesta del sistema",
                        "opciones": [
                            ("Optimizar memoria virtual", False),
                            ("Liberar memoria en segundo plano", True),
                            ("Priorizar programas en primer plano", True)
                        ]
                    }
                ],
                "Apariencia": [
                    {
                        "nombre": "Personalización Visual",
                        "desc": "Modifica la apariencia del sistema operativo",
                        "opciones": [
                            ("Habilitar modo oscuro", True),
                            ("Mostrar archivos ocultos", False),
                            ("Transparencia en menús", True)
                        ]
                    },
                    {
                        "nombre": "Barra de Tareas",
                        "desc": "Personaliza la barra de tareas para mayor eficiencia",
                        "opciones": [
                            ("Ocultar automáticamente", False),
                            ("Mostrar segundos en el reloj", True),
                            ("Iconos pequeños", False)
                        ]
                    }
                ],
                "Privacidad": [
                    {
                        "nombre": "Configuración de Telemetría",
                        "desc": "Controla qué información se envía al fabricante",
                        "opciones": [
                            ("Deshabilitar recopilación de datos", True),
                            ("Bloquear publicidad personalizada", True),
                            ("Limitar diagnósticos", True)
                        ]
                    },
                    {
                        "nombre": "Permisos de Aplicaciones",
                        "desc": "Gestiona los permisos de aplicaciones instaladas",
                        "opciones": [
                            ("Bloquear acceso a la cámara", False),
                            ("Bloquear acceso al micrófono", False),
                            ("Limitar acceso a ubicación", True)
                        ]
                    }
                ],
                "Gaming": [
                    {
                        "nombre": "Modo Juego",
                        "desc": "Optimiza el sistema para mejor rendimiento en juegos",
                        "opciones": [
                            ("Activar modo de alto rendimiento", True),
                            ("Priorizar GPU para juegos", True),
                            ("Deshabilitar efectos visuales", False)
                        ]
                    },
                    {
                        "nombre": "Configuración Avanzada",
                        "desc": "Ajustes para jugadores experimentados",
                        "opciones": [
                            ("Optimizar latencia de red", False),
                            ("Ajustes avanzados de DirectX", False),
                            ("Overclocking seguro", False)
                        ]
                    }
                ]
            }
            
            # Crear pestañas y su contenido
            for categoria, tweaks in categorias.items():
                # Frame para la categoría con scroll
                cat_main_frame = tk.Frame(notebook, bg=self.color_fondo)
                notebook.add(cat_main_frame, text=categoria)
                
                # Añadir scroll interno a cada pestaña
                cat_canvas = tk.Canvas(cat_main_frame, bg=self.color_fondo, highlightthickness=0)
                cat_scrollbar = ttk.Scrollbar(cat_main_frame, orient="vertical", command=cat_canvas.yview)
                cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
                
                cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                cat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                cat_frame = tk.Frame(cat_canvas, bg=self.color_fondo)
                cat_canvas_window = cat_canvas.create_window((0, 0), window=cat_frame, anchor="nw")
                
                # Configurar eventos de scroll para esta pestaña
                cat_canvas.bind('<Configure>', lambda e, c=cat_canvas, w=cat_canvas_window: 
                              self.on_tab_canvas_configure(e, c, w))
                cat_frame.bind('<Configure>', lambda e, c=cat_canvas: 
                            self.on_tab_frame_configure(e, c))
                
                # Permitir scroll con la rueda del mouse en esta pestaña
                cat_canvas.bind('<MouseWheel>', lambda e, c=cat_canvas: 
                              self.on_tab_mousewheel(e, c))
                
                # Iterar sobre los grupos de tweaks
                for tweak in tweaks:
                    # Crear frame para el grupo de tweaks
                    tweak_frame = tk.Frame(cat_frame, bg="white", bd=1, relief=tk.SOLID)
                    tweak_frame.pack(fill=tk.X, pady=10, padx=5, ipady=10)
                    
                    # Encabezado del tweak
                    tk.Label(tweak_frame, text=tweak["nombre"], font=("Consolas", 12, "bold"),
                           bg="white", fg=self.color_texto).pack(anchor="w", padx=15, pady=(10, 5))
                    
                    # Descripción
                    tk.Label(tweak_frame, text=tweak["desc"], font=("Consolas", 10),
                           bg="white", fg=self.color_secundario).pack(anchor="w", padx=15, pady=(0, 10))
                    
                    # Separador
                    ttk.Separator(tweak_frame, orient="horizontal").pack(fill=tk.X, padx=15, pady=5)
                    
                    # Opciones del tweak (checkboxes)
                    opciones_frame = tk.Frame(tweak_frame, bg="white")
                    opciones_frame.pack(fill=tk.X, padx=15, pady=5)
                    
                    for texto, valor in tweak["opciones"]:
                        var = tk.BooleanVar(value=valor)
                        
                        fila = tk.Frame(opciones_frame, bg="white")
                        fila.pack(fill=tk.X, pady=3)
                        
                        cb = tk.Checkbutton(fila, text=texto, variable=var, font=("Consolas", 10),
                                       bg="white", fg=self.color_texto, selectcolor="white",
                                       activebackground="white")
                        cb.pack(side=tk.LEFT)
                        
                        # Etiqueta "Recomendado" para opciones marcadas por defecto
                        if valor:
                            recomendado = tk.Label(fila, text="Recomendado", font=("Consolas", 8),
                                              bg="#E8F5E9", fg="#2E7D32", padx=5, pady=2)
                            recomendado.pack(side=tk.LEFT, padx=10)
                    
                    # Botón de aplicar para este grupo
                    tk.Button(tweak_frame, text="Aplicar cambios", font=("Consolas", 10),
                            bg="#673AB7", fg=self.color_texto_claro, 
                            padx=15, pady=5, bd=0).pack(anchor="e", padx=15, pady=10)
            
            # Perfil de optimización
            perfil_frame = tk.Frame(tweaks_frame, bg="#EEEEEE", bd=1, relief=tk.SOLID)
            perfil_frame.pack(fill=tk.X, pady=(20, 30), ipady=10)  # Añadir padding al final
            
            tk.Label(perfil_frame, text="Perfiles de Optimización", font=("Consolas", 12, "bold"),
                   bg="#EEEEEE", fg=self.color_texto).pack(pady=(10, 5))
            
            tk.Label(perfil_frame, text="Aplica un conjunto predefinido de tweaks según tus necesidades",
                   font=("Consolas", 10), bg="#EEEEEE", fg=self.color_texto).pack()
            
            # Botones de perfiles
            perfiles_frame = tk.Frame(perfil_frame, bg="#EEEEEE")
            perfiles_frame.pack(pady=10)
            
            perfiles = ["Balanceado", "Máximo Rendimiento", "Ahorro de Energía", "Gaming", "Productividad"]
            
            for perfil in perfiles:
                btn = tk.Button(perfiles_frame, text=perfil, font=("Consolas", 10),
                             bg="white", fg=self.color_texto, padx=10, pady=5, bd=1)
                btn.pack(side=tk.LEFT, padx=5)
    
    def on_tab_canvas_configure(self, event, canvas, window):
        """Ajustar el ancho del frame interno al cambiar el tamaño del canvas en las pestañas"""
        canvas.itemconfig(window, width=event.width)
    
    def on_tab_frame_configure(self, event, canvas):
        """Ajustar la región de desplazamiento al cambiar el tamaño del frame en las pestañas"""
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def on_tab_mousewheel(self, event, canvas):
        """Permitir desplazamiento con la rueda del mouse en las pestañas"""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Pie de página para la aplicación
class PiePagina(tk.Frame):
    def __init__(self, parent, color_fondo, color_texto, app_name="ToolboXBS"):
        super().__init__(parent, bg=color_fondo, height=80)
        self.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Contenido del pie de página
        contenido_frame = tk.Frame(self, bg=color_fondo)
        contenido_frame.pack(fill=tk.X, pady=10)
        
        # Columna izquierda - Logo y derechos
        col_izq = tk.Frame(contenido_frame, bg=color_fondo)
        col_izq.pack(side=tk.LEFT, padx=20)
        
        # Logo en blanco y negro
        tk.Label(col_izq, text=app_name, font=("Consolas", 14, "bold"), 
               bg=color_fondo, fg=color_texto).pack(anchor="w")
        
        tk.Label(col_izq, text="© 2025 Brandon Sepúlveda. Todos los derechos reservados.", 
               font=("Consolas", 8), bg=color_fondo, fg=color_texto).pack(anchor="w", pady=(5, 0))
        
        # Columna central - Enlaces rápidos
        col_centro = tk.Frame(contenido_frame, bg=color_fondo)
        col_centro.pack(side=tk.LEFT, padx=30, fill=tk.Y)
        
        tk.Label(col_centro, text="Enlaces Rápidos", font=("Consolas", 10, "bold"), 
               bg=color_fondo, fg=color_texto).pack(anchor="w", pady=(0, 5))
        
        enlaces = ["Inicio", "Soporte", "Documentación", "Actualizaciones"]
        for enlace in enlaces:
            link = tk.Label(col_centro, text=enlace, font=("Consolas", 8), 
                          bg=color_fondo, fg=color_texto, cursor="hand2")
            link.pack(side=tk.LEFT, padx=10)
        
        # Columna derecha - Versión
        col_der = tk.Frame(contenido_frame, bg=color_fondo)
        col_der.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(col_der, text="Versión 2.5.1", font=("Consolas", 8), 
               bg=color_fondo, fg=color_texto).pack(side=tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionToolboXBS(root)
    
    # Agregar el pie de página
    pie = PiePagina(root, "#000000", "#FFFFFF", "ToolboXBS")
    
    root.mainloop()