from PIL import Image, ExifTags
from PIL.ExifTags import GPSTAGS
import io

def get_gps_from_exif(image_data):
    """
    Extract GPS coordinates from EXIF data in image bytes.
    Returns tuple (latitude, longitude) or None if no GPS data found.
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Get EXIF data
        exif = image._getexif()
        if not exif:
            return None
            
        # Find GPS info in EXIF
        gps_info = None
        for tag, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                gps_info = value
                break
                
        if not gps_info:
            return None
            
        # Extract GPS coordinates
        gps_data = {}
        for key, value in gps_info.items():
            tag_name = GPSTAGS.get(key, key)
            gps_data[tag_name] = value
            
        # Convert GPS coordinates to decimal degrees
        lat = _convert_to_degrees(gps_data.get('GPSLatitude'))
        lon = _convert_to_degrees(gps_data.get('GPSLongitude'))
        
        if lat is None or lon is None:
            return None
            
        # Apply direction (N/S for latitude, E/W for longitude)
        if gps_data.get('GPSLatitudeRef') == 'S':
            lat = -lat
        if gps_data.get('GPSLongitudeRef') == 'W':
            lon = -lon
            
        return (lat, lon)
        
    except Exception:
        # If any error occurs, return None
        return None

def _convert_to_degrees(value):
    """
    Convert GPS coordinates from degrees/minutes/seconds to decimal degrees.
    """
    if not value:
        return None
        
    try:
        d, m, s = value
        return float(d) + float(m)/60 + float(s)/3600
    except (ValueError, TypeError, ZeroDivisionError):
        return None

def process_image_for_storage(image_data, target_dpi=300, thumbnail_dpi=72, max_dimension=3840):
    """
    Process image data to create optimized versions for storage.
    
    Args:
        image_data (bytes): Original image data
        target_dpi (int): Target DPI for main image (default: 300 - good for Retina displays)
        thumbnail_dpi (int): Target DPI for thumbnail (default: 72 - web standard)
        max_dimension (int): Maximum width/height for main image (default: 3840 for 4K support)
    
    Returns:
        tuple: (processed_image_data, thumbnail_data) both as bytes
    """
    try:
        # Open the original image
        original_image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary (handles RGBA, P, etc.)
        if original_image.mode not in ('RGB', 'L'):
            original_image = original_image.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = original_image.size
        
        # Calculate new dimensions for main image (300 DPI equivalent)
        # Scale down if image is too large
        if max(original_width, original_height) > max_dimension:
            if original_width > original_height:
                new_width = max_dimension
                new_height = int((original_height * max_dimension) / original_width)
            else:
                new_height = max_dimension
                new_width = int((original_width * max_dimension) / original_height)
        else:
            new_width, new_height = original_width, original_height
        
        # Create main image (300 DPI equivalent)
        main_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate thumbnail dimensions (72 DPI equivalent - roughly 1/4 of main image)
        thumb_scale = thumbnail_dpi / target_dpi  # 72/300 = 0.24
        thumb_width = int(new_width * thumb_scale)
        thumb_height = int(new_height * thumb_scale)
        
        # Ensure thumbnail isn't too small
        min_thumb_size = 200  # Increased minimum for better quality
        if max(thumb_width, thumb_height) < min_thumb_size:
            if thumb_width > thumb_height:
                thumb_width = min_thumb_size
                thumb_height = int((thumb_height * min_thumb_size) / thumb_width)
            else:
                thumb_height = min_thumb_size
                thumb_width = int((thumb_width * min_thumb_size) / thumb_height)
        
        # Create thumbnail
        thumbnail = original_image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        
        # Save main image to bytes with higher quality
        main_buffer = io.BytesIO()
        main_image.save(main_buffer, format='JPEG', quality=92, optimize=True)
        main_data = main_buffer.getvalue()
        
        # Save thumbnail to bytes
        thumb_buffer = io.BytesIO()
        thumbnail.save(thumb_buffer, format='JPEG', quality=80, optimize=True)
        thumb_data = thumb_buffer.getvalue()
        
        return main_data, thumb_data
        
    except Exception as e:
        # If processing fails, return original data for both
        return image_data, image_data 