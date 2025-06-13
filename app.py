from flask import Flask, jsonify, render_template, request
from scraper import scrape_newegg

app = Flask(__name__)

# Define the categories you want to feature on the homepage
FEATURED_CATEGORIES = [
    {"title": "Graphics Cards", "term": "graphics card"},
    {"title": "Processors (CPU)", "term": "cpu processor"},
    {"title": "Motherboards", "term": "amd motherboard"},
    {"title": "Memory (RAM)", "term": "ddr5 ram 32gb"},
]


@app.route("/")
def home():
    """
    Serves the main search page.
    This function now pre-scrapes featured categories to display on load.
    """
    featured_data = {}
    print("Loading homepage, scraping featured categories...")
    for category in FEATURED_CATEGORIES:
        # For each category, scrape the top few results.
        # We pass the search term from our list to the scraper.
        parts = scrape_newegg(category["term"])
        if parts:
            # We only want to show a handful, e.g., the first 10
            featured_data[category["title"]] = parts[:10]

    print("Finished scraping featured categories.")
    # Pass the dictionary of scraped data to the template
    return render_template("index.html", featured_data=featured_data)


@app.route("/build")
def build_page():
    """ Serves the dedicated build summary page. """
    return render_template("build.html")


@app.route("/api/search")
def search_api():
    """ API endpoint that runs the scraper based on a user's query. """
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "A search query is required."}), 400

    print(f"API received search query: '{query}'. Running scraper...")
    parts_data = scrape_newegg(query)
    print(f"Scraper finished. Found {len(parts_data)} parts.")

    return jsonify(parts_data)


if __name__ == "__main__":
    app.run(debug=True)