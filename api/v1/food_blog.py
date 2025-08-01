from flask import Blueprint, render_template, request, abort
from api.data import recipes

food_blog_bp = Blueprint('food_blog', __name__, url_prefix='/food-blog')

@food_blog_bp.route('/')
def food_blog_index():
    search = request.args.get('search', '').lower()
    selected_categories = request.args.getlist('category')
    selected_cuisines = request.args.getlist('cuisine')
    
    filtered_recipes = recipes

    if search:
        filtered_recipes = [r for r in filtered_recipes if search in r['title'].lower() or search in r['description'].lower()]
    if selected_categories:
        filtered_recipes = [r for r in filtered_recipes if r.get('category') in selected_categories]
    if selected_cuisines:
        filtered_recipes = [r for r in filtered_recipes if r.get('cuisine') in selected_cuisines]
        
    categories = sorted(list(set(r.get('category') for r in recipes if r.get('category'))))
    cuisines = sorted(list(set(r.get('cuisine') for r in recipes if r.get('cuisine'))))

    template = 'recipes/partials/recipe_grid.html' if request.headers.get('HX-Request') else 'recipes/index.html'

    return render_template(template, 
                           recipes=filtered_recipes, 
                           search=search, 
                           categories=categories, 
                           cuisines=cuisines,
                           selected_categories=selected_categories,
                           selected_cuisines=selected_cuisines)

@food_blog_bp.route('/<slug>')
def food_blog_recipe(slug):
    recipe = next((r for r in recipes if r['slug'] == slug), None)
    if recipe is None:
        abort(404)
    return render_template('recipes/recipe.html', recipe=recipe) 