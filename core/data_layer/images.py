import uuid
from sqlalchemy import create_engine, Column, Integer, String, BLOB, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from core.data_layer.sql import SqlManager
from core.utils import process_image_for_storage

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    unique_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    image_data = Column(BLOB, nullable=False)  # Full resolution image (300 DPI, up to 4K)
    thumbnail_data = Column(BLOB, nullable=False)  # Low resolution thumbnail (72 DPI)
    mimetype = Column(String, nullable=False)
    caption = Column(String)
    location = Column(JSON)  # Storing location as [lat, long]
    tags = Column(JSON)      # Storing tags as a list of strings

def create_image_table():
    sql_manager = SqlManager()
    engine = sql_manager.get_engine('default')
    if engine:
        Base.metadata.create_all(engine)

def add_image(image_data: bytes, mimetype: str, caption: str = None, location: list = None, tags: list = None):
    # Process the image to create optimized versions
    processed_image_data, thumbnail_data = process_image_for_storage(image_data)
    
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        # Check for duplicates using the processed image data
        if session.query(Image).filter_by(image_data=processed_image_data).first():
            session.close()
            return "duplicate"
            
        new_image = Image(
            image_data=processed_image_data,
            thumbnail_data=thumbnail_data,
            mimetype='image/jpeg',  # All processed images are JPEG
            caption=caption,
            location=location,
            tags=tags
        )
        session.add(new_image)
        session.commit()
        image_id = new_image.unique_id
        session.close()
        return image_id
    return None

def get_image_by_id(unique_id: str):
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        image = session.query(Image).filter_by(unique_id=unique_id).first()
        session.close()
        return image
    return None

def update_image_by_id(unique_id: str, caption: str = None, location: list = None, tags: list = None):
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        try:
            image = session.query(Image).filter_by(unique_id=unique_id).first()
            if image:
                image.caption = caption
                image.location = location
                image.tags = tags
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return False
        except Exception as e:
            session.rollback()
            session.close()
            raise e
    return False

def get_all_images():
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        images = session.query(Image).all()
        session.close()
        return images
    return []

def delete_image_by_id(unique_id: str):
    sql_manager = SqlManager()
    session = sql_manager.get_session('default')
    if session:
        try:
            image = session.query(Image).filter_by(unique_id=unique_id).first()
            if image:
                session.delete(image)
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return False
        except Exception as e:
            session.rollback()
            session.close()
            raise e
    return False 