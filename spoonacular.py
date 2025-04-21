import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")


def clean_instructions(instructions):
    """Clean HTML tags from instructions or format them properly"""
    if not instructions:
        return "Instruções não disponíveis."

    # Remove HTML tags but preserve list items by replacing </li> with newlines
    cleaned = re.sub(r"<li>", "\n- ", instructions)  # Convert <li> to bullet points
    cleaned = re.sub(r"<[^>]+>", "", cleaned)  # Remove all other HTML tags
    cleaned = cleaned.replace("\n\n", "\n").strip()  # Clean up extra newlines

    return cleaned if cleaned else "Instruções não disponíveis."


def extract_recipe_data(recipe):
    """Helper to safely extract recipe data"""
    ingredients = [
        ing.get("original", ing.get("name", "Ingrediente desconhecido"))
        for ing in recipe.get("extendedIngredients", [])
    ] or ["Nenhum ingrediente listado"]

    instructions = clean_instructions(recipe.get("instructions"))
    image = recipe.get("image", None)

    return {
        "title": recipe.get("title", "Receita sem título"),
        "ingredients": ingredients,
        "instructions": instructions,
        "image": image,
        "id": recipe.get("id"),
    }


def search_recipes(query, diet=None, language="pt", number=3):
    """Improved search function with better Portuguese support"""
    search_url = "https://api.spoonacular.com/recipes/complexSearch"
    info_url_template = "https://api.spoonacular.com/recipes/{id}/information"

    search_params = {
        "query": query,
        "number": number,
        "apiKey": API_KEY,
        "language": language,
        "instructionsRequired": True,
        "addRecipeInformation": True,  # Get more data in initial search
    }

    if diet:
        search_params["diet"] = diet

    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data.get("results"):
            # Return all found recipes (up to 'number' results)
            recipes = []
            for result in search_data["results"]:
                # If basic info is available, use it
                if "extendedIngredients" in result:
                    recipes.append(extract_recipe_data(result))
                else:
                    # Otherwise fetch full details
                    recipe_id = result["id"]
                    info_url = info_url_template.format(id=recipe_id)
                    info_response = requests.get(
                        info_url, params={"apiKey": API_KEY, "language": language}
                    )
                    if info_response.status_code == 200:
                        recipes.append(extract_recipe_data(info_response.json()))

            return recipes if recipes else None

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")

    return None


def get_random_recipe(language="pt"):
    """Get random recipe with Portuguese support"""
    url = "https://api.spoonacular.com/recipes/random"
    params = {
        "number": 1,
        "apiKey": API_KEY,
        "language": language,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("recipes"):
            return extract_recipe_data(data["recipes"][0])

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")

    return None


def get_recipe_by_id(recipe_id, language="pt"):
    """Get recipe by ID with Portuguese support"""
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": API_KEY,
        "language": language,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return extract_recipe_data(data)

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")

    return None


def get_recipe_nutrition(recipe_id, language="pt"):
    """Get nutrition information with Portuguese support"""
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    params = {
        "apiKey": API_KEY,
        "language": language,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "calories": data.get("calories", "Informação não disponível"),
            "fat": data.get("fat", "Informação não disponível"),
            "carbs": data.get("carbs", "Informação não disponível"),
            "protein": data.get("protein", "Informação não disponível"),
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {e}")

    return None


# Helper functions remain similar but with Portuguese defaults
def get_recipe_ingredients(recipe_id, language="pt"):
    recipe = get_recipe_by_id(recipe_id, language)
    return recipe["ingredients"] if recipe else None


def get_recipe_instructions(recipe_id, language="pt"):
    recipe = get_recipe_by_id(recipe_id, language)
    return recipe["instructions"] if recipe else None


def get_recipe_image(recipe_id, language="pt"):
    recipe = get_recipe_by_id(recipe_id, language)
    return recipe["image"] if recipe else None
