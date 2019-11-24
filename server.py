from flask import Flask, render_template, request
import invertedindex

""" I'm going to use flask and its very easy to set up and start running. It renders two html files for adding a file and search results."""
app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def indexfile():
    # text = jsonify(request.form['filename'].split("\n\r"))
    f = request.files["file1"]
    search_term = request.form["searchterm"]
    f.save(f.filename)
    print(f.filename)
    status = invertedindex.indexing(str(f.filename), search_term)
    return render_template("searchresult.html", data=status)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
