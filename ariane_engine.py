import os
import requests


class ArianeEngine:

    def __init__(self):

        self.api_url = os.environ.get(
            "ARIANE_API_URL",
            ""
        ).rstrip("/")

        self.api_key = os.environ.get(
            "ARIANE_API_KEY",
            ""
        )

        if not self.api_url:
            raise RuntimeError(
                "ARIANE_API_URL n'est pas configurée."
            )

        if not self.api_key:
            raise RuntimeError(
                "ARIANE_API_KEY n'est pas configurée."
            )


    def ask(
        self,
        question,
        scope="course",
        slide=None
    ):

        response = requests.post(
            f"{self.api_url}/ask",

            headers={
                "X-ARIANE-Key":
                    self.api_key
            },

            json={
                "question":
                    question,

                "scope":
                    scope,

                "slide":
                    slide
            },

            timeout=300
        )

        if response.status_code != 200:

            raise RuntimeError(
                f"Erreur ARIANE API "
                f"({response.status_code}) : "
                f"{response.text}"
            )

        return response.json()
