from flask import Blueprint, render_template, request, abort
from api.data import dev_posts

dev_blog_bp = Blueprint('dev_blog', __name__, url_prefix='/dev-blog')

@dev_blog_bp.route('/')
def dev_blog_index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').lower()
    
    if search:
        filtered_posts = [p for p in dev_posts if search in p['title'].lower() or search in p['content'].lower()]
    else:
        filtered_posts = dev_posts

    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = filtered_posts[start:end]
    total_pages = (len(filtered_posts) + per_page - 1) // per_page
    
    return render_template('blog/index.html', posts=paginated_posts, page=page, total_pages=total_pages, search=search)

@dev_blog_bp.route('/<slug>')
def dev_blog_post(slug):
    post = next((p for p in dev_posts if p['slug'] == slug), None)
    if post is None:
        abort(404)
    related_posts = [p for p in dev_posts if p['slug'] in post.get('related', [])]
    return render_template('blog/blog_post.html', post=post, related_posts=related_posts) 