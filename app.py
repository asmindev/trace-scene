from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
import lib.predict as predict
import time

app = Flask(__name__)
CORS(app)
predict = predict.Img2VecPredictor()

app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024  # 3 MB


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify(
        {
            "message": "Request entity too large",
            "code": 413,
            "success": False,
        }
    )


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World!"}), 200


@app.route("/search", methods=["POST"])
def search():
    data = request.files
    image = data.get("image")
    if image is None:
        return jsonify({"message": "No image found"}), 400
    start_time = time.time()
    result = predict.find_similar(vector=predict.vectorize(image_path=image))
    count = predict.collection.count()
    total_time = time.time() - start_time
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]
    for md, dist in zip(metadatas, distances):
        md["distance"] = dist

    # filter results
    metadatas = [md for md in metadatas if md["distance"] < 0.16]
    if len(metadatas) == 0:
        return jsonify({"message": "No results found"}), 404
    return (
        jsonify(
            dict(
                metadatas=metadatas,
                count=count,
                total_time=total_time,
            )
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
