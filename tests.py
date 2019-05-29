import unittest
from app import app
from flask_pymongo import PyMongo

class TestOnlineCookbook(unittest.TestCase):

    # Ensure Flask app loads correctly
    def test_flask(self):
        app.app_context
        client = app.test_client(self)
        response = client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure all recipes page loads correctly
    def test_all_recipes_page_loaded(self):
        client = app.test_client(self)
        response = client.get('/', content_type='html/text')
        self.assertTrue(b'<div class="card hoverable large">' in response.data)

    # Ensure the add_recipe template renders correctly
    def test_add_recipe_loaded(self):
        client = app.test_client(self)
        response = client.get('/add_recipe', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    # Ensure inserting test recipe to database works
    # REMEMBER TO DELETE RECORD MANUALLY AFTER RUNNING TESTS
    def test_insert_recipe(self):
        client = app.test_client(self)
        response = client.post('/insert_recipe', data={
            'recipe_name': "test recipe",
            'ingredient_name1': "test ingredient 1",
            'ingredient_name2': "test ingredient 2",
            'ingredient_name3': "test ingredient 3",
            'ingredient_amount1': "test amount 1",
            'ingredient_amount2': "test amount 2",
            'ingredient_amount3': "test amount 3",
            'recipe_author': "tester",
            'cuisine': "Thai",
            'vegetarian': "on",
            'serves': "4",
            'difficulty': "Easy",
            'preparation_time': "15 mins",
            'cooking_time': "30 mins",
            'step1': "test step 1",
            'step2': "test step 2",
            'step3': "test step 3",
            'views': 0,
            'likes': 0
        }, follow_redirects=True)
        self.assertIn(b'<h4 class="title center-align">test recipe</h4>', response.data)
     
    # Ensure correct filter recipes by cuisine loads correctly
    def test_set_filter_cuisine(self):
        client = app.test_client(self)
        response = client.get('/filter_recipes/Thai', content_type='html/text')
        self.assertTrue(b'<div class="card hoverable large">' in response.data)
        
    # Ensure incorrect filter recipes does not load recipes
    def test_set_incorrect_filter_cuisine(self):
        client = app.test_client(self)
        response = client.get('/filter_recipes/IncorrectCuisine', content_type='html/text')
        self.assertFalse(b'<div class="card hoverable large">' in response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)