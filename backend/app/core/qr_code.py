import io
import json
from typing import Dict, Any
import qrcode
from PIL import Image
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import pyzbar with better error handling
try:
    import pyzbar
    from pyzbar.pyzbar import decode as pyzbar_decode
    logger.info(f"Successfully imported pyzbar from {pyzbar.__file__}")
except ImportError as e:
    logger.error(f"Failed to import pyzbar: {e}")
    logger.error(f"Python path: {sys.path}")
    pyzbar_decode = None


def generate_qr_code(data: Dict[str, Any]) -> bytes:
    """
    Generate a QR code image (PNG bytes) from a dictionary.
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(data))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        return b'dummy_qr_code'


def decode_qr_code(image_bytes: bytes) -> Dict[str, Any]:
    """
    Temporarily disabled QR code decoding.
    Returns dummy data.
    """
    logger.warning("QR code decoding is temporarily disabled")
    return {
        "id": 1,
        "name": "Dummy Asset",
        "serial_number": "DUMMY-001",
        "category": "Dummy Category"
    }


def generate_qr_code(data: Dict[str, Any]) -> bytes:
    """
    Generate a QR code image (PNG bytes) from a dictionary.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def decode_qr_code(image_bytes: bytes) -> Dict[str, Any]:
    """
    Decode a QR code image (PNG bytes) and return the data as a dictionary.
    Requires pyzbar and pillow.
    """
    if not pyzbar_decode:
        error_msg = "pyzbar is required for QR code decoding. Please ensure it is installed correctly."
        logger.error(error_msg)
        raise ImportError(error_msg)
    
    try:
        img = Image.open(io.BytesIO(image_bytes))
        decoded = pyzbar_decode(img)
        if not decoded:
            error_msg = "No QR code found in image."
            logger.error(error_msg)
            raise ValueError(error_msg)
        data = decoded[0].data.decode("utf-8")
        return json.loads(data)
    except Exception as e:
        error_msg = f"Error decoding QR code: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg) 