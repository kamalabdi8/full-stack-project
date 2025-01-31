from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Recipe, Category, db  # Import from models.py

# Initialize app and migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

CORS(app, supports_credentials=True)

# CRUD functions for categories
def create_category(data):
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return new_category

def get_all_categories():
    return Category.query.all()

def delete_category_by_id(category_id):
    category = Category.query.get(category_id)
    if not category:
        return None
    db.session.delete(category)
    db.session.commit()
    return category

# Category Routes
@app.route('/categories', methods=['GET', 'POST'])
def handle_categories():
    if request.method == 'GET':
        categories = get_all_categories()
        return jsonify([{'id': cat.id, 'name': cat.name} for cat in categories])
    
    if request.method == 'POST':
        data = request.json
        new_category = create_category(data)
        return jsonify({'id': new_category.id, 'name': new_category.name}), 201

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = delete_category_by_id(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({'message': 'Category deleted'}), 200

# CRUD functions for recipes
def create_recipe(data):
    category = Category.query.get(data['category_id'])
    if not category:
        return None
    new_recipe = Recipe(
        name=data['name'],
        description=data['description'],
        category_id=data['category_id'],
        user_id=1  # Assuming a user with ID 1 exists
    )
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe

def get_all_recipes():
    return Recipe.query.all()

def delete_recipe_by_id(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return None
    db.session.delete(recipe)
    db.session.commit()
    return recipe

# Recipe Routes
@app.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    if request.method == 'GET':
        recipes = get_all_recipes()
        return jsonify([
            {'id': r.id, 'name': r.name, 'description': r.description, 'ingredients': [{'name': i.name} for i in r.ingredients], 'category': r.category.name} 
            for r in recipes
        ])
    
    if request.method == 'POST':
        data = request.json
        new_recipe = create_recipe(data)
        if not new_recipe:
            return jsonify({'error': 'Invalid category ID'}), 400
        return jsonify({'id': new_recipe.id, 'name': new_recipe.name, 'category': new_recipe.category.name}), 201

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = delete_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify({'message': 'Recipe deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
