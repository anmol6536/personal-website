from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from core.data_layer.images import add_image, get_image_by_id, get_all_images, update_image_by_id, delete_image_by_id
from core.utils import get_gps_from_exif, process_image_for_storage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'AdminPass123':
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def dashboard():
    images = get_all_images()
    return render_template('admin/index.html', images=images)

@admin_bp.route('/edit_image/<unique_id>')
@login_required
def edit_image_page(unique_id):
    image = get_image_by_id(unique_id)
    if image:
        return render_template('admin/edit_image.html', image=image)
    flash("Image not found.", "error")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_image/<unique_id>', methods=['POST'])
@login_required
def delete_image(unique_id):
    try:
        if delete_image_by_id(unique_id):
            flash("Image deleted successfully!", "success")
        else:
            flash("Failed to delete image. Image not found.", "error")
    except Exception as e:
        flash(f"Error deleting image: {str(e)}", "error")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/update_image/<unique_id>', methods=['POST'])
@login_required
def update_image(unique_id):
    caption = request.form.get('caption')
    location_str = request.form.get('location')
    tags_str = request.form.get('tags')
    
    # Handle location parsing with error handling
    location = None
    if location_str and location_str.strip():
        try:
            location = [float(x.strip()) for x in location_str.split(',')]
        except ValueError:
            flash("Invalid location format. Please use: lat, long", "error")
            return redirect(url_for('admin.edit_image_page', unique_id=unique_id))
    
    # Handle tags parsing
    tags = None
    if tags_str and tags_str.strip():
        tags = [t.strip() for t in tags_str.split(',') if t.strip()]
    
    # Handle caption
    if caption and not caption.strip():
        caption = None
    
    try:
        if update_image_by_id(unique_id, caption, location, tags):
            flash("Image updated successfully!", "success")
        else:
            flash("Failed to update image.", "error")
    except Exception as e:
        flash(f"Error updating image: {str(e)}", "error")
        
    return redirect(url_for('admin.edit_image_page', unique_id=unique_id))

@admin_bp.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        flash("No image file provided", "error")
        return redirect(url_for('admin.dashboard'))
    
    file = request.files['image']
    
    if file.filename == '':
        flash("No image selected", "error")
        return redirect(url_for('admin.dashboard'))
        
    if file:
        image_data = file.read()
        mimetype = file.mimetype
        caption = request.form.get('caption')
        location_str = request.form.get('location')
        tags_str = request.form.get('tags')
        
        # Parse manually entered location
        location = None
        if location_str and location_str.strip():
            try:
                location = [float(x.strip()) for x in location_str.split(',')]
            except ValueError:
                flash("Invalid location format. Please use: lat, long", "error")
                return redirect(url_for('admin.dashboard'))
        
        # If no manual location provided, try to extract from EXIF
        if not location:
            gps_coords = get_gps_from_exif(image_data)
            if gps_coords:
                location = [gps_coords[0], gps_coords[1]]
                flash(f"GPS coordinates found in image: {gps_coords[0]:.6f}, {gps_coords[1]:.6f}", "success")
        
        tags = [t.strip() for t in tags_str.split(',')] if tags_str else None
        
        image_id = add_image(image_data=image_data, mimetype=mimetype, caption=caption, location=location, tags=tags)
        
        if image_id == "duplicate":
            flash("Image already exists.", "warning")
            return redirect(url_for('admin.dashboard'))
        elif image_id:
            flash("Image uploaded successfully!", "success")
            image = get_image_by_id(image_id)
            images = get_all_images()
            return render_template('admin/index.html', image=image, images=images)
        else:
            flash("Failed to upload image.", "error")
            return redirect(url_for('admin.dashboard')) 