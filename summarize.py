import os
import tempfile
import article_summary

# Summarizes the article.
# The argument `text` is a String, containing the text of the article.
# This function returns a String, containing the ML-generated summary of the article.
def summarize(text):
    # Create temporary file for text
    file = tempfile.NamedTemporaryFile()
    file.write(bytes(text, 'utf-8'))
    file.flush()

    # TODO: Li implement
    summary = article_summary.summarize(file.name, 5)
    if summary is None:
        summary = text

    #os.unlink(file.name)

    print(f"Summary generated: {summary}")
    return "summary not yet implemented"

