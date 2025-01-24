from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import db
from models import Recipe, Category, Ingredient

app = Flask(__name__)
CORS(app)
api = Api(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Updated to use `app.db`
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {'message': 'Recipe Restaurant Backend'}

# Recipe CRUD routes
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    new_recipe = Recipe(name=data['name'], description=data.get('description'), category_id=data['category_id'])
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe.to_dict())

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()
    recipe.name = data.get('name', recipe.name)
    recipe.description = data.get('description', recipe.description)
    recipe.category_id = data.get('category_id', recipe.category_id)
    db.session.commit()
    return jsonify(recipe.to_dict())

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204

# Category CRUD routes
@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify(category.to_dict())

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204

# Ingredient CRUD routes
@app.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    recipe = Recipe.query.get_or_404(data['recipe_id'])
    new_ingredient = Ingredient(name=data['name'], quantity=data['quantity'], recipe_id=recipe.id)
    db.session.add(new_ingredient)
    db.session.commit()
    return jsonify(new_ingredient.to_dict()), 201

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients])

@app.route('/ingredients/<int:id>', methods=['GET'])
def get_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    return jsonify(ingredient.to_dict())

@app.route('/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    data = request.get_json()
    ingredient.name = data.get('name', ingredient.name)
    ingredient.quantity = data.get('quantity', ingredient.quantity)
    db.session.commit()
    return jsonify(ingredient.to_dict())

@app.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5000, debug=True)
