from flask import Blueprint, jsonify, request
from stores import db
from models.DisasterEvent import DisasterEvent, EventItem
from models.DonationRequest import DonationRequest
from models.Response import Response
from models.Items import Item
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from routes import admin_auth, donor_auth, recipient_auth
import json
import jwt

events_bp = Blueprint('Event', __name__)


@events_bp.route("/CreateEvent", methods=["POST"])
@admin_auth.login_required
def create_event():
    try:
        data = request.json
        event_name = data.get("event_name")
        location = data.get("location")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        start_date = datetime.now()
        end_date = None
        description = data.get("description")
        item_names = data.get("item_names", [])

        new_event = DisasterEvent(
            event_name=event_name,
            location=location,
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        db.session.add(new_event)
        db.session.commit()

        for item_name in item_names:
            item = Item.query.filter_by(ItemName=item_name).first()
            if item:
                new_event_item = EventItem(
                    event_id=new_event.event_id,
                    item_id=item.ItemID
                )
                db.session.add(new_event_item)

        db.session.commit()

        return jsonify({"message": "Event created successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create event", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@events_bp.route("/CreateEventItem", methods=["POST"])
@admin_auth.login_required
def create_event_item():
    try:
        data = request.json
        event_id = data.get("event_id")
        item_names = data.get("item_names", [])

        event = DisasterEvent.query.get(event_id)
        if event is None:
            return jsonify({"error": "Event not found"}), 404

        for item_name in item_names:
            item = Item.query.filter_by(ItemName=item_name).first()
            if item:
                event_item = EventItem(
                    event_id=event_id,
                    item_id=item.ItemID
                )
            db.session.add(event_item)

        db.session.commit()

        return jsonify({"message": "Item names added successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create item names", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@events_bp.route("/isEvent", methods=["GET"])
def is_event():
    event_id = request.args.get('event_id', None)
    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    try:
        event = DisasterEvent.query.filter_by(event_id=event_id, end_date=None).first()
        if event:
            return jsonify({"is_event": True}), 200
        else:
            return jsonify({"is_event": False}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@events_bp.route("/GetAllEvents", methods=["GET"])
def get_all_events():
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetAllEvents')
        events = cursor.fetchall()
        cursor.close()
        conn.close()

        serialized_events = []
        for event in events:
            serialized_event = {
                "event_id": event[0],
                "event_name": event[1],
                "location": event[2],
                "latitude": event[3],
                "longitude": event[4],
                "start_date": event[5],
                "description": event[7]
            }
            serialized_events.append(serialized_event)

        return jsonify({"events": serialized_events}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@events_bp.route("/GetEventById", methods=["GET"])
def get_event_by_id():

    event_id = request.args.get('event_id', None)
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetEventById', [event_id])
        event = cursor.fetchone()
        cursor.close()
        conn.close()

        if event:
            serialized_event = {
                "event_id": event[0],
                "event_name": event[1],
                "location": event[2],
                "latitude": event[3],
                "longitude": event[4],
                "start_date": event[5].strftime("%Y-%m-%d %H:%M:%S"),
                "description": event[7],
                "items": event[8].split(',') if event[8] else []
            }

            return jsonify({"event": serialized_event}), 200

        else:
            return jsonify({"error": "Event not found"}), 404

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@events_bp.route('/CreateItemRequest', methods=['POST'])
@recipient_auth.login_required
def create_item_request():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        user_id = (jwt.decode(token, "secret", algorithms=["HS256"]))["id"]
        data = request.get_json()
        event_id = int(data.get('event_id'))
        item = data.get('item_name')
        quantity_requested = int(data.get('quantity_requested'))
        quantity_remaining = quantity_requested
        item_id = Item.query.filter_by(ItemName=item).first().ItemID
        event_item_id = EventItem.query.filter_by(event_id=event_id, item_id=item_id).first().event_item_id
        if not event_item_id:
            return jsonify({'error': 'Item not found in event'}), 404
        event = DisasterEvent.query.filter_by(event_id=event_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        donation_request = DonationRequest(
            event_id=event_id,
            user_id=user_id,
            event_item_id= event_item_id,
            is_fulfilled=0,
            quantity_remaining=quantity_remaining,
            quantity_requested=quantity_requested,
            created_date=datetime.now()
        )
        db.session.add(donation_request)
        db.session.commit()

        return jsonify({'message': 'Item request created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@events_bp.route('/DeleteEvent', methods=['GET'])
@admin_auth.login_required
def delete_event():
    try:
        event_id = request.args.get('event_id')
        event = DisasterEvent.query.get(event_id)
        if event:
            event.end_date = datetime.now()
            db.session.commit()
            return jsonify({'message': 'Event deleted successfully'}), 200
        else:
            return jsonify({'error': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@events_bp.route('/search', methods=['GET'])
def search_events():
    try:
        search_query = request.args.get('query', '')
        if search_query:
            boolean_search_query = f'{search_query}*'
            search_statement = db.text(
                # Natural Language Mode conditions
                "(MATCH(event_name) AGAINST(:query IN NATURAL LANGUAGE MODE)) OR "
                "(MATCH(description) AGAINST(:query IN NATURAL LANGUAGE MODE)) OR "
                "(MATCH(location) AGAINST(:query IN NATURAL LANGUAGE MODE)) OR "
                # Boolean Mode conditions (for partial matches)
                "(MATCH(event_name) AGAINST(:boolean_query IN BOOLEAN MODE)) OR "
                "(MATCH(description) AGAINST(:boolean_query IN BOOLEAN MODE)) OR "
                "(MATCH(location) AGAINST(:boolean_query IN BOOLEAN MODE))"
            )
            results = DisasterEvent.query.filter(search_statement).params(query=search_query, boolean_query=boolean_search_query).all()
            return jsonify([event.to_dict() for event in results if event.end_date is None])
        else:
            return jsonify({'error': 'No search query provided'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@events_bp.route("/GetAllItemRequestsByEventId", methods=["GET"])
def get_all_item_requests_by_event_id():
    event_id = request.args.get('event_id', None)
    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetRequestsByEventID', [event_id])
        event_details = cursor.fetchone()
        cursor.close()
        conn.close()
        if not event_details:
            return jsonify({"event_id": []}), 200
        json_tmp = {
            "event_id": event_details[0],
            "event_name": event_details[1],
            "location": event_details[2],
            "start_date": event_details[3].strftime("%Y-%m-%d %H:%M:%S"),
            "description": event_details[4],
            "requests": []
        }
        if event_details[5]:
            json_tmp["requests"] = json.loads(event_details[5])
            
        return json_tmp, 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@events_bp.route('/CreateResponse', methods=['POST'])
@donor_auth.login_required
def create_response():
    try:
        request_id = int(request.args.get('request_id', None))
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        user_id = (jwt.decode(token, "secret", algorithms=["HS256"]))["id"]
        request_tmp = DonationRequest.query.filter_by(request_id=request_id).first()
        quantity = request_tmp.quantity_remaining
        new_response = Response(user_id=user_id, request_id=request_id, is_fulfilled=0, quantity_donated=quantity, created_date=datetime.now())
        request_tmp.quantity_remaining = 0
        request_tmp.is_fulfilled = 1
        db.session.add(new_response)
        db.session.commit()
        return jsonify({'message': 'Response created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@events_bp.route("/GetResponsesByRequestId", methods=["GET"])
def get_responses_by_request_id():
    request_id = request.args.get('request_id', None)
    if not request_id:
        return jsonify({"error": "Request ID is required"}), 400

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetResponsesByRequestIdJSON', [request_id])
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        responses = []
        for result in results:
            response_id, user_id, is_fulfilled, created_date, shipped_date, items_json = result
            responses.append({
                "response_id": response_id,
                "user_id": user_id,
                "is_fulfilled": bool(is_fulfilled),
                "created_date": created_date.strftime("%Y-%m-%d %H:%M:%S") if created_date else None,
                "shipped_date": shipped_date.strftime("%Y-%m-%d %H:%M:%S") if shipped_date else None,
                "items": json.loads(items_json)  
            })

        if responses:
            return jsonify({"responses": responses}), 200
        else:
            return jsonify({"error": "No responses found for the given request ID"}), 404

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@events_bp.route("/GetResponsesByEventID", methods=["GET"])
def get_responses_by_event_id():
    event_id = request.args.get('event_id', None)
    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetResponsesByEventID', [event_id])
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        responses = []
        for result in results:
            response_id, request_id, user_id, is_fulfilled, created_date, shipped_date, items_json = result
            responses.append({
                "response_id": response_id,
                "request_id": request_id,
                "user_id": user_id,
                "is_fulfilled": bool(is_fulfilled),
                "created_date": created_date.strftime("%Y-%m-%d %H:%M:%S") if created_date else None,
                "shipped_date": shipped_date.strftime("%Y-%m-%d %H:%M:%S") if shipped_date else None,
                "items": json.loads(items_json)
            })

        if responses:
            return jsonify({"responses": responses}), 200
        else:
            return jsonify({"error": "No responses found for the given event ID"}), 404

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@events_bp.route("/getActiveRequests", methods=["GET"])
def get_active_requests():
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetActiveRequests')  # Call the stored procedure
        requests = cursor.fetchall()  # Fetch all results
        cursor.close()
        conn.close()
 
        serialized_requests = []
        for request in requests:
            serialized_request = {
                "request_id": request[0],
                "event_id": request[1],
                "user_id": request[2],
                "event_item_id": request[3],
                "is_fulfilled": request[4],
                "quantity_requested": request[5],
                "quantity_remaining": request[6],
                "created_date": request[7].strftime("%Y-%m-%d %H:%M:%S") if request[7] else None,
                "modified_date": request[8].strftime("%Y-%m-%d %H:%M:%S") if request[8] else None
            }
            serialized_requests.append(serialized_request)
 
        return jsonify({"active_requests": serialized_requests}), 200
 
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

