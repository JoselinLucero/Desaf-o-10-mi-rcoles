import streamlit as st #no pude importar la libreria
from groq import Groq

#primero configuro la ventana de mi web
st.set_page_config(page_icon = "Mi chat de IA", page_icon = "👌")

#el titulo de mi pagina
st.title("Mi primer App con Streamlit(sale mal)")

#Donde el usuario anota su primer dato
nombre = st.text_imput("¿como te llamas?")

#Boton con funcionalidad
if st.button("saludar)") :
    st.write(f"¡Bienvenido {nombre}!")

Modelo = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["clave API"]
    return Groq(api_key = clave_secreta)


def configuracion_modelo(cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model = modelo, mensaje = [{"role":"user", "content": mensaje}], stream = True)
        

def inicializar_estado():
    if "mensaje" not in st.session_states:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    #metodo para agregar datos
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar} 
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        while st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["contenido"])

def area_chat():
    contenidoChat = st.container(heigt=400, border = True)
    with contenidoChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" #variable vacia
    for frase in chat_completo:
        if frase.choice[0].delta.content:
            respuesta_completa += frase.choice[0].delta.content
            yield frase.choice[0].delta.content
    return respuesta_completa

def configurar_pagina():
    st.tittle("Mi chat IA")
    st.sidebar.tittle("Configuracion")
    elegirModelo = st.sidebar.selectbox(
        "elegi un modulo",
        Modelo,
        index = 0
    )
    return elegirModelo

def main():
    modelo = configurar_pagina()
    cliente_usuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()

    mensaje = st.chat_input("Escribe un mensaje. . .")

    if mensaje:
        actualizar_historial("user", mensaje, "🐕")
        chat_completo = configuracion_modelo(cliente_usuario, modelo, mensaje)
        if chat_completo:
            with st.chat_mensaje("assistent") :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistent", respuesta_completa, "🐈‍⬛")

    #nos conectamos a api
    def crear_usuario_groq():
        clave_secreta = st.secrets["clave api"] #obtener la clave
        return Groq(api_key = clave_secreta) #conecto la api

    def configurar_modelo(ciente, modelo, MensajedeEntrada):
        return ciente.chat.completions.create(
            model= modelo, #indica el modelo de la IA
            messages = [{"role": "user", "content":MensajedeEntrada}],
            stream = True
        )

    #historial demensaje
    def inicializar_estado():
        if "mensajes" not in st.sesion_star:
            st.session_state.mensajes = []

    def configurar_pagina():
        st.title("Mi chat de IA")#el titulo
        st.sidebar.title("Configuracion") #el menu lateral

    configurar_pagina() #y al final llamo a la funcion


    if mensaje:
        configurar_modelo(cliente_usuario, modelo, mensaje)
        print(mensaje)

if __name__ == "__main__":
    main()