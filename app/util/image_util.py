from io import BytesIO, StringIO

import cv2
import numpy as np
import svgwrite
from PIL import Image, ImageFile
from scour import scour


def resize_image(image: ImageFile.ImageFile, width: int, height: int) -> Image:
    return image.resize((max(width, 100), max(height, 100)))


def is_jpg_or_png(image_data: bytes) -> bool:
    try:
        image_format = Image.open(BytesIO(image_data)).format
        return image_format in ['JPEG', 'PNG']
    except Exception:
        return False


def get_image_size(image_data: bytes) -> int:
    return len(image_data)


def get_image_format(image_data: bytes) -> str:
    return Image.open(BytesIO(image_data)).format.lower()


def convert_image_to_svg(image_data: bytes) -> bytes:
    img_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dwg = svgwrite.Drawing(size=(img.shape[1], img.shape[0]))

    if not contours:
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                color = 'black' if img[y, x] == 255 else 'white'
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=color))
    else:
        max_contour = max(contours, key=cv2.contourArea)
        for contour in contours:
            points = [(int(point[0][0]), int(point[0][1])) for point in contour]
            if points:
                if cv2.contourArea(contour) != cv2.contourArea(max_contour):
                    if points[0] != points[-1]:
                        points.append(points[0])
                    dwg.add(dwg.polygon(points=points, fill='black', stroke='black'))
                else:
                    continue

    output_bytes = StringIO()
    dwg.write(output_bytes)
    return output_bytes.getvalue().encode('utf-8')


def optimize_svg(svg_data: bytes) -> bytes:
    svg_string = svg_data.decode('utf-8')
    options = scour.parse_args([])
    options.enable_viewboxing = True
    options.enable_id_stripping = True
    options.enable_comment_stripping = True
    options.shorten_ids = True
    options.indent_type = 'none'
    options.remove_metadata = True
    options.strip_xml_prolog = True
    options.remove_descriptive_elements = True
    options.group_create = True
    options.group_collapse = True
    options = scour.sanitizeOptions(options)
    optimized_svg = scour.scourString(svg_string, options)
    return StringIO(optimized_svg).read().encode('utf-8')


def preprocess_image(image_data: bytes) -> bytes:
    image = Image.open(BytesIO(image_data))
    resized_image = resize_image(image, image.width // 2, image.height // 2)
    grayscale_image = resized_image.convert('L')
    output = BytesIO()
    grayscale_image.save(output, image.format)
    return output.getvalue()


def process_image(image_data: bytes) -> bytes:
    svg_data = convert_image_to_svg(image_data)
    optimized_svg_data = optimize_svg(svg_data)
    return optimized_svg_data
