import csv
from download_image import download_img

def spaces2underscore(text: str) -> str:
    return text.replace(" ", "_")

def parse_csv_with_images(csv_file_path: str, directory_path: str):

    with open(csv_file_path, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                local_name = spaces2underscore(row["itemLabel"])
                download_img(row["imageAddr"], directory_path, local_name)

#parse_csv_with_images("C:\\Users\\ncoro\\Downloads\\query.csv", "images_folder\\")