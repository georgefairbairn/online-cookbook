import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-lefha.mongodb.net/online_cookbook?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())
    

@app.route('/add_recipe') 
def add_recipe():
    return render_template('add_recipe.html')


@app.route('/increase_likes/<recipe_id>')
def increase_likes(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    current_likes = int(the_recipe['likes'])
    new_likes = str(current_likes + 1)
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)},
    {
        'name': the_recipe['name'],
        'ingredients': the_recipe['ingredients'],
        'author': the_recipe['author'],
        'cuisine': the_recipe['cuisine'],
        'vegetarian': the_recipe['vegetarian'],
        'serves': the_recipe['serves'],
        'difficulty': the_recipe['difficulty'],
        'preparation_time': the_recipe['preparation_time'],
        'cooking_time': the_recipe['cooking_time'],
        'method': the_recipe['method'],
        'photo_link': the_recipe['photo_link'],
        'views': the_recipe['views'],
        'likes': new_likes
    })
    return redirect(url_for('get_recipes'))
    
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    form = request.form.to_dict()
    keys = list(form.keys())
    ingredient_names = []
    ingredient_amounts=[]
    steps = []
    
    for key in keys:
        if 'ingredient_name' in key:
            ingredient_names.append(key)
        elif 'ingredient_amount' in key:
            ingredient_amounts.append(key)
        elif 'step' in key:
            steps.append(key)
            
    ingredient_names.sort()
    ingredient_amounts.sort()
    steps.sort()
    
    for i in steps:
        step_instruction = request.form.get(i)
        step_number = steps.index(i)
        steps[step_number] = step_instruction
    
    ingredient_dict = dict(zip(ingredient_names, ingredient_amounts))
    ingredients = {}
    
    for name, amount in ingredient_dict.items():
        name_val = request.form.get(name)
        amount_val = request.form.get(amount)
        ingredients[name_val] = amount_val
        
    photo_link = request.form.get('recipe_photo')     
    if not photo_link:
        photo_link = '/static/img/default.jpg'
        
    recipe = {
        'name': request.form.get('recipe_name'),
        'ingredients': ingredients,
        'author': request.form.get('recipe_author'),
        'cuisine': request.form.get('cuisine'),
        'vegetarian': request.form.get('vegetarian'),
        'serves': request.form.get('recipe_serves'),
        'difficulty': request.form.get('difficulty'),
        'preparation_time': request.form.get('recipe_prep_time'),
        'cooking_time': request.form.get('recipe_cook_time'),
        'method': steps,
        'photo_link': photo_link,
        'views': 0,
        'likes': 0
    }
    
    recipes = mongo.db.recipes
    recipes.insert_one(recipe)
    return redirect(url_for('get_recipes'))
    

@app.route('/open_recipe/<recipe_id>')
def open_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$inc': {'views': 1}})
    
    return render_template('open_recipe.html', recipe = the_recipe)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe=the_recipe)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    form = request.form.to_dict()
    keys = list(form.keys())
    ingredient_names = []
    ingredient_amounts=[]
    steps = []
    
    for key in keys:
        if 'ingredient_name' in key:
            ingredient_names.append(key)
        elif 'ingredient_amount' in key:
            ingredient_amounts.append(key)
        elif 'step' in key:
            steps.append(key)
            
    ingredient_names.sort()
    ingredient_amounts.sort()
    steps.sort()
    
    for i in steps:
        step_instruction = request.form.get(i)
        step_number = steps.index(i)
        steps[step_number] = step_instruction
    
    ingredient_dict = dict(zip(ingredient_names, ingredient_amounts))
    ingredients = {}
    
    for name, amount in ingredient_dict.items():
        name_val = request.form.get(name)
        amount_val = request.form.get(amount)
        ingredients[name_val] = amount_val
        
    photo_link = request.form.get('recipe_photo')     
    if not photo_link:
        photo_link = '/static/img/default.jpg'
    
    recipes = mongo.db.recipes    
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        
    recipe = {
        'name': request.form.get('recipe_name'),
        'ingredients': ingredients,
        'author': request.form.get('recipe_author'),
        'cuisine': request.form.get('cuisine'),
        'vegetarian': request.form.get('vegetarian'),
        'serves': request.form.get('recipe_serves'),
        'difficulty': request.form.get('difficulty'),
        'preparation_time': request.form.get('recipe_prep_time'),
        'cooking_time': request.form.get('recipe_cook_time'),
        'method': steps,
        'photo_link': photo_link,
        'views': the_recipe['views'],
        'likes': the_recipe['likes']
    }
    
    recipes.update({'_id': ObjectId(recipe_id)}, recipe)
    return redirect(url_for('open_recipe', recipe_id = the_recipe['_id']))
    
    
@app.route('/filter_recipes/<cuisine>')
def filter_recipes(cuisine):
    return render_template('recipes.html', recipes=mongo.db.recipes.find({'cuisine': cuisine}))
    
@app.route('/order_recipes/<criteria>')
def order_recipes(criteria):
    return render_template('recipes.html', recipes=mongo.db.recipes.find().sort(criteria, -1))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)