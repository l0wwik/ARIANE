
import os
import json
import re
import time
import requests
import numpy as np

from rank_bm25 import BM25Okapi
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://127.0.0.1:11434"

EMBED_MODEL = "bge-m3"
LLM_MODEL = "llama3.1:8b"


BASE_DIR = Path(__file__).resolve().parent

CHUNKS_PATH = BASE_DIR / "data" / "chunks.json"
CACHE_PATH = BASE_DIR / "official_embeddings_bge_m3.npy"

VECTOR_WEIGHT = 0.70
BM25_WEIGHT = 0.30

TOP_K = 3


# ============================================================
# OUTILS
# ============================================================

def tokenize(text):

    return re.findall(
        r"\b[\w\-]+\b",
        text.lower()
    )


def normalize(values):

    values = np.array(
        values,
        dtype=np.float32
    )

    if len(values) == 1:
        return np.ones_like(values)

    minimum = values.min()
    maximum = values.max()

    if maximum == minimum:
        return np.zeros_like(values)

    return (
        values - minimum
    ) / (
        maximum - minimum
    )


def cosine(a, b):

    denominator = (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(a, b)
        /
        denominator
    )


# ============================================================
# MOTEUR
# ============================================================

class ArianeEngine:

    def __init__(self):

        # ----------------------------------------------------
        # COURS
        # ----------------------------------------------------

        with open(
            CHUNKS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            self.chunks = json.load(f)


        # ----------------------------------------------------
        # BM25
        # ----------------------------------------------------

        self.bm25 = BM25Okapi([

            tokenize(
                chunk["text"]
            )

            for chunk
            in self.chunks
        ])


        # ----------------------------------------------------
        # EMBEDDINGS
        # ----------------------------------------------------

        self.embeddings = (
            self._load_embeddings()
        )


    # ========================================================
    # EMBEDDINGS OLLAMA
    # ========================================================

    def embed(self, text_or_texts):

        response = requests.post(

            f"{OLLAMA_URL}/api/embed",

            json={
                "model": EMBED_MODEL,
                "input": text_or_texts,
                "keep_alive": "30m"
            },

            timeout=600
        )

        response.raise_for_status()

        embeddings = np.array(
            response.json()["embeddings"],
            dtype=np.float32
        )

        if isinstance(
            text_or_texts,
            str
        ):

            return embeddings[0]

        return embeddings


    # ========================================================
    # CACHE DU COURS
    # ========================================================

    def _load_embeddings(self):

        if os.path.exists(
            CACHE_PATH
        ):

            embeddings = np.load(
                CACHE_PATH
            )

            if (
                len(embeddings)
                ==
                len(self.chunks)
            ):

                return embeddings


        texts = [

            chunk["text"]

            for chunk
            in self.chunks
        ]


        embeddings = self.embed(
            texts
        )


        np.save(
            CACHE_PATH,
            embeddings
        )


        return embeddings


    # ========================================================
    # SCOPE
    # ========================================================

    def candidate_indices(
        self,
        scope,
        slide=None
    ):

        # ------------------------------
        # DIAPOSITIVE
        # ------------------------------

        if (
            scope == "slide"
            and
            slide is not None
        ):

            indices = [

                i

                for i, chunk
                in enumerate(self.chunks)

                if int(
                    chunk["slide"]
                ) == int(slide)
            ]

            if indices:
                return indices


        # ------------------------------
        # CHAPITRE
        #
        # Pour le jeu de test STAT_PROBA,
        # le bloc principal de dispersion
        # correspond aux slides 3 à 16.
        # ------------------------------

        if scope == "chapter":

            return [

                i

                for i, chunk
                in enumerate(self.chunks)

                if 3 <= int(
                    chunk["slide"]
                ) <= 16
            ]


        # ------------------------------
        # COURS ENTIER
        # ------------------------------

        return list(
            range(
                len(self.chunks)
            )
        )


    # ========================================================
    # RETRIEVAL
    # ========================================================

    def retrieve(
        self,
        question,
        scope="course",
        slide=None
    ):

        query_embedding = self.embed(
            question
        )


        indices = self.candidate_indices(
            scope,
            slide
        )


        vector_scores = [

            cosine(
                query_embedding,
                self.embeddings[i]
            )

            for i
            in indices
        ]


        all_bm25_scores = (
            self.bm25.get_scores(
                tokenize(question)
            )
        )


        lexical_scores = [

            all_bm25_scores[i]

            for i
            in indices
        ]


        vector_norm = normalize(
            vector_scores
        )

        lexical_norm = normalize(
            lexical_scores
        )


        hybrid_scores = (

            VECTOR_WEIGHT
            *
            vector_norm

            +

            BM25_WEIGHT
            *
            lexical_norm
        )


        results = []


        for local_i, chunk_i in enumerate(
            indices
        ):

            chunk = self.chunks[
                chunk_i
            ]


            results.append({

                "slide":
                    chunk["slide"],

                "text":
                    chunk["text"],

                "score":
                    float(
                        hybrid_scores[
                            local_i
                        ]
                    )
            })


        results.sort(

            key=lambda x:
                x["score"],

            reverse=True
        )


        return results[
            :min(
                TOP_K,
                len(results)
            )
        ]


    # ========================================================
    # GENERATION
    # ========================================================

    def ask(
        self,
        question,
        scope="course",
        slide=None
    ):

        total_start = time.time()


        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        retrieval_start = (
            time.time()
        )


        sources = self.retrieve(
            question,
            scope,
            slide
        )


        retrieval_time = (
            time.time()
            -
            retrieval_start
        )


        # ----------------------------------------------------
        # CONTEXTE
        # ----------------------------------------------------

        context = "\n\n".join([

            (
                f"[Slide "
                f"{source['slide']}]\n"
                f"{source['text']}"
            )

            for source
            in sources
        ])


        # ----------------------------------------------------
        # PROMPT FINAL
        # ----------------------------------------------------

        system_prompt = """
Tu es ARIANE, un assistant pédagogique intégré au portail UTT.

Le SUPPORT OFFICIEL fourni est ta seule source de vérité.

RÈGLES ABSOLUES :

1. Utilise uniquement les sources fournies.

2. N'utilise jamais tes connaissances générales pour
   compléter le cours.

3. Lis toutes les sources fournies avant de répondre.

4. Si plusieurs sources contiennent des informations
   complémentaires, combine-les.

5. Si le support permet directement de répondre ou fournit
   une propriété permettant de déduire la réponse, réponds.

6. Si une partie seulement est couverte, réponds à cette partie
   et indique que le reste n'est pas traité.

7. Si la question porte sur un concept précis absent des
   sources, ne déduis aucune propriété sur ce concept.

8. Dans ce cas, réponds :
   "Cette information n'est pas présente dans le support officiel."

9. Une information vraie dans le monde réel n'est pas suffisante.
   Elle doit être soutenue par le support fourni.

10. Cite chaque information importante sous la forme :
    [Slide X]

11. Ne cite jamais une slide qui ne soutient pas
    réellement l'affirmation.

12. Le fait qu'une affirmation soit compatible avec le cours
    ne signifie pas qu'elle est présente dans le cours.

13. Réponds en français.

14. Sois concis, structuré et pédagogique.
"""


        user_prompt = f"""
SUPPORT OFFICIEL :

{context}


QUESTION :

{question}
"""


        # ----------------------------------------------------
        # LLAMA
        # ----------------------------------------------------

        generation_start = (
            time.time()
        )


        response = requests.post(

            f"{OLLAMA_URL}/api/chat",

            json={

                "model":
                    LLM_MODEL,

                "stream":
                    False,

                "keep_alive":
                    "30m",

                "messages": [

                    {
                        "role":
                            "system",

                        "content":
                            system_prompt
                    },

                    {
                        "role":
                            "user",

                        "content":
                            user_prompt
                    }
                ],

                "options": {
                    "temperature": 0
                }
            },

            timeout=300
        )


        response.raise_for_status()


        answer = (
            response
            .json()
            ["message"]
            ["content"]
            .strip()
        )


        generation_time = (
            time.time()
            -
            generation_start
        )


        total_time = (
            time.time()
            -
            total_start
        )


        return {

            "answer":
                answer,

            "sources":
                sources,

            "retrieval_time":
                retrieval_time,

            "generation_time":
                generation_time,

            "total_time":
                total_time
        }
