from PIL import Image
from typing import Tuple, List

Color = Tuple[int, int, int]


color_list = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

def load_image(src: str) -> List[Color]:
    """
    Return a list of tiles
    The returned pixels do not have their alpha values!
    """
    image = Image.open(src)

    if image.width % 8 != 0:
        raise Exception("Invalid width")
    if image.height % 8 != 0:
        raise Exception("Invalid height")

    n_w = image.width // 8
    n_h = image.height // 8


    tiles = [extract_tile(image, x, y) for y in range(n_h) for x in range(n_w)]
    return tiles


def extract_tile(image: Image, x: int, y: int) -> List[Color]:
    """
    Extract the (x, y) tile and returns the flattened pixel list
    The returned pixels do not have their alpha values!
    """
    pixels_with_alpha = [image.getpixel((i, j)) for j in range(y*8, y*8+8) for i in range(x*8, x*8+8)]
    pixels = [(r, g, b) for (r, g, b, _) in pixels_with_alpha]
    return pixels


def pixels_to_id(l: List[Color]) -> List[int]:
    """
    Convert a list of pixels to a list of values ranging from 0 to 3
    using color_list.
    If a color isn't in color_list, defaults to 0
    """
    return [0 if c not in color_list else color_list.index(c) for c in l]
    

def id_to_bin(i: int) -> Tuple[str, str]:
    """
    Convert a value between 0 and 3 to its binary representation as a pair
    """
    if i == 0:
        return ("0", "0")
    elif i == 1:
        return ("0", "1")
    elif i == 2:
        return ("1", "0")
    elif i == 3:
        return ("1", "1")
    else:
        raise Exception("Invalid argument")


def bin_to_lines(l: List[Tuple[str, str]]) -> List[List[str]]:
    """
    Convert a list of binary values to its multiline representation
    (most significant bit is at bottom)
    """
    return [[x[1] for x in l], [x[0] for x in l]]


def line_to_hex(l: List[str]) -> str:
    """
    Convert a binary number to its hex representation
    """
    value = int("".join(l), 2)
    return "$%02X" % value



def build_matrix(l: List, w: int) -> List[List]:
    """
    Convert a list to a matrix of width w
    """
    if len(l) % w != 0:
        raise Exception("Can't convert list to matrix")
    h = len(l) // w
    return [[l[x + y*w] for x in range(w)] for y in range(h)]



def pretty_matrix_print(matrix: List[List]):
    for line in matrix:
        print("".join(line))


if __name__ == "__main__":
    src = "test.png"
    out = "test.s"

    tiles = load_image(src)
    hex_str = []
    for tile in tiles: 
        l = pixels_to_id(tile)
        l2 = [id_to_bin(i) for i in l]
        bin_matrix = build_matrix(l2, 8)
        vertical_matrix = [line for pairs in bin_matrix for line in bin_to_lines(pairs)]
        hex_lines = [line_to_hex(line) for line in vertical_matrix]
        hex_str.append(".DB " + ",".join(hex_lines) + "\n")
    
    with open(out, "w") as f:
        for hex_s in hex_str:
            f.write(hex_s)
            print(hex_s.strip())


