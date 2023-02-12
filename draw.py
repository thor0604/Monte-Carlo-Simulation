#! /usr/bin/env python3
"""generate PPM images and transform them into GIF"""

import sys
import subprocess
import approximate_pi
import integers

def take_argument():
    """take 3 arguments from the command line"""
    if len(sys.argv) != 4:
        raise IndexError("Please add in size of image as second argument, "
        "number of repeats as third argument "
        "and decimal as fourth argument!")
    try:
        size, repeat, decimal = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    except ValueError:
        raise ValueError("size, repeat and decimal must be integer!") from None

    if size < 100:
        raise ValueError("size must be larger than or equal to 100")
    if repeat <= 100:
        raise ValueError("repeat must be larger than 100")
    if decimal < 1 or decimal > 5:
        raise ValueError("decimal must be a value between 1 and 5")

    return size, repeat, decimal

def generate_ppm_table_white(size):
    """generate a ppm table with white background"""
    return [(1,1,1)]*(size)*(size)

def index_to_change(point, size):
    """return the index to change in ppm_table given a certain point"""
    new_x = int((point[0] + 1) * size/2)
    new_y = int((point[1] - 1) * size/2 * (-1))
    return new_x + new_y * (size)

def one_tenth_of_value(current, total, count):
    """return True if the current value is one tenth of the total number"""
    return current == int(count*total/10)

def calculate_pi(count_in_circle, total):
    """
    return the approximated value of pi given the number of points
    that fall in circle and the total number of points
    """
    return 4 * count_in_circle / total

def convert_float_to_string(value, decimal):
    """convert a float value to string with a given decimal"""
    str_value = str(value)
    end = decimal + 2
    if len(str_value) < decimal + 2:
        to_append = decimal + 2 - len(str_value)
        for _ in range(to_append):
            str_value += '0'
    return str_value[0:end]

def calculate_scale_for_integer(size):
    """
    calculate the scale to exlarge the integer with regards to
    the size of template and the size of image"""
    if size < 300:
        y_domaine = int((size)*1/10)
    else:
        y_domaine = int((size)*1/13)
    scale = int(y_domaine/9)
    return scale

def calculate_start_index_with_ratio(size):
    """
    calculate the first index to insert the value of pi at the
    center of image with the ratio of 5:2:5 for x and 6:1:6 for y
    """
    start_x = int((size)*5/12)
    start_y = int((size)*6/13)
    return start_x + start_y*(size)

def scale_table(table, scale):
    """return a scaled up table"""
    scaled_table_x = []
    height = 9
    width = 3
    for pixel in table:
        for _ in range(scale):
            scaled_table_x.append(pixel)
    scaled_table = []
    count = 0
    for _ in range(height):
        for _ in range(scale):
            for index in range(count, count+width*scale):
                scaled_table.append(scaled_table_x[index])
        count += width*scale
    return scaled_table


def save_pixel_in_set(chartable, chartable_width, size, start_index, pi_pixel_set):
    """save the pixels to show the value of pi in a set"""
    chartable_height = int(len(chartable) / chartable_width)
    count_pixel = 0
    for _ in range(chartable_height):
        for index in range(start_index, start_index + chartable_width):
            pixel = chartable[count_pixel]
            if pixel == 1:
                pi_pixel_set.add(index)
            count_pixel += 1
        start_index += size


def calculate_pixel_pi(decimal, pi_value, size):
    """
    calculate the pixels to print the value of pi and return the coordinates
    in the form of set
    """
    str_pi = convert_float_to_string(pi_value, decimal)
    scale = calculate_scale_for_integer(size)
    width = 3 * scale
    start_index = calculate_start_index_with_ratio(size)
    pi_pixel_set = set()
    for character in str_pi:
        table_char = scale_table(integers.DICT_INTEGER[character], scale)
        save_pixel_in_set(table_char, width, size, start_index, pi_pixel_set)
        start_index += int(width * 1.4)
    return pi_pixel_set


def generate_filename(count, pi_value, decimal):
    """generate filename for ppm images"""
    pi_str = f"{pi_value:.{decimal}f}".replace('.','-')
    return f"img{count}_" + pi_str + ".ppm"


def write_ppm_file(count, pi_value, decimal, ppm_table, pixel_to_color):
    """output a ppm image file given a ppm_table"""
    size = int(len(ppm_table)**(1/2))
    ppm_file = generate_filename(count, pi_value, decimal)
    with open (ppm_file, 'w', encoding='utf-8') as file:
        file.write(f"P6 {size} {size} 1\n")
    with open (ppm_file, 'ab') as file:
        for index in range(size**2):
            if index in pixel_to_color:
                file.write(b"\x00\x00\x00")
            else:
                pixel = ppm_table[index]
                if pixel == (1,0,0):
                    file.write(b"\x01\x00\x00")
                elif pixel == (0,0,1):
                    file.write(b"\x00\x00\x01")
                else:
                    file.write(b"\x01\x01\x01")


def generate_ppm_file(size, repeat, decimal):
    """calculate pi and output ppm image files"""
    color_in_circle, color_out_circle = (1,0,0), (0,0,1)
    count_in_circle = 0
    count_save_file = 1
    ppm_table = generate_ppm_table_white(size)
    for i in range(1, repeat+1):
        rpoint = approximate_pi.generate_random_point()
        index = index_to_change(rpoint, size)
        if approximate_pi.in_circle(rpoint):
            count_in_circle += 1
            ppm_table[index] = color_in_circle
        else:
            ppm_table[index] = color_out_circle
        # create a ppm file for every n/10
        if one_tenth_of_value(i, count_save_file, repeat):
            pi_value = calculate_pi(count_in_circle, i)
            pixel_to_color = calculate_pixel_pi(decimal, pi_value, size)
            write_ppm_file(count_save_file-1, pi_value, decimal, ppm_table, pixel_to_color)
            count_save_file += 1

def convert_ppm_to_gif():
    """convert ppm images to gif"""
    input_files = "*.ppm"
    output_file = "pi.gif"
    subprocess.run("convert -delay 100 -loop 0 " + input_files + " " +
        output_file, shell=True, check=True)

def main():
    """programme principale de génération d'images"""
    size, repeat, decimal = take_argument()
    generate_ppm_file(size, repeat, decimal)
    convert_ppm_to_gif()

if __name__ == '__main__':
    main()
