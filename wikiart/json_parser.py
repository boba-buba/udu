import requests

def parse_updated_artists(url):
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
                process_artist(artist)  # Placeholder for actual processing logic

        # Check for pagination token and fetch next set of data if available
        pagination_token = data.get("paginationToken")
        if pagination_token:
            next_url = f"https://www.wikiart.org/en/api/2/UpdatedArtists?paginationToken={pagination_token}"
            parse_updated_artists(next_url)  # Recursive call to handle the next page

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")

def process_artist(artist):
    """
    Processes an individual artist's data. Modify this function based on what needs to be done.

    :param artist: A dictionary representing the artist's data.
    """
    print(f"Processing artist: {artist.get('artistName', 'Unknown Name')}")
    # Add more processing logic as needed, e.g., saving data to a database or file

# Example usage
if __name__ == "__main__":
    initial_url = "https://www.wikiart.org/en/api/2/UpdatedArtists"
    parse_updated_artists(initial_url)
