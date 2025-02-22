from src import bingo_generator
import os

if __name__ == "__main__":
    image_root = os.getenv("IMAGE_ROOT", "/home/sam/Documents/bingo2/figuren")
    output_root = os.getenv("OUTPUT_ROOT", "../out")
    number_of_cards = os.getenv("NUMBER_OF_CARDS", 20)

    bingo_cards_output_pdf = f"{output_root}/result.pdf"
    images_output_pdf = f"{output_root}/images.pdf"

    used_image_files = bingo_generator.create_bingo_cards(image_root, bingo_cards_output_pdf, num_cards=int(number_of_cards))
    bingo_generator.create_images(used_image_files, images_output_pdf)
