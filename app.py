import streamlit as st
from spoonacular import search_recipes, get_random_recipe
from deep_translator import GoogleTranslator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure page
st.set_page_config(
    page_title="🍳 Chef Virtual",
    layout="centered",
    page_icon="👩‍🍳",
    menu_items={
        "Get Help": "https://github.com/your-repo",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": "# Chef Virtual de Receitas\nEncontre receitas deliciosas!",
    },
)
st.title("👩‍🍳 Chef Virtual de Receitas")


# Translation functions
def translate_to_english(text):
    """Translate Portuguese text to English for API calls"""
    try:
        if not text or str(text).strip() == "":
            return text
        return GoogleTranslator(source="pt", target="en").translate(str(text))
    except Exception as e:
        logger.error(f"Translation error (pt->en): {e}")
        return text


def translate_to_portuguese(text):
    """Translate English text to Portuguese for display"""
    try:
        if not text or str(text).strip() == "":
            return text
        return GoogleTranslator(source="en", target="pt").translate(str(text))
    except Exception as e:
        logger.error(f"Translation error (en->pt): {e}")
        return text


# Initialize session state
if "recipe_history" not in st.session_state:
    st.session_state.recipe_history = []

# Welcome message
with st.chat_message("assistant"):
    st.markdown("""
    Olá! Eu sou seu chef virtual. 🍴  
    Diga o que você está com vontade de comer e eu vou encontrar receitas deliciosas para você!
    """)

# User input
user_input = st.chat_input(
    "Digite um ingrediente ou prato (ex: frango, massa vegana, bolo de chocolate)..."
)

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Procurando receitas..."):
            # Translate user input to English for API
            translated_query = translate_to_english(user_input)
            logger.info(f"Original: '{user_input}' | Traduzido: '{translated_query}'")

            # Search recipes
            recipes = search_recipes(query=translated_query, language="en", number=3)

            if recipes:
                for i, recipe in enumerate(recipes):
                    # Translate recipe content back to Portuguese
                    try:
                        translated_recipe = {
                            "title": translate_to_portuguese(recipe["title"]),
                            "ingredients": [
                                translate_to_portuguese(ing)
                                for ing in recipe["ingredients"]
                            ],
                            "instructions": translate_to_portuguese(
                                recipe["instructions"]
                            ),
                            "image": recipe["image"],
                            "id": recipe["id"],
                        }
                    except Exception as e:
                        logger.error(f"Error translating recipe: {e}")
                        translated_recipe = recipe

                    st.session_state.recipe_history.append(translated_recipe)

                    with st.expander(
                        f"🍽️ {translated_recipe['title']}", expanded=i == 0
                    ):
                        if translated_recipe["image"]:
                            st.image(translated_recipe["image"], use_container_width=True)

                        st.markdown("#### 📝 Ingredientes:")
                        for ing in translated_recipe["ingredients"]:
                            st.markdown(f"- {ing.capitalize()}")

                        st.markdown("#### 🧑‍🍳 Modo de Preparo:")
                        st.markdown(
                            translated_recipe["instructions"], unsafe_allow_html=True
                        )

                        st.markdown("---")

                st.success("🍴 Pronto! Aqui estão algumas opções para você!")
            else:
                st.error("""
                Não encontrei receitas com esses termos.  
                Tente algo como:
                - 'frango assado'
                - 'macarrão integral'
                - 'sobremesa fácil'
                """)

# Recipe history in sidebar
if st.session_state.recipe_history:
    with st.sidebar:
        st.header("📜 Histórico")
        unique_recipes = {}
        for recipe in reversed(st.session_state.recipe_history):
            if recipe["id"] not in unique_recipes:
                unique_recipes[recipe["id"]] = recipe
                if st.button(recipe["title"], key=f"hist_{recipe['id']}"):
                    st.session_state.show_recipe = recipe

# Show recipe from history
if "show_recipe" in st.session_state:
    recipe = st.session_state.show_recipe
    del st.session_state.show_recipe

    with st.chat_message("assistant"):
        with st.expander(f"🍽️ {recipe['title']}", expanded=True):
            if recipe["image"]:
                st.image(recipe["image"], use_container_width=True)

            st.markdown("#### 📝 Ingredientes:")
            for ing in recipe["ingredients"]:
                st.markdown(f"- {ing.capitalize()}")

            st.markdown("#### 🧑‍🍳 Modo de Preparo:")
            st.markdown(recipe["instructions"], unsafe_allow_html=True)

# Random recipe button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🍀 Receita Aleatória"):
        with st.spinner("Procurando uma receita surpresa..."):
            random_recipe = get_random_recipe(language="en")
            if random_recipe:
                try:
                    translated_recipe = {
                        "title": translate_to_portuguese(random_recipe["title"]),
                        "ingredients": [
                            translate_to_portuguese(ing)
                            for ing in random_recipe["ingredients"]
                        ],
                        "instructions": translate_to_portuguese(
                            random_recipe["instructions"]
                        ),
                        "image": random_recipe["image"],
                        "id": random_recipe["id"],
                    }
                    st.session_state.recipe_history.append(translated_recipe)
                    st.session_state.show_recipe = translated_recipe
                    st.rerun()
                except Exception as e:
                    st.error("Erro ao obter receita aleatória")
                    logger.error(f"Random recipe error: {e}")
