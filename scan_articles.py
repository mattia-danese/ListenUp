import os
import json

# Scan all the *.json news articles in the given directory.
# These json files should be created by news-please:
#     https://github.com/fhamborg/news-please
#
# Returns an array of articles, in JSON format.
# These articles are sorted by date, with the newest article
# at the front (i.e. the newest article is articles[0]).
# 
def scan_articles(articles_dir):
    print("Scanning articles_dir: " + articles_dir)

    # Step 1. Accumulate paths to articles
    article_paths = []
    for path in os.listdir(articles_dir):

        article_path = os.path.join(articles_dir, path)
        if os.path.isfile(article_path):
            article_paths.append(article_path)

    # Step 1.5. Sort the list of paths, to get the oldest
    #           articles first.
    article_paths = sorted(article_paths)

    # Step 2. Read in those paths, and parse to JSON
    articles = []
    for path in article_paths:
        with open(path, 'r') as article_raw:
            articles.append(json.load(article_raw))
    

    articles.reverse()
    #print("Articles JSON array: " + str(articles[0]))

    return articles

# Filters the given list of articles to only those
# that are relevant to the query.
def query_articles(query, articles):

    #print("About to query articles: " + str(articles[:5]))

    def query_matches_article(article):
        # Split query up into words
        query_fragments = query.split()

        # Does any piece of the query appear in the article
        # title?
        for fragment in query_fragments:
            if fragment in article['title']:
                return True
            
        return False

    return list(filter(query_matches_article, articles))[:5]