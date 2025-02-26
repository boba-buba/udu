import requests
import time
from human_handler import Human
from artwork_handler import ArtWork
import unicodedata

# umelci do narození:é před rokem 1935
#  díla vytvořená před rokem 1950



month_mapping = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}


def parse_date(data: dict[str, str], date: str, name: str, threshold_year) -> bool:
    if date == "None" or date == "0":
        return True

    date = date.replace(',', '').replace('c.', '').split(" ")
    index = 0
    if date[index] == '':
        return True

    if len(date) == 1:
        data[name] = f"+{date[0]}-00-00T00:00:00Z"
        data[name+'_precision'] = 9
    elif len(date) == 2:
        index = 1
        data[name] = f"+{date[1]}-{month_mapping[date[0]]}-00T00:00:00Z"
        data[name+'_precision'] = 10
    elif len(date) == 3:
        index = 2
        day = "{:02d}".format(int(date[1]))
        data[name] = f"+{date[2]}-{month_mapping[date[0]]}-{day}T00:00:00Z"
        data[name+'_precision'] = 11

    if len(date) > 0 and int(date[index]) > threshold_year:
        return False
    return True

def set_up_dict_for_artist(artist) -> dict[str, str]:
    artist_data = {}
    artist_data["artistName"] = unicodedata.normalize("NFC", artist.get('artistName', 'Unknown Name').rstrip().replace('\"', ''))
    retval = parse_date(artist_data,  artist.get('birthDayAsString', '0'), "birthDayAsString", 1934)
    if retval == False:
        return {}
    parse_date(artist_data, artist.get('deathDayAsString', '0'), "deathDayAsString", 9999)
    retval = parse_date(artist_data, str(artist.get('activeYearsStart', '0')), "activeYearsStart", 1950)
    if retval == False:
        return {}
    parse_date(artist_data, str(artist.get('activeYearsCompletion', '0')), "activeYearsCompletion", 9999)
    artist_data["image"] = artist.get('image', 'None')
    artist_data["gender"] = artist.get('sex', '')
    artist_data["id"] = artist.get('id', '')
    artist_data["url"] = artist.get('url', '')

    return artist_data




def parse_updated_artists(url: str, log_file):
    """
    Fetches and parses the JSON data from the given URL. If the JSON contains a `paginationToken`,
    it recursively fetches the next set of data and processes all artists.

    :param url: The initial URL to fetch the JSON data from.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP requests with status codes 4xx/5xx
        data = response.json()

        # Process artists in the current response
        if "data" in data and isinstance(data["data"], list):
            for artist in data["data"]:
                process_artist(artist, log_file)  # Placeholder for actual processing logic

        # Check for pagination token and fetch next set of data if available
        pagination_token = data.get("paginationToken")
        if pagination_token:
            log_file.write("paginationToken: " + pagination_token + "\n")
            print("paginationToken: " + pagination_token + "\n")
            next_url = f"https://www.wikiart.org/en/api/2/UpdatedArtists?paginationToken={pagination_token}"
            parse_updated_artists(next_url, log_file)  # Recursive call to handle the next page

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    # except ValueError as e:
    #     print(f"Error parsing JSON: {e}")


def set_up_dict_for_artwork(artwork, artist_qid: str) -> dict[str, str]:
    artwork_dict = {"artist_qid": artist_qid}
    artwork_dict["contentId"] = str(artwork.get("contentId"))
    title = artwork.get("title").replace("\"", "\'")
    if len(title) > 250:
        title = title[:250]
    if title == "" or title == "Untıtled" or title == "Untitled":
        artwork_dict["title"] = "Untitled " + artwork_dict["contentId"]
    else:
        artwork_dict["title"] = title
    completion_date = artwork.get("completitionYear", "None")
    if completion_date != "None":
        retval = parse_date(artwork_dict, str(completion_date), "completitionYear", 1949)
        if retval == False:
            return {}
    artwork_dict["width"] = str(artwork.get("width"))
    artwork_dict["height"] = str(artwork.get("height"))
    artwork_dict["image"] = str(artwork.get("image"))

    return artwork_dict


def process_artwork(artwork_json, qid: str, log_f):
    artwork_data = set_up_dict_for_artwork(artwork_json, qid)
    if len(artwork_data) == 0:
        return
    artwork = ArtWork()

    if artwork.Exists(artwork_data["title"], artwork_data["contentId"]):
        return
    log_f.write("\t"+ artwork_data["title"] +"\n")
    print("\t"+ artwork_data["title"]+"\n")
    artwork.InsertNew(artwork_data)


def process_artworks(artworks_url: str, qid: str, log_f):

    try:
        response = requests.get(artworks_url)
        response.raise_for_status()  # Raise an error for HTTP requests with status codes 4xx/5xx
        data = response.json()

        if isinstance(data, list):
            for work in data:
                process_artwork(work, qid, log_f)

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    # except ValueError as e:
    #     print(f"Error parsing JSON: {e}")



def process_artist(artist, log_file):
    """
    Processes an individual artist's data. Modify this function based on what needs to be done.

    :param artist: A dictionary representing the artist's data.
    """
    name = unicodedata.normalize("NFC", artist.get('artistName', 'Unknown Name').rstrip().replace('\"', ''))
    birthdate = artist.get('birthDayAsString', '0')
    log_file.write(name + " " + birthdate + "\n")
    print(name + " " + birthdate + "\n")
    artist_dict = set_up_dict_for_artist(artist)
    if len(artist_dict) == 0:
        return

    human = Human()
    qid = human.Exists(name)
    if qid == 'None':
        human.InsertNewHuman(artist_dict)
    else:
        human.AddToExisting(artist_dict, qid)

    while qid == -1 or qid == "None":
        time.sleep(2.5)
        qid = human.Exists(name)

    artworks_url = f'https://www.wikiart.org/en/App/Painting/PaintingsByArtist?artistUrl={artist_dict["url"]}&json=2'
    process_artworks(artworks_url, qid, log_file)




def main():
    with open("wikiart_log.txt", "a", encoding='utf-8') as f:
        initial_url = "https://www.wikiart.org/en/api/2/UpdatedArtists?paginationToken=eHD8xvjo%2fx0SU9TfXJpRXfVxqvf%2bVQiCdWYK81Dqt4E%3d"
        parse_updated_artists(initial_url, f)

main()
# # Example usage
# if __name__ == "__main__":
#     initial_url = "https://www.wikiart.org/en/api/2/UpdatedArtists"
#     parse_updated_artists(initial_url)


### TODO: Berthold  Woltze malformed text, do wikibase
### + jeste zkusit v query servic check for duplicities treba na examplu  Ebru (attributed)