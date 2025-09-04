import streamlit as st
import random
import time

# -------------------------
# Datos de preguntas
# -------------------------
preguntas = {
    "Fútbol": [
        {"pregunta": "¿Quién ganó el Mundial 2010?", "opciones": ["España", "Holanda", "Brasil"], "respuesta": "España"},
        {"pregunta": "¿Cuál es el equipo con más Champions League?", "opciones": ["Real Madrid", "Barcelona", "Milan"], "respuesta": "Real Madrid"},
    ],
    "Cultura General": [
        {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": ["Da Vinci", "Picasso", "Van Gogh"], "respuesta": "Da Vinci"},
        {"pregunta": "¿Cuál es la capital de Japón?", "opciones": ["Seúl", "Pekín", "Tokio"], "respuesta": "Tokio"},
    ],
    "Matemáticas": [
        {"pregunta": "¿Cuánto es 7 x 8?", "opciones": ["54", "56", "64"], "respuesta": "56"},
        {"pregunta": "¿La raíz cuadrada de 81 es...?", "opciones": ["9", "8", "7"], "respuesta": "9"},
    ],
}

# -------------------------
# Funciones del juego
# -------------------------
def iniciar_trivia(categoria):
    st.session_state["categoria"] = categoria
    st.session_state["preguntas"] = random.sample(preguntas[categoria], len(preguntas[categoria]))
    st.session_state["indice"] = 0
    st.session_state["vidas"] = 3
    st.session_state["puntaje"] = 0
    st.session_state["pantalla"] = "juego"


def jugar_penaltis():
    st.session_state["pantalla"] = "penaltis"
    st.session_state["penales"] = 5
    st.session_state["goles"] = 0
    st.session_state["tiros"] = 0


# -------------------------
# Interfaz de Trivia
# -------------------------
def pantalla_trivia():
    if st.session_state["vidas"] <= 0 or st.session_state["indice"] >= len(st.session_state["preguntas"]):
        st.subheader("🎉 Juego terminado")
        st.write(f"⭐ Puntaje final: {st.session_state['puntaje']}")
        st.write("❤️ Vidas restantes:", st.session_state["vidas"])
        if st.button("Volver al menú"):
            st.session_state["pantalla"] = "menu"
        return

    pregunta = st.session_state["preguntas"][st.session_state["indice"]]
    st.subheader(f"Categoría: {st.session_state['categoria']}")
    st.write(f"❤️ Vidas: {st.session_state['vidas']} | ⭐ Puntaje: {st.session_state['puntaje']}")

    st.write(f"**{pregunta['pregunta']}**")
    opcion = st.radio("Elige tu respuesta:", pregunta["opciones"], key=f"preg_{st.session_state['indice']}")

    if st.button("Responder"):
        if opcion == pregunta["respuesta"]:
            st.success("✅ Correcto!")
            st.session_state["puntaje"] += 10
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['respuesta']}")
            st.session_state["vidas"] -= 1
        st.session_state["indice"] += 1
        time.sleep(1)
        st.experimental_rerun()


# -------------------------
# Interfaz Penaltis
# -------------------------
def pantalla_penaltis():
    if st.session_state["tiros"] >= st.session_state["penales"]:
        st.subheader("⚽ Fin de la tanda de penaltis")
        st.write(f"Goles: {st.session_state['goles']} de {st.session_state['penales']}")
        if st.session_state["goles"] >= 3:
            st.success("¡Ganaste la tanda! 🏆")
        else:
            st.error("Perdiste la tanda ❌")
        if st.button("Volver al menú"):
            st.session_state["pantalla"] = "menu"
        return

    st.subheader(f"Tiro {st.session_state['tiros']+1} de {st.session_state['penales']}")
    portero = random.choice(["Izquierda", "Centro", "Derecha"])

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Izquierda"):
            evaluar_penal("Izquierda", portero)
    with col2:
        if st.button("⬆️ Centro"):
            evaluar_penal("Centro", portero)
    with col3:
        if st.button("➡️ Derecha"):
            evaluar_penal("Derecha", portero)


def evaluar_penal(eleccion, portero):
    st.session_state["tiros"] += 1
    if eleccion == portero:
        st.error(f"❌ Fallaste, el portero adivinó ({portero})")
    else:
        st.success(f"⚽ ¡Gol! Portero se lanzó a {portero}")
        st.session_state["goles"] += 1
    time.sleep(1)
    st.experimental_rerun()


# -------------------------
# Menú Principal
# -------------------------
def menu():
    st.title("🎮 Trivia y Penaltis")
    st.write("Elige una categoría para jugar:")

    for categoria in preguntas.keys():
        if st.button(categoria):
            iniciar_trivia(categoria)

    st.write("---")
    st.subheader("⚽ Extra")
    if st.button("Jugar Penaltis"):
        jugar_penaltis()


# -------------------------
# Flujo principal
# -------------------------
if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "menu"

if st.session_state["pantalla"] == "menu":
    menu()
elif st.session_state["pantalla"] == "juego":
    pantalla_trivia()
elif st.session_state["pantalla"] == "penaltis":
    pantalla_penaltis()
