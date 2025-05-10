from chromadb_functions import get_situation_from_chromadb_by_id
from flask import jsonify
from models import db, Ticket
from tasks import update_mfc_db_task, update_chromadb_task
from celery.result import AsyncResult
from tasks import celery
from flask_app import create_app

app = create_app()

update_task = None
update_chromadb_task_instance = None

with app.app_context():
    db.create_all()

@app.route('/update_mfc_db', methods=['POST'])
def update_mfc_db():
    global update_task
    update_task = update_mfc_db_task.delay()
    return jsonify({"status": "Update started"}), 202

@app.route('/update_chromadb', methods=['POST'])
def update_chromadb():
    global update_chromadb_task_instance
    update_chromadb_task_instance = update_chromadb_task.delay()
    return jsonify({"status": "Chromadb update started"}), 202

@app.route('/is_updating', methods=['GET'])
def is_updating():
    if update_task:
        task_result = AsyncResult(update_task.id, app=celery)
        if task_result.state == 'PENDING':
            return jsonify({"status": "Update in progress"})
        else:
            return jsonify({"status": "Update completed"})
    return jsonify({"status": "No update in progress"})

@app.route('/is_chromadb_updating', methods=['GET'])
def is_chromadb_updating():
    if update_chromadb_task_instance:
        task_result = AsyncResult(update_chromadb_task_instance.id, app=celery)
        if task_result.state == 'PENDING':
            return jsonify({"status": "Chromadb update in progress"})
        else:
            return jsonify({"status": "Chromadb update completed", "result": task_result.result})
    return jsonify({"status": "No chromadb update in progress"})

@app.route('/get_situation_by_id/<string:ticket_id>', methods=['GET'])
def get_situation_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        return jsonify({
            "id": ticket.id,
            "text": ticket.text,
            "topic": ticket.topic,
            "link": ticket.link
        })
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/get_situation_from_chromadb_by_id/<string:ticket_id>', methods=['GET'])
def get_situation_from_vectordb_by_id(ticket_id):
    result = get_situation_from_chromadb_by_id(ticket_id)
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)