import requests
import re

class BookLookup:

    @staticmethod
    def openlibrary(isbn):
        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            r = requests.get(url, timeout=5)

            if r.status_code != 200:
                return None
            
            data = r.json()

            book = {
                "title": data.get("title", ""),
                "published": None,
                "edition": "",
                "author": "",
                "summary": "",
                "language": "",
                "cover": ","
            }

            if data.get("publish_date"):
                match = re.search(
                    r"\b(18|19|20)\d{2}\b",
                    data["publish_date"]
                )
                
                if match:
                    book["published"] = int(match.group())

            if "publishers" in data:
                if len(data["publishers"]) > 0:
                    book["edition"] = data["publishers"][0]

            if "authors" in data:

                author_key = data["authors"][0]["key"]

                author = requests.get(
                    f"https://openlibrary.org{author_key}.json",
                    timeout=5
                )

                if author.status_code == 200:
                    book["author"] = author.json().get("name", "")

            if data.get("works"):
                work_key = data["works"][0]["key"]

                work = requests.get(
                    f"https://openlibrary.org{work_key}.json",
                    timeout=5
                )

                if work.status_code == 200:

                    work_data = work.json()

                    description = work_data.get("description")

                    if isinstance(description, dict):
                        book["summary"] = description.get("value", "")

                    elif isinstance(description, str):
                        book["summary"] = description
                
            if data.get("languages"):

                lang = data["languages"][0]["key"]

                book["language"] = lang.split("/")[-1]
            
            if data.get("covers"):
                cover_id = data["covers"][0]

                book["cover"] = (
                    f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                )

            return book
        
        except Exception:
            return None
    
    @staticmethod
    def googlebooks(isbn):

        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

        try:

            r = requests.get(url, timeout=5)

            if r.status_code != 200:
                return None
            
            data = r.json()

            if data["totalItems"] == 0:
                return None
            
            info = data["items"][0]["volumeInfo"]

            return {
                "title": info.get("title", ""),
                "author": ", ".join(info.get("authors", [])),
                "published": int(info.get("publishedDate", "0")[:4]) if info.get("publishedDate") else None,
                "edition": info.get("publisher", ""),
                "summary": info.get("description", ""),
                "language": info.get("language", ""),
                "cover": info["imageLinks"].get("thumbnail", ""),
            }
        
        except Exception:
            return None
        
    @classmethod
    def search(cls, isbn):
        book = cls.openlibrary(isbn)

        if not book:
            book = {}

        missing_fields = [
            key for key, value in book.items()
            if not value
        ]

        if missing_fields:
            google_book = cls.googlebooks(isbn)

            if google_book:
                for field in missing_fields:
                    if google_book.get(field):
                        book[field] = google_book[field]
        
        return book
