"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image.

    Parameters
    ----------
    file_location: str
        The location of the image file to decode. This defaults to the provided
        encoded image in the images folder.
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    x_size, y_size = encoded_image.size

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if red_channel.getpixel((i, j)) % 2 == 0:
                pixels[i, j] = (255,255,255)

    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Write text to an RGB image. Automatically line wraps.

    Parameters
    ----------
    text_to_write: str
        The text to write to the image.
    image_size: (int, int)
        The size of the resulting text image.
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed2.jpg"):
    """Encode a text message into an image.

    Parameters
    ----------
    text_to_encode: str
        The text to encode into the template image.
    template_image: str
        The image to use for encoding. An image is provided by default.
    """
    unencoded_image = Image.open(template_image)
    red_channel, green_channel, blue_channel = unencoded_image.split()
    x_size, y_size = unencoded_image.size

    encoded_image = Image.new("RGB", unencoded_image.size)
    pixels = encoded_image.load()
    data = write_text(text_to_encode, (x_size, y_size))

    for i in range(x_size):
        for j in range(y_size):
            red_val = red_channel.getpixel((i, j))
            green_val = green_channel.getpixel((i, j))
            blue_val = blue_channel.getpixel((i, j))

            if (data.getpixel((i, j)) == (0,0,0)) != (red_val % 2 == 0):
                red_val += 1
                if red_val > 255:
                    red_val -= 2

            pixels[i, j] = (red_val, green_val, blue_val)

    encoded_image.save("images/encoded_image.png")


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image("images/encoded_image.png")

    print("Encoding the image...")
    text = "An infinite number of mathematicians walk into a bar. The first mathematician orders a beer. The second orders half a beer. I don't serve half-beers the bartender replies. Excuse me? Asks mathematician 2. What kind of bar serves half-beers? The bartender remarks. That's ridiculous. Oh c'mon says mathematician 1 do you know how hard it is to collect an infinite number of us? Just play along There are strict laws on how I can serve drinks. I couldn't serve you half a beer even if I wanted to. But that's not a problem mathematician 3 chimes in at the end of the joke you serve us a whole number of beers. You see, when you take the sum of a continuously halving function- I know how limits work interjects the bartender. Oh, alright then. I didn't want to assume a bartender would be familiar with such advanced mathematics Are you kidding me? The bartender replies, you learn limits 9th grade! What kind of mathematician thinks limits are advanced mathematics? HE'S ON TO US mathematician 1 screeches. Simultaneously, every mathematician opens their mouth and out pours a cloud of multicolored mosquitoes. Each mathematician is bellowing insects of a different shade. The mosquitoes form into a singular, polychromatic swarm. FOOLS it booms in unison, I WILL INFECT EVERY BEING ON THIS PATHETIC PLANET WITH MALARIA The bartender stands fearless against the technicolor hoard. He interrupts, thinking fast, if you do that, politicians will use the catastrophe as an excuse to implement free healthcare. Think of how much that will hurt the taxpayers! The mosquitoes fall silent for a brief moment. My God, you're right. We didn't think about the economy! Very well, we will not attack this dimension. FOR THE TAXPAYERS! and with that, they vanish. A nearby barfly stumbles over to the bartender. How'd you know that would work? It's simple really the bartender says. I saw that the vectors formed a gradient and therefore must be conservative. - u/pokeloly on reddit"

    encode_image(text)
