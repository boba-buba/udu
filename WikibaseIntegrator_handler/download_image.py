import requests
import os

def download_img(img_url: str, directory_path: str, img_local_name: str):

    """ Based on img_url download file into directory_path and to file with name img_local_name """
    os.makedirs(directory_path, exist_ok=True)
    img_data = requests.get(img_url).content
    if (not directory_path.endswith("\\") or not directory_path.endswith("/")):
        directory_path = directory_path + "\\"
    # Extract file format from image url
    img_format = img_url.split('.')[-1]
    with open(directory_path + img_local_name + '.' + img_format, 'wb') as handler:
        handler.write(img_data)


#download_img("https://api.kramerius.mzk.cz/search/iiif/uuid:17f2d0c0-308a-11e9-a347-005056825209/full/1977,2770/0/default.jpg", "C:\Users\ncoro\source\repos\udu\imagesDownloader", "local_image")