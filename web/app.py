from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

router_db = client["ipa2025"]
router_col = router_db["routers"]


sample = Flask(__name__)

data = []

@sample.route("/")
def main():
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_router():
    router_ip = request.form.get("router_ip")
    username = request.form.get("username")
    password = request.form.get("password")


    if router_ip and username and password:
        data.append({"router_ip": router_ip, "username": username, "password": password})
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_router():
    try:
        idx = int(request.form.get("idx"))
        if 0 <= idx < len(data):
            data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)

@sample.route("/delete/<idx>", methods=["POST"])
def delete_router(idx):
    idx = int(idx)
    try:
        if 0 <= idx < len(data):
            data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)