from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from pymongo.errors import PyMongoError, OperationFailure

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/note_taking_db"
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

mongo = PyMongo(app)

# Test MongoDB connection
try:
    mongo.db.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Create database and collections
try:
    db = mongo.cx['note_taking_db']
    
    if 'notes' not in db.list_collection_names():
        db.create_collection('notes')
        print("'notes' collection created.")
    
    if 'todos' not in db.list_collection_names():
        db.create_collection('todos')
        print("'todos' collection created.")
    
    print("Database and collections are set up.")
except OperationFailure as e:
    print(f"An error occurred while setting up the database: {e}")

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        notes = list(mongo.db.notes.find())
        for note in notes:
            note['_id'] = str(note['_id'])
        print(f"Retrieved {len(notes)} notes")
        return jsonify(notes)
    except PyMongoError as e:
        print(f"MongoDB error in get_notes: {e}")
        return jsonify({"error": "Failed to retrieve notes"}), 500

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        todos = list(mongo.db.todos.find())
        for todo in todos:
            todo['_id'] = str(todo['_id'])
        print(f"Retrieved {len(todos)} todos")
        return jsonify(todos)
    except PyMongoError as e:
        print(f"MongoDB error in get_todos: {e}")
        return jsonify({"error": "Failed to retrieve todos"}), 500

@app.route('/api/notes', methods=['POST'])
def add_note():
    try:
        data = request.json
        print(f"Received note data: {data}")
        note_id = mongo.db.notes.insert_one({'text': data['text']}).inserted_id
        new_note = mongo.db.notes.find_one({'_id': note_id})
        new_note['_id'] = str(new_note['_id'])
        print(f"Note added: {new_note}")
        return jsonify(new_note)
    except PyMongoError as e:
        print(f"MongoDB error in add_note: {e}")
        return jsonify({"error": "Failed to add note"}), 500
    except Exception as e:
        print(f"Unexpected error in add_note: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        data = request.json
        print(f"Received todo data: {data}")
        todo_id = mongo.db.todos.insert_one({'text': data['text']}).inserted_id
        new_todo = mongo.db.todos.find_one({'_id': todo_id})
        new_todo['_id'] = str(new_todo['_id'])
        print(f"Todo added: {new_todo}")
        return jsonify(new_todo)
    except PyMongoError as e:
        print(f"MongoDB error in add_todo: {e}")
        return jsonify({"error": "Failed to add todo"}), 500
    except Exception as e:
        print(f"Unexpected error in add_todo: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/notes/<id>', methods=['DELETE'])
def delete_note(id):
    try:
        result = mongo.db.notes.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            print(f"Note deleted: {id}")
            return '', 204
        else:
            print(f"Note not found: {id}")
            return jsonify({"error": "Note not found"}), 404
    except PyMongoError as e:
        print(f"MongoDB error in delete_note: {e}")
        return jsonify({"error": "Failed to delete note"}), 500

@app.route('/api/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    try:
        result = mongo.db.todos.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            print(f"Todo deleted: {id}")
            return '', 204
        else:
            print(f"Todo not found: {id}")
            return jsonify({"error": "Todo not found"}), 404
    except PyMongoError as e:
        print(f"MongoDB error in delete_todo: {e}")
        return jsonify({"error": "Failed to delete todo"}), 500

if __name__ == '__main__':
    print("Server starting on http://127.0.0.1:5000")
    app.run(debug=True)
