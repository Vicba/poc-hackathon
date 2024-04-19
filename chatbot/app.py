from flask import Flask, jsonify, request
from flask_cors import CORS
from retriever import Retriever
import weaviate

# from build_knowledge_base.populate import create_movies_collection, import_movies_data, get_collection_length

app = Flask(__name__)

CORS(app)


retriever = Retriever()


@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})


# @app.route('/populate')
# def populate():
#     try:
#         client = weaviate.connect_to_local(host="weaviate", port=8080)

#         create_movies_collection(client)
#         import_movies_data(client)
#         collection_length = get_collection_length(client)
#         return jsonify({'message': 'Populated Weaviate!', 'collection_length': collection_length})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

# @app.route('/check-db')
# def check_db() -> str:
#     try:
#         client = weaviate.connect_to_local(host="weaviate", port=8080)
#         collection_length = get_collection_length(client)
#         return jsonify({'message': 'Connected to Weaviate!', 'collection_length': collection_length})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)