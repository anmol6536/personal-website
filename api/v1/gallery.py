from flask import Blueprint, render_template, jsonify, Response
from core.data_layer.sql import SqlManager
from core.data_layer.images import Image, get_image_by_id

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@gallery_bp.route('/image/<unique_id>')
def serve_image(unique_id):
    """Serve full resolution image (300 DPI, up to 4K resolution)"""
    image = get_image_by_id(unique_id)
    if image:
        return Response(image.image_data, mimetype=image.mimetype)
    return "Image not found", 404

@gallery_bp.route('/thumbnail/<unique_id>')
def serve_thumbnail(unique_id):
    """Serve low resolution thumbnail (72 DPI, web-optimized)"""
    image = get_image_by_id(unique_id)
    if image:
        return Response(image.thumbnail_data, mimetype=image.mimetype)
    return "Thumbnail not found", 404

@gallery_bp.route('/')
def index():
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        images = session.query(Image).all()
        session.close()
    else:
        images = []
    return render_template('gallery/index.html', photos=images)

@gallery_bp.route('/<int:image_id>')
def get_image(image_id):
    """Serve full resolution image by ID (300 DPI, up to 4K resolution)"""
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        image = session.query(Image).filter_by(id=image_id).first()
        session.close()
        if image:
            return Response(image.image_data, mimetype=image.mimetype)
    return "Image not found", 404

@gallery_bp.route('/thumbnail/<int:image_id>')
def get_thumbnail(image_id):
    """Serve low resolution thumbnail by ID (72 DPI, web-optimized)"""
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        image = session.query(Image).filter_by(id=image_id).first()
        session.close()
        if image:
            return Response(image.thumbnail_data, mimetype=image.mimetype)
    return "Thumbnail not found", 404

@gallery_bp.route('/modal/<int:image_id>')
def gallery_modal(image_id):
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        photo = session.query(Image).filter_by(id=image_id).first()
        session.close()
    else:
        photo = None
    return render_template('gallery/modal.html', photo=photo) 