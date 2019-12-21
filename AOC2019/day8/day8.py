import numpy as np


def build_image(pixels, x, y):
    pixel_list = [int(v) for v in pixels]
    array = np.array(pixel_list)
    array = array.reshape((-1, y, x), order='C')
    return array


def find_densest_layer(image):
    zeros = image == 0
    layer_zeros = np.sum(zeros, (1, 2))
    return np.argmin(layer_zeros)


def calc_checksum(image, layer):
    ones = image[layer, :, :] == 1
    twos = image[layer, :, :] == 2
    n_ones = np.sum(ones)
    n_twos = np.sum(twos)
    return n_ones * n_twos


def flatten(image):
    transparent = 2
    render = np.full_like(image[0, :, :], transparent)
    for layer in image:
        roi = render == transparent
        render[roi] = layer[roi]
    return render


def image_to_string(image):
    lines = []
    pixels = {0: ' ', 1: '#'}
    for line in image:
        lines.append(''.join([pixels[v] for v in line]))
    return '\n'.join(lines)


def main():
    with open('input.txt') as f:
        pixels = f.read()
    image = build_image(pixels, x=25, y=6)
    layer = find_densest_layer(image)
    print('Layer with fewest zeros is ', layer)
    checksum = calc_checksum(image, layer)
    print('Checksum is ', checksum)

    render = flatten(image)
    print('Message is:')
    print(image_to_string(render))


if __name__ == '__main__':
    main()
