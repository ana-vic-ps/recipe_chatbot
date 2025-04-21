from typing import Dict, List, Union

CHICKEN = "chicken"
PASTA = "pasta"
SALAD = "salad"
BEEF = "beef"

recipes: Dict[str, Dict[str, Union[str, List[str]]]] = {
    CHICKEN: {
        "title": "Grilled Chicken",
        "ingredients": ["Chicken breast", "Olive oil", "Garlic", "Rosemary", "Salt", "Pepper"],
        "instructions": "Marinate chicken with olive oil, garlic, and rosemary for 30 minutes. Grill on medium heat for 6-8 minutes per side until fully cooked."
    },
    PASTA: {
        "title": "Creamy Alfredo Pasta",
        "ingredients": ["Pasta", "Cream", "Parmesan", "Garlic", "Butter"],
        "instructions": "Boil pasta until al dente (8-10 minutes). In a pan, melt butter, sauté garlic, add cream, and simmer for 5 minutes. Stir in Parmesan and mix with pasta."
    },
    SALAD: {
        "title": "Fresh Garden Salad",
        "ingredients": ["Lettuce", "Tomato", "Cucumber", "Olive oil", "Lemon juice"],
        "instructions": "Chop all veggies into bite-sized pieces. Mix olive oil and lemon juice for dressing. Toss veggies with dressing and serve immediately."
    },
    BEEF: {
        "title": "Beef Stir Fry",
        "ingredients": ["Beef strips", "Soy sauce", "Ginger", "Bell peppers", "Onion"],
        "instructions": "Stir-fry beef strips with soy sauce, ginger, and vegetables over high heat for 5-7 minutes."
    },
}