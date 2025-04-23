from flask import jsonify
from models import db, Ticket
from tasks import update_mfc_db_task
from celery.result import AsyncResult
from mfc_parser import celery
from flask_app import create_app

app = create_app()

update_task = None

with app.app_context():
    db.create_all()

@app.route('/update_mfc_db', methods=['POST'])
def update_mfc_db():
    global update_task
    update_task = update_mfc_db_task.delay()
    return jsonify({"status": "Update started"}), 202

@app.route('/is_updating', methods=['GET'])
def is_updating():
    if update_task:
        task_result = AsyncResult(update_task.id, app=celery)
        if task_result.state == 'PENDING':
            return jsonify({"status": "Update in progress"})
        else:
            return jsonify({"status": "Update completed"})
    return jsonify({"status": "No update in progress"})

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=False)
