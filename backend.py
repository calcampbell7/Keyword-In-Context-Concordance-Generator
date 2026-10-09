from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from concord3 import generate_concordance


app = FastAPI()

MAX_EXCLUSION_CHARS = 10_000
MAX_BODY_CHARS = 100_000
MAX_BODY_WORDS = 5_000


class ConcordanceRequest(BaseModel):
    exclusion_words: str = Field(max_length=MAX_EXCLUSION_CHARS)
    body_text: str = Field(max_length=MAX_BODY_CHARS)


@app.post("/api/concordance")
def create_concordance(request: ConcordanceRequest):
    exclusion_words = [
        word.strip().lower()
        for word in request.exclusion_words.splitlines()
        if word.strip()
    ]

    body_lines = [
        line.strip()
        for line in request.body_text.splitlines()
        if line.strip()
    ]

    word_count = sum(len(line.split()) for line in body_lines)
    if word_count > MAX_BODY_WORDS:
        raise HTTPException(
            status_code=413,
            detail=f"Body text may contain at most {MAX_BODY_WORDS} words.",
        )

    output_lines = generate_concordance(body_lines, set(exclusion_words))

    return {
        "lines": output_lines,
        "output": "\n".join(output_lines),
    }
