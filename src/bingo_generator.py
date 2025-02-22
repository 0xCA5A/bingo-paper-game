import os
import random
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

SUPPORTED_IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")


def create_bingo_cards(image_folder, output_pdf, card_dimension=(3, 3), num_cards=20):
    images = [
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS)
    ]

    print (f"[i] Found {len(images)} images in folder {image_folder} (supported image extensions: {", ".join(SUPPORTED_IMAGE_EXTENSIONS)})")

    if len(images) < card_dimension[0] * card_dimension[1]:
        raise ValueError("Not enough images to fill the bingo card")

    pdf = canvas.Canvas(output_pdf, pagesize=A4)
    pdf.setTitle("Bingo!")
    pdf.setAuthor("Bingo Generator")

    page_width, page_height = A4
    margin = 50
    cell_size = min((page_width - 2 * margin) / card_dimension[1], (page_height - 2 * margin) / card_dimension[0])

    grid_width = cell_size * card_dimension[1]
    grid_height = cell_size * card_dimension[0]
    vertical_offset = (page_height - grid_height) / 2
    horizontal_offset = (page_width - grid_width) / 2

    card_index = 0

    used_image_files = set()
    with tempfile.TemporaryDirectory() as temp_dir:

        for _ in range(num_cards):
            random.shuffle(images)
            selected_images = images[: card_dimension[0] * card_dimension[1]]

            card_index += 1

            print (f"[i] Generating bingo card {card_index} of {num_cards} with images: {', '.join([x.split('/')[-1] for x in selected_images])}")

            used_image_files.update(selected_images)

            image_index = 0
            for row in range(card_dimension[0]):
                for col in range(card_dimension[1]):
                    img_path = selected_images.pop(0)
                    img = Image.open(img_path)
                    img.thumbnail((cell_size, cell_size))

                    img_x = horizontal_offset + col * cell_size + (cell_size - img.size[0]) / 2
                    img_y = page_height - (vertical_offset + (row + 1) * cell_size) + (cell_size - img.size[1]) / 2

                    temp_file_path = os.path.join(temp_dir, f"temp_img_{card_index}_{image_index}.png")
                    img.save(temp_file_path)
                    pdf.drawImage(
                        temp_file_path,
                        img_x,
                        img_y,
                        width=img.size[0],
                        height=img.size[1],
                    )
                    image_index += 1

            # Draw grid
            for row in range(card_dimension[0] + 1):
                y = page_height - (vertical_offset + row * cell_size)
                pdf.line(horizontal_offset, y, horizontal_offset + grid_width, y)
            for col in range(card_dimension[1] + 1):
                x = horizontal_offset + col * cell_size
                pdf.line(x, page_height - vertical_offset, x, page_height - vertical_offset - grid_height)

            pdf.showPage()

        pdf.save()
        return used_image_files


def create_images(image_files, images_output_pdf):
    pdf = canvas.Canvas(images_output_pdf, pagesize=A4)
    pdf.setTitle("Bingo!")
    pdf.setAuthor("Bingo Generator")

    page_width, page_height = A4

    for img_path in image_files:
        img = Image.open(img_path)
        img_width, img_height = img.size

        scale = min(page_width / img_width, page_height / img_height)
        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        pdf.drawImage(img_path, x, y, width=new_width, height=new_height)
        pdf.showPage()

    pdf.save()
