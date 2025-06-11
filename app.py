from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/keto-content")
def keto_content():
    url = request.args.get("url")
    if not url or not url.startswith("https://kizios.com"):
        return jsonify({"error": "URL invalide"}), 400

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Page introuvable"}), 404

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1", class_="entry-title")
    content = soup.find("div", class_="entry-content")

    if not title or not content:
        return jsonify({"error": "Contenu non lisible"}), 500

    result = {
        "title": title.text.strip(),
        "content": content.get_text(separator="\n", strip=True)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
