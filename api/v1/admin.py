from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.data_layer.images import add_image, get_image_by_id, get_all_images, update_image_by_id, delete_image_by_id
from core.utils import get_gps_from_exif, process_image_for_storage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    images = get_all_images()
    return render_template('admin/index.html', images=images)

@admin_bp.route('/edit_image/<unique_id>')
def edit_image_page(unique_id):
    image = get_image_by_id(unique_id)
    if image:
        return render_template('admin/edit_image.html', image=image)
    flash("Image not found.", "error")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_image/<unique_id>', methods=['POST'])
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