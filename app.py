import os
from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "demo_secret_key"

# Mock product data
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 99.99, "description": "Noise-cancelling over-ear headphones."},
    {"id": 2, "name": "Smartwatch", "price": 149.99, "description": "Track your fitness and notifications."},
    {"id": 3, "name": "Gaming Mouse", "price": 49.99, "description": "High precision and customizable buttons."}
]

# Function to read all code files for display
def load_repo_code():
    repo_code = {}
    base_dir = os.path.dirname(__file__)
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".py", ".txt", ".yaml", ".html", ".md")):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, base_dir)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        repo_code[relpath] = f.read()
                except Exception as e:
                    repo_code[relpath] = f"Error reading file: {e}"
    return repo_code

@app.route("/")
def home():
    repo_code = load_repo_code()
    return render_template("home.html", products=PRODUCTS, repo_code=repo_code)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        flash("Product not found!", "error")
        return redirect(url_for("home"))
    return render_template("product_detail.html", product=product)

@app.route("/checkout", methods=["POST"])
def checkout():
    product_id = int(request.form.get("product_id"))
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        flash(f"Successfully purchased {product['name']} for ${product['price']}!", "success")
    else:
        flash("Product not found!", "error")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
