from flask import Blueprint, jsonify, request
from stores import db
from models.DisasterEvent import DisasterEvent, EventItem
from models.DonationRequest import DonationRequest, ItemRequest
from models.Items import Item
from routes import admin_auth
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

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
        print(e)
        return jsonify({"error": "Failed to create event", "details": str(e)}), 500

    except Exception as e:
        print(e)
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
                    event_id = event_id,
                    item_id = item.ItemID
                )
            db.session.add(event_item)
        
        db.session.commit()

        return jsonify({"message": "Item names added successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create item names", "details": str(e)}), 500

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
    print(event_id)
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
def create_item_request():
    try:
        data = request.get_json()
        
        event_id = data.get('event_id')
        user_id = data.get('user_id')
        items = data.get('item_names')  

        event = DisasterEvent.query.filter_by(event_id=event_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        donation_request = DonationRequest(
            event_id=event_id, 
            user_id=user_id, 
            is_fulfilled=0, 
            created_date=datetime.now()
        )
        
        db.session.add(donation_request)
        db.session.commit()

        for item_data in items:
            item_name = item_data.get('item_name') 
            quantity = item_data.get('quantity')  

            item = Item.query.filter_by(ItemName=item_name).first()
            if not item:
                db.session.rollback() 
                return jsonify({'error': f'Item "{item_name}" not found'}), 404

            new_item_request = ItemRequest(
                request_id=donation_request.request_id,
                item_id=item.ItemID,  
                quantity=quantity
            )
            db.session.add(new_item_request)

        db.session.commit()

        return jsonify({'message': 'Item request created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    
@events_bp.route('/DeleteEvent', methods=['GET'])
@admin_auth.login_required
def delete_event():
    # Updates the event's end_date to the current date
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
