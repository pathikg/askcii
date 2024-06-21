import os
import argparse
import requests
from io import BytesIO
from urllib.parse import urlparse

import torch
from PIL import Image
from diffusers import StableDiffusionPipeline

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width, new_height):
    return image.resize((new_width, new_height))


def to_grayscale(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()
    return "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])


def image_to_ascii(image, new_width, new_height):
    image = resize_image(image, new_width, new_height)
    grayscale_image = to_grayscale(image)
    ascii_str = pixels_to_ascii(grayscale_image)

    img_width = grayscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i : i + img_width] + "\n"

    return ascii_img


def generate_image_from_prompt(prompt, model_id, steps):
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    image = pipe(prompt, num_inference_steps=steps).images[0]
    return image


def generate_default_ascii():
    default_image = Image.new("RGB", (100, 100), color="white")
    return image_to_ascii(default_image)


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def load_image_from_url_or_path(url_or_path):
    try:
        if is_valid_url(url_or_path):
            response = requests.get(url_or_path)
            return Image.open(BytesIO(response.content))
        elif os.path.isfile(url_or_path):
            return Image.open(url_or_path)
        else:
            raise ValueError("Not a valid URL or file path")
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def parse_arguments():
    parser = argparse.ArgumentParser(description="ASKCII: ASCII Art Generator")
    parser.add_argument("command", choices=["create"], help="Command to execute")
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        nargs="?",
        help="URL or path to the image file",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        required=False,
        help="Prompt to generate the ASCII art",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        help="Width to resize the image (default: original width)",
    )
    parser.add_argument(
        "-h",
        "--height",
        type=int,
        help="Height to resize the image (default: original height)",
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=int,
        default=20,
        help="Number of inference steps for Stable Diffusion (default: 50)",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="stabilityai/stable-diffusion-2-1-base",
        help="Diffusion model to use (default: stable-diffusion-2-1-base)",
    )

    args = parser.parse_args()
    return args


def main(args):
    if args.command == "create":
        if args.url:
            image = load_image_from_url_or_path(args.url_or_path)
            if image:
                print(f"Creating ASCII art from: {args.url_or_path}")
                if args.width:
                    ascii_art = image_to_ascii(image, args.width, args.height)
                else:
                    ascii_art = image_to_ascii(image, image.width, image.height)
            else:
                print("Using default image as fallback.")
                ascii_art = generate_default_ascii()
        elif args.prompt:
            print("Loading Model...")
            image = generate_image_from_prompt(args.prompt, args.model, args.steps)
            ascii_art = image_to_ascii(image, args.width)
        else:
            print("Using default image.")
            ascii_art = generate_default_ascii()
    else:
        print("Invalid command. Use 'create' to generate ASCII art.")
        return

    print(ascii_art)

    # Save to file
    with open("ascii_output.txt", "w") as f:
        f.write(ascii_art)
    print("ASCII art saved to ascii_output.txt")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
