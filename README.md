# askcii

<img width="674" alt="Screenshot 2024-06-22 at 1 54 04 AM" src="https://github.com/pathikg/askcii/assets/55437218/54a62ac4-0f26-4246-876b-08a50e986f14">

create and convert image to ascii in a single prompt

# Demo

Here's Colab Notebook for the same:  
https://colab.research.google.com/drive/1jh3aDOkxTV5mGiDtUWSFTAJTfUI6VTMh?usp=sharing

## Features

- Generate images from text prompts using Stable Diffusion 2
- Convert existing images (from local files or URLs) to ASCII art
- Save both the generated image and ASCII art output

## Requirements

- Python 3.7+
- CUDA-capable GPU (for Stable Diffusion image generation)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/askcii.git
   cd askcii
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

The basic syntax for using ASKCII is:

```
usage: askcii.py [-h] [-u [URL]] [-p PROMPT] [-wt WIDTH] [-ht HEIGHT] [-s STEPS] [-m MODEL] {create}

ASKCII: ASCII Art Generator

positional arguments:
  {create}              Command to execute

options:
  -h, --help            show this help message and exit
  -u [URL], --url [URL]
                        URL or path to the image file
  -p PROMPT, --prompt PROMPT
                        Prompt to generate the ASCII art
  -wt WIDTH, --width WIDTH
                        Width to resize the image (default: original width)
  -ht HEIGHT, --height HEIGHT
                        Height to resize the image (default: original height)
  -s STEPS, --steps STEPS
                        Number of inference steps for Stable Diffusion (default: 50)
  -m MODEL, --model MODEL
                        Diffusion model to use (default: stable-diffusion-2-1-base)
```

### Examples

1. Generate ASCII art from a text prompt:
   ```
   python askcii.py create -p "{prompt}" -s {steps} -wt {width} -ht {height} --model {model_id}

   ```

2. Generate ASCII art from a local image:
   ```
   python askcii.py create -u path/to/your/image.jpg
   ```

3. Generate ASCII art from an online image:
   ```
   python askcii.py create -u https://example.com/image.jpg
   ```

## Output

For each run, ASKCII will:
1. Print the ASCII art to the console
2. Save the ASCII art to a file named `ascii_output.txt`

## Note on First Run

The first time you run ASKCII with a text prompt, it will download the Stable Diffusion 2 model, which is several gigabytes in size. This may take some time depending on your internet connection.

## Limitations

- The script is currently set up to use CUDA for GPU acceleration. If you're running on a CPU or a different GPU architecture, you may need to modify the `generate_image_from_prompt()` function.
- Image generation can be computationally intensive and may take some time, depending on your hardware.

## Contributing

Contributions to ASKCII are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [Stable Diffusion](https://github.com/CompVis/stable-diffusion) model via the [🤗 Diffusers](https://github.com/huggingface/diffusers) library.
- ASCII art conversion inspired by various open-source projects in the community.
