from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017/')

router_db = client["ipa2025"]
router_col = router_db["routers"]

sample = Flask(__name__)

data = []

@sample.route("/")
def main():
    # Get data from MongoDB and store in data list
    data.clear()  # Clear existing data
    mongo_data = router_col.find({}, {"router_ip": 1, "username": 1})
    for doc in mongo_data:
        data.append({
            "router_ip": doc["router_ip"],
            "username": doc["username"]
        })
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_router():
    router_ip = request.form.get("router_ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if router_ip and username and password:
        # Store in MongoDB
        router_col.insert_one({
            "router_ip": router_ip,
            "username": username,
            "password": password
        })
        # Store in data list (only router_ip and username)
        data.append({"router_ip": router_ip, "username": username})
    return redirect(url_for("main"))

@sample.route("/delete/<idx>", methods=["POST"])
def delete_router(idx):
    idx = int(idx)
    try:
        if 0 <= idx < len(data):
            # Get the router_ip to delete from MongoDB
            router_to_delete = data[idx]["router_ip"]
            # Delete from MongoDB
            router_col.delete_one({"router_ip": router_to_delete})
            # Delete from data list
            data.pop(idx)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)