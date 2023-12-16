from img2vec_pytorch import Img2Vec
from .chroma import collection
import numpy

from PIL import Image
import os


class Img2VecPredictor:
    def __init__(self, model="resnet-18"):
        """
        Initialize the Img2VecPredictor class.

        Args:
            model (str, optional): The path to the model. Defaults set to resnet-18.
        """
        self.img2vec = Img2Vec(model=model)
        self.collection = collection

    def vectorize(self, image_path=None, image=None):
        if image_path is not None:
            image = Image.open(image_path).convert("RGB")
        vector = self.img2vec.get_vec(image)
        return [float(x) for x in vector]

    def find_similar(self, vector: numpy.ndarray):
        """
        Find similar vectors in the collection based on the given input vector.
        Args:
            vector (numpy.ndarray): The input vector to find similar vectors for.
        Returns:
            dict: A dictionary containing the query results, including the top 5 similar vectors and their distances.
        """

        return self.collection.query(
            query_embeddings=[vector],
            n_results=3,
            include=["distances", "metadatas", "embeddings"],
            # where distance <0.09
        )


# Contoh penggunaan
if __name__ == "__main__":
    predictor = Img2VecPredictor()
    img = "Pasted image 4.png"
    vector = predictor.vectorize(image_path=img)
    similar = predictor.find_similar(vector)
    metadata = similar["metadatas"][0]
    distance = similar["distances"][0]
    for meta, dis in zip(metadata, distance):
        name = meta["name"]
        current_time = f"{int(meta['hour']):02d}:{int(meta['minute']):02d}:{int(meta['second']):02d}"
        print(f"Movie: {name} | Time: {current_time} | Distance: {dis}")
