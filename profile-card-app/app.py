from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-profile", methods=["POST"])
def generate_profile():
    name = request.form.get("name")
    bio = request.form.get("bio")
    image_url = request.form.get("image_url")

    profile = {
        "name": name,
        "bio": bio,
        "image_url": image_url
    }

    return render_template("index.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)
