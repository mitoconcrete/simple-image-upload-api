from io import BytesIO, StringIO

import cv2
import numpy as np
import svgwrite
from PIL import Image, ImageFile
from scour import scour


def _resize_image(image: ImageFile.ImageFile, width, height) -> Image:
    return image.resize((max(width, 100), max(height, 100)))


# 이미지 타입이 jpg, png 인지 확인하는 함수를 작성합니다.
def is_image_type_jpg_or_png(image: bytes) -> bool:
    try:
        image_type = Image.open(BytesIO(image)).format
        if image_type in ['JPEG', 'PNG']:
            return True
        return False
    except Exception:
        return False


def basic_image_preprocessor(image: bytes) -> bytes:
    """
    jpg, png 이미지를 받아서 가로 세로를 // 2로 리사이즈하고, 흑백 필터를 적용한 이미지를 반환합니다.
    """
    converted = Image.open(BytesIO(image))
    # 이미지 크기 조정
    resized = _resize_image(converted, converted.width // 2, converted.height // 2)

    # 흑백 필터 적용
    grayscale = resized.convert('L')

    # 이미지를 바이트로 변환
    output = BytesIO()
    grayscale.save(output, converted.format)
    return output.getvalue()


def _svg_optimizer(image: bytes) -> bytes:
    # SVG 바이트를 문자열로 디코딩
    svg_string = image.decode('utf-8')

    # scour 옵션 설정
    options = scour.parse_args([])

    # 최적화 옵션 설정
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

    # StringIO 객체 생성
    options = scour.sanitizeOptions(options)

    # 최적화된 SVG 바이트를 반환
    optimized_svg = scour.scourString(svg_string, options)
    optimized_svg_bytes = StringIO(optimized_svg).read().encode('utf-8')

    return optimized_svg_bytes


def _image_to_svg(image: bytes) -> bytes:
    """
    byte 형식의 이미지를 SVG로 변환합니다.
    가장 바깥 사각형을 제외하고 내부 경계만 검정색으로 채웁니다.
    경계가 미세하게 닫히지 않았을 경우, 이를 추론하여 경계를 닫습니다.
    윤곽선이 없으면 이미지를 직접 그려서 반환합니다.
    """
    # 바이트 데이터를 이미지로 변환
    img_array = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

    # 이미지 전처리
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # SVG 생성
    dwg = svgwrite.Drawing(size=(img.shape[1], img.shape[0]))

    # 윤곽선이 없으면 이미지의 각 픽셀을 그려서 SVG로 반환
    if not contours:
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                color = 'black' if img[y, x] == 255 else 'white'
                dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=color))
    else:
        # 가장 바깥 경계를 제외하기 위해, 가장 큰 경계 찾기
        max_contour = max(contours, key=cv2.contourArea)  # 가장 큰 경계 찾기

        for contour in contours:
            # 경계의 각 점을 추출하여 정수로 변환
            points = [(int(point[0][0]), int(point[0][1])) for point in contour]

            if points:
                # 경계가 미세하게 닫히지 않았으면 점들을 이어서 닫아줌
                if cv2.contourArea(contour) != cv2.contourArea(max_contour):  # 면적 기준으로 비교
                    # 경계가 닫히지 않았을 경우 점을 이어서 닫기
                    if points[0] != points[-1]:  # 첫 점과 마지막 점이 다르면 이어준다.
                        points.append(points[0])  # 첫 점을 마지막에 추가하여 경계를 닫음

                    # 내부 경계는 채우고, 가장 큰 경계는 제외
                    dwg.add(dwg.polygon(points=points, fill='black', stroke='black'))
                else:
                    # 가장 큰 경계는 제외하고 그리지 않음
                    continue

    # SVG를 바이트 형태로 반환
    output_bytes = StringIO()
    dwg.write(output_bytes)
    return output_bytes.getvalue().encode('utf-8')


def process_image_to_svg(image: bytes) -> bytes:
    """
    이미지를 받아서 처리합니다.
    """
    svg = _image_to_svg(image)
    optimized_svg = _svg_optimizer(svg)
    return optimized_svg


def get_image_size(image: bytes):
    return len(image)


def get_image_type(image: bytes) -> str:
    return Image.open(BytesIO(image)).format.lower()
