#!/usr/bin/env python3

from app import app
from models import db, Recipe, Category, Ingredient

with app.app_context():
    # Clear existing data
    Ingredient.query.delete()
    Recipe.query.delete()
    Category.query.delete()
    db.session.commit()

    # Create categories
    appetizer = Category(name="Appetizer")
    main_course = Category(name="Main Course")
    dessert = Category(name="Dessert")

    db.session.add_all([appetizer, main_course, dessert])
    db.session.commit()

    # Create recipes
    recipe1 = Recipe(name="Bruschetta", description="A delicious appetizer with tomatoes, garlic, and basil.", category_id=appetizer.id, user_id=1)
    recipe2 = Recipe(name="Pizza Margherita", description="A classic pizza with mozzarella, tomatoes, and basil.", category_id=main_course.id, user_id=1)
    recipe3 = Recipe(name="Tiramisu", description="A famous Italian dessert with coffee, mascarpone cheese, and cocoa.", category_id=dessert.id, user_id=1)

    db.session.add_all([recipe1, recipe2, recipe3])
    db.session.commit()

    # Create ingredients (if any)
    ingredient1 = Ingredient(name="Tomatoes", recipe_id=recipe1.id)
    ingredient2 = Ingredient(name="Mozzarella", recipe_id=recipe2.id)
    ingredient3 = Ingredient(name="Mascarpone", recipe_id=recipe3.id)

    db.session.add_all([ingredient1, ingredient2, ingredient3])
    db.session.commit()

    print("Seeding done!")
