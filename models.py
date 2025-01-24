from config import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Define the relationship with Ingredient
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients],
        }

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Define the relationship with Recipe
    recipes = db.relationship('Recipe', backref='category', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'recipes': [recipe.to_dict() for recipe in self.recipes],
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'recipe_id': self.recipe_id,
        }
