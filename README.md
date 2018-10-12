# mtg-image-downloader
This python program downloads the png images of all Magic: the Gathering cards from Scryfall. Very convenient to help with image recognition.

**WARNING**: This will take up aprox 90 GB of data so be sure that you have enough space. The script will take a VERY long time to execute. Between an hour to 8 hours depending on download speed and number of threads used.

## Downloading Info

### Format
It will download png images and save them in the following format:

`$output_dest/mtg_images/$card_name[$set]-[$card_num]/original.png`  

As is, this script will not work with Windows due to how paths work. If interest is there, adjustments can be made (see future).

It should be noted that because of incompatibilities with cards with multiple 'cards' on them (flip cards and split cards) and standard file naming conventions that any '//' in names are changed to '--'. As each side of a transform card is a completely different image, they will be located their own folder under each card face's name.

### What is downloaded
Any physical card including special promotionals, funny cards, Archenemy, Planechase, token, and any other physical card that is in Scryfall's database will be pulled. Digital only cards such as Avatars or cards from Tempest Remastered will be ignored.

## Environment
The following external libraries are used and should be installed.
* requests
* ratelimit

Just a simple `pip install -r requirements.txt` should get you what you need. I would recommend using a virtual environment as I doubt this program will be used by many and because of that won't be maintained (see future below).

This program was designed with Python 3.7 but I imagine it would work for all versions > 3.2.

You will also need the JSON database of cards located at https://scryfall.com/docs/api/bulk-data.

### Configs
The program will read from a config.ini for the configuration. If there is not one found, it will read from the example.ini. This is not recommended as it will create a folder in the current working directory with all the images in it which can be a pain to move. Also, the default is to not use threading which will take a very long time. 

#### Attributes in config.ini
* json_source: Put here the location of the Bulk Data JSON downloaded from Scryfall.
* output_dest: Where the folders will be created to put the pictures. Make sure there is no trailing '/' at the end
* threaded: Whether the download will be threaded or not. HIGHLY recommended. Make sure it is either True or False. Default is False for compatibility.
* max_threads: Number of threads to use. Try not to put more than your computer can do. If you are unsure try the number of cores you have * 2 - 1. Please note that due to Scryfall having a rate limit, the effectiveness of threads decrease sharply after about 10.

## Other Stuff

### Future
I do not expect to put much more work into this as I made it for my own purpose of downloading all the images. However, if there is enough interest, I will dedicate myself more to this and add additional features such as functionality under Windows filesystems, download specific sets of images, and download digital only images. I personally have no use for said features and this was made for my personal benefit so they were not implemented. If you think you will use this, please let me know. I would like to know that I made something that was beneficial to others. Pull Requests are certainly welcome, but I'm not holding my breath. Any bugs or troubles please let me know.

### Copyright Stuff and Legalities
All images are copyright Wizards of the Coast (and/or their artist, for very old sets). This script is in NO WAY affliated with Wizards of the Coast OR Scryfall. Please review Scryfall's image guidelines located at https://scryfall.com/docs/api/images if you intend to use the images in a public way. This script may be used in any way as long as the rights of the images are properly attributed and Scryfall's image guidelines are followed.
