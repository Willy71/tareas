import streamlit as st
import pandas as pd
import sqlite3

# -----------------------------------------------------------------------------------------------------------------------------
# Colocar nome na pagina, icone e ampliar a tela
st.set_page_config(
    page_title="Tareas",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)
# -----------------------------------------------------------------------------------------------------------------------------
# Estilo de pagina y background

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: ("589.jpg");
background-size: 180%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stSidebar"] {{
background: rgba(28,28,56,1);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------------------
# Funciones predefinidas para Frontend
def centrar_imagen(imagen, ancho):
    # Aplicar estilo CSS para centrar la imagen con Markdown
    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="{imagen}" width="{ancho}">'
        f'</div>',
        unsafe_allow_html=True
    )


def centrar_texto(texto, tamanho, color):
    st.markdown(f"<h{tamanho} style='text-align: center; color: {color}'>{texto}</h{tamanho}>",
                unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------------------------
# Funciones de backend
# Conectar a la base de datos


# Conectar a la base de datos
def conectar_base():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # Verificar si la tabla ya existe
    cur.execute("PRAGMA table_info(tareas);")
    if not cur.fetchall():
        # La tabla no existe, la creamos
        cur.execute('''CREATE TABLE IF NOT EXISTS tareas
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarea VARCHAR(200) NOT NULL,
                    status INTEGER NOT NULL)''')
    return con, cur


# Mostrar datos de la base de datos
def mostrar_db():
    con, cur = conectar_base()
    data = cur.execute('SELECT * FROM tareas ORDER BY user_id')
    st.dataframe(data,
                 width=700,
                 column_config={
                     "0": "ID",
                     "1": "Tarea",
                     "2": "Status"},
                 hide_index=True)

# Agregar datos a la base de datos


def agregar_datos(nombre, apellido):
    con, cur = conectar_base()
    # Insertar datos en la tabla
    cur.execute('INSERT INTO tareas (tarea, status) VALUES (?, ?)',
                (nombre, apellido))
    con.commit()
    con.close()
# -------------------------------------------------------------------------------------------------------------------------
# Crear la base de datos si no existe
con, cur = conectar_base()
con.close()
# -----------------------------------------------------------------------------------------------------------------------------


action = st.sidebar.selectbox(
    "Elija una opción...",
    [
        "Nueva tarea",
        "Pendientes",
        "Concluidas",
        "Borrar tarea",
    ],
)
# -------------------------------------------------------------------------------------------------------------------------

vendor_to_update = None  # Establecer un valor predeterminado

if action == "Nueva tarea":
    centrar_texto("Agregue una tarea", 3, "white")
    with st.form(key="Agregacion"):
        with st.container():
            col10, col11, col12 = st.columns([6, 2, 2])
            with col10:
                tarea = st.text_input("", label_visibility="collapsed")
            with col12:
                update_button = st.form_submit_button(label="Agregar")
            status = False
            if update_button:
                agregar_datos(tarea, status)
    # Consulta los datos desde la base de datos y conviértelos a un DataFrame
    con = sqlite3.connect('database.db')
    data_df = pd.read_sql_query('SELECT * FROM tareas ORDER BY user_id', con)
    con.close()

    # Convertir la columna user_id a texto para controlar el formato de visualización
    data_df['user_id'] = data_df['user_id'].astype(str)

    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = data_df.copy()

    # Muestra el editor de datos con el DataFrame convertido y las configuraciones de columna
    edited_data = st.data_editor(
        data_df,
        width=900,
        column_config={
            "status": st.column_config.CheckboxColumn(
                "Status",
                help="Seleccione su status. Si esta tildado esta completo",
                default=False,
            ),
            "user_id": st.column_config.NumberColumn(
                "ID",
                width="small",
            ),
            "tarea": st.column_config.TextColumn(
                "Tarea",
                width="large",
            ),
        },
        disabled=["Tareas"],
        hide_index=True
    )

    # Obtener los datos editados por el usuario desde el data editor
    if edited_data is not None:
        con, cur = conectar_base()
        for index, row in edited_data.iterrows():
            cur.execute('UPDATE tareas SET tarea=?, status=? WHERE user_id=?',
                        (row['tarea'], int(row['status']), int(row['user_id'])))
        con.commit()
        con.close()
        # Utilizar st.experimental_rerun para volver a ejecutar la sección específica del código
        #st.experimental_rerun()
        

# -------------------------------------------------------------------------------------------------------------------------
if action == "Pendientes":
    centrar_texto("Tareas pendientes", 3, "white")
    # Consulta los datos desde la base de datos y conviértelos a un DataFrame
    con = sqlite3.connect('database.db')
    data_df = pd.read_sql_query('SELECT * FROM tareas WHERE status=0', con)
    con.close()

    # Convertir la columna user_id a texto para controlar el formato de visualización
    data_df['user_id'] = data_df['user_id'].astype(str)

    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = data_df.copy()

    # Muestra el editor de datos con el DataFrame convertido y las configuraciones de columna
    edited_data = st.data_editor(
        data_df,
        width=900,
        column_config={
            "status": st.column_config.CheckboxColumn(
                "Status",
                help="Seleccione su status. Si esta tildado esta completo",
                default=False,
            ),
            "user_id": st.column_config.NumberColumn(
                "ID",
                width="small",
            ),
            "tarea": st.column_config.TextColumn(
                "Tarea",
                width="large",
            ),
        },
        disabled=["Tareas"],
        hide_index=True
    )

    # Obtener los datos editados por el usuario desde el data editor
    if edited_data is not None:
        con, cur = conectar_base()
        for index, row in edited_data.iterrows():
            cur.execute('UPDATE tareas SET tarea=?, status=? WHERE user_id=?',
                        (row['tarea'], int(row['status']), int(row['user_id'])))
        con.commit()
        con.close()
    
    col110, col111, col112, col113, col114 = st.columns([1,1,3,2,1])
    with col112:
        actualizar_button = st.button(label="Actualizar", use_container_width=True)
        if actualizar_button:
            st.experimental_rerun()
        
    

# -------------------------------------------------------------------------------------------------------------------------
if action == "Concluidas":
    centrar_texto("Tareas finalizadas", 3, "white")
    # Consulta los datos desde la base de datos y conviértelos a un DataFrame
    con = sqlite3.connect('database.db')
    data_df = pd.read_sql_query('SELECT * FROM tareas WHERE status=1', con)
    con.close()

    # Convertir la columna user_id a texto para controlar el formato de visualización
    data_df['user_id'] = data_df['user_id'].astype(str)

    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = data_df.copy()

    # Muestra el editor de datos con el DataFrame convertido y las configuraciones de columna
    edited_data = st.data_editor(
        data_df,
        width=900,
        column_config={
            "status": st.column_config.CheckboxColumn(
                "Status",
                help="Seleccione su status. Si esta tildado esta completo",
                default=False,
            ),
            "user_id": st.column_config.NumberColumn(
                "ID",
                width="small",
            ),
            "tarea": st.column_config.TextColumn(
                "Tarea",
                width="large",
            ),
        },
        disabled=["Tareas"],
        hide_index=True
    )

    # Obtener los datos editados por el usuario desde el data editor
    if edited_data is not None:
        con, cur = conectar_base()
        for index, row in edited_data.iterrows():
            cur.execute('UPDATE tareas SET tarea=?, status=? WHERE user_id=?',
                        (row['tarea'], int(row['status']), int(row['user_id'])))
        con.commit()
        con.close()
        # Utilizar st.experimental_rerun para volver a ejecutar la sección específica del código
        #st.experimental_rerun()
    col120, col121, col122, col123, col124 = st.columns([1,1,3,2,1])
    with col122:
        actualizar_button_2 = st.button(label="Actualizar", use_container_width=True)
        if actualizar_button_2:
            st.experimental_rerun()
        

# -------------------------------------------------------------------------------------------------------------------------
if action == "Borrar tarea":
    centrar_texto("Borre una tarea", 3, "white")
    with st.form(key="Borrado"):
        with st.container():
            # Consulta los datos desde la base de datos y conviértelos a un DataFrame
            con = sqlite3.connect('database.db')
            data_df = pd.read_sql_query(
                'SELECT * FROM tareas ORDER BY user_id', con)
            con.close()

            # Convertir la columna user_id a texto para controlar el formato de visualización
            data_df['user_id'] = data_df['user_id'].astype(str)

            if 'dataframe' not in st.session_state:
                st.session_state.dataframe = data_df.copy()

            # Muestra el editor de datos con el DataFrame convertido y las configuraciones de columna
            edited_data = st.data_editor(
                data_df,
                width=900,
                column_config={
                    "status": st.column_config.CheckboxColumn(
                        "Status",
                        help="Seleccione su status. Si esta tildado esta completo",
                        default=False,
                    ),
                    "user_id": st.column_config.NumberColumn(
                        "ID",
                        width="small",
                    ),
                    "tarea": st.column_config.TextColumn(
                        "Tarea",
                        width="large",
                    ),
                },
                disabled=["Tareas"],
                hide_index=True
            )
            col100, col101, col102, col103, col104 = st.columns([1,2,1,2,1])
            with col101:
                con, cur = conectar_base()
                data = cur.execute(
                    'SELECT user_id FROM tareas ORDER BY user_id')
                all_ids = [row[0] for row in data]
                vendor_to_update = st.selectbox(
                    "", index=None, placeholder="Elija una opcion..", label_visibility="collapsed", options=all_ids)
            with col103:
                clear_button = st.form_submit_button(label="Borrar", use_container_width=True)

            if clear_button:
                # Realizar la eliminación
                con, cur = conectar_base()
                cur.execute('DELETE FROM tareas WHERE user_id=?',
                            (vendor_to_update,))
                con.commit()
                con.close()
                # Utilizar st.experimental_rerun para volver a ejecutar la sección específica del código
                st.experimental_rerun()
                
                st.success("Datos eliminados exitosamente!")

            
