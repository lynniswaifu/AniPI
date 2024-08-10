import re
import requests
from anipie.queries import ANIME_QUERY, MANGA_QUERY, ANIME_API_URL


class SearchByQuery:
    """A class that searches for an anime or manga by query."""

    def __init__(self, title, type="ANIME"):
        """Initialize the class."""
        self._title = title
        self._type = type.upper()
        if self._type not in ["ANIME", "MANGA"]:
            raise ValueError("Type must be either 'ANIME' or 'MANGA'")
        self._search()

    def __str__(self) -> str:
        """Return all the information of the anime as a string."""

        if self._type.upper() == "MANGA":
            manga_str = (
                f"Chapters: {self.get_chapters}\n" f"Volumes: {self.get_volumes}\n"
            )

        return (
            f"Title: {self.get_romanji_name}\n"
            f"English Title: {self.get_english_name}\n"
            f"Romaji Title: {self.get_romanji_name}\n"
            f"Type: {self._type}\n"
            f"Status: {self.get_status}\n"
            f"Description: {self.get_description}\n"
            f"Episodes: {self.get_episodes}\n"
            f"Cover Image URL: {self.get_cover_image_url}\n"
            f"Genres: {self.get_genres}\n"
            f"Site URL: {self.get_site_url}\n"
            f"Start Date: {self.get_start_date}\n"
            f"End Date: {self.get_end_date}\n"
            f"Average Score: {self.get_avg_score}\n"
            f"Season: {self.get_season}\n"
            f"Format: {self.get_format}\n"
            f"ID: {self.get_id}\n"
        ) + (manga_str if self._type.upper() == "MANGA" else "")

    def _search(self) -> None:
        """Perform the search for the anime."""
        variables = {
            "search": self._title,
            "type": self._type,
        }
        query = ANIME_QUERY if self._type == "ANIME" else MANGA_QUERY
        try:
            response = requests.post(
                ANIME_API_URL,
                json={"query": query, "variables": variables},
                timeout=1,
                verify=True,
            )
            self._response = response.json()
            self._media = self._response.get("data").get("Media")
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise SystemExit(errh)
        except requests.exceptions.ReadTimeout as errrt:
            raise TimeoutError(errrt)
        except requests.exceptions.ConnectionError as conerr:
            raise ConnectionError(conerr)
        except requests.exceptions.RequestException as errex:
            raise RuntimeError(errex)

    def get_raw_data(self) -> dict:
        """Returns the raw JSON data from the API."""
        return self._response

    @property
    def get_romanji_name(self) -> str:
        """Returns the romanji name of the anime."""
        return self._media.get("title").get("romaji")

    @property
    def get_english_name(self) -> str:
        """Returns the english name of the anime."""
        return self._media.get("title").get("english")

    @property
    def get_status(self) -> str:
        """Returns the status of the anime."""
        return self._media.get("status")

    @property
    def get_description(self) -> str:
        """Returns the description of the anime."""
        des = self._media.get("description")
        return re.sub(re.compile("<.*?>"), "", des)

    @property
    def get_episodes(self) -> int:
        """Returns the number of episodes of the anime."""
        return self._media.get("episodes")

    @property
    def get_cover_image_url(self) -> str:
        """Returns the cover image of the anime."""
        return self._media.get("coverImage").get("large")

    @property
    def get_genres(self) -> str:
        """Returns the genres of the anime."""
        return ", ".join(self._media.get("genres"))

    @property
    def get_site_url(self) -> str:
        """Returns the site url of the anime."""
        return self._media.get("siteUrl")

    def __handle_date(self, date) -> str:
        """Handle the date."""

        month = date.get("month")
        day = date.get("day")
        year = date.get("year")

        return (
            f"{month}/{day}/{year}"
            if month is not None and day is not None and year is not None
            else None
        )

    @property
    def get_start_date(self) -> str:
        """Returns the start date of the anime."""
        return self.__handle_date(self._media.get("startDate"))

    @property
    def get_end_date(self) -> str:
        """Returns the end date of the anime."""
        return self.__handle_date(self._media.get("endDate"))

    @property
    def get_avg_score(self) -> float:
        """Returns the average score of the anime."""
        average_score = self._media.get("averageScore")
        return (int(average_score) / 10) or None

    @property
    def get_season(self) -> str:
        """Returns the season of the anime."""
        return self._media.get("season")

    @property
    def get_format(self) -> str:
        """Returns the format of the anime."""
        return self._media.get("format")

    @property
    def get_id(self) -> int:
        """Returns the ID of the anime."""
        return self._media.get("id")

    @property
    def get_chapters(self) -> int:
        """Returns the number of chapters of the manga."""
        return self._media.get("chapters") or None

    @property
    def get_volumes(self) -> int:
        """Returns the number of volumes of the manga."""
        return self._media.get("volumes") or None
