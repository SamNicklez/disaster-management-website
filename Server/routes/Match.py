from flask import Blueprint, jsonify, request
from stores import db
from models.Pledges import Pledge
from models.DonationRequest import DonationRequest
from models.Response import Response
from models.DisasterEvent import DisasterEvent, EventItem
from routes import admin_auth
from geopy.distance import geodesic

matches_bp = Blueprint('Matches', __name__)

@matches_bp.route('/AutoMatchRequestToPledge', methods=['POST'])
@admin_auth.login_required
def match_request_to_pledge():
    data = request.get_json()
    request_id = data.get('request_id')

    if not request_id:
        return jsonify({"error": "request_id is required"}), 400

    try:
        donation_request = DonationRequest.query.filter_by(request_id=request_id).first()
        if not donation_request:
            return jsonify({"error": "Request not found"}), 404
        
        # Fetch the event associated with the request
        event = DisasterEvent.query.filter_by(event_id=donation_request.event_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        event_location = (event.latitude, event.longitude)
        event_item = EventItem.query.filter_by(event_item_id=donation_request.event_item_id).first()
        if not event_item:
            return jsonify({"error": "Event item not found"}), 404

        pledges = Pledge.query.filter(Pledge.item_id == event_item.item_id, Pledge.quantity_remaining > 0).all()
        
        pledges = sorted(
            pledges,
            key=lambda x: geodesic(
                (x.user.latitude, x.user.longitude), event_location).kilometers
        )
        
        if pledges:
            for pledge in pledges:
                quantity_to_donate = min(donation_request.quantity_remaining, pledge.quantity_remaining)
                
                if quantity_to_donate > 0:
                    new_response = Response(
                        request_id=request_id,
                        user_id=pledge.user_id,
                        is_fulfilled=1,
                        quantity_donated=quantity_to_donate
                    )
                    db.session.add(new_response)

                    donation_request.quantity_remaining -= quantity_to_donate
                    donation_request.is_fulfilled = 1 if donation_request.quantity_remaining == 0 else 0

                    pledge.quantity_remaining -= quantity_to_donate
                    if pledge.quantity_remaining == 0:
                        pledge.is_fulfilled = 1

                    db.session.commit()
                    
        else:
            return jsonify({"error": "Pledge Not Found"}), 404

        # Serialize the updated request and its item details
        updated_request = {
            "request_id": donation_request.request_id,
            "event_id": donation_request.event_id,
            "user_id": donation_request.user_id,
            "event_item_id": donation_request.event_item_id,
            "is_fulfilled": donation_request.is_fulfilled,
            "quantity_requested": donation_request.quantity_requested,
            "quantity_remaining": donation_request.quantity_remaining,
        }

        return jsonify({"message": "Request processed successfully", "updated_request": updated_request}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@matches_bp.route('/ManualMatchRequestToPledge', methods=['POST'])
@admin_auth.login_required
def match_specific_request_to_pledge():
    data = request.get_json()
    request_id = data.get('request_id')
    pledge_id = data.get('pledge_id')

    if not request_id or not pledge_id:
        return jsonify({"error": "Both request_id and pledge_id are required"}), 400

    try:
        donation_request = DonationRequest.query.filter_by(request_id=request_id, is_fulfilled=0).first()
        if not donation_request:
            return jsonify({"error": "Request not found or already fulfilled"}), 404

        pledge = Pledge.query.filter(Pledge.pledge_id == pledge_id, Pledge.quantity_remaining > 0).first()
        if not pledge:
            return jsonify({"error": "Pledge not found or has no remaining quantity"}), 404

        # Determine the quantity that can be fulfilled
        quantity_to_donate = min(donation_request.quantity_remaining, pledge.quantity_remaining)
        
        if quantity_to_donate > 0:
            # Create the response
            new_response = Response(
                request_id=request_id,
                user_id=pledge.user_id,
                is_fulfilled=1,
                quantity_donated=quantity_to_donate
            )
            db.session.add(new_response)

            # Update the donation request and pledge
            donation_request.quantity_remaining -= quantity_to_donate
            donation_request.is_fulfilled = 1 if donation_request.quantity_remaining == 0 else 0
            pledge.quantity_remaining -= quantity_to_donate
            pledge.is_fulfilled = 1 if pledge.quantity_remaining == 0 else 0

            db.session.commit()

            # Serialize the response details for the response body
            response_details = {
                "response_id": new_response.response_id,
                "request_id": new_response.request_id,
                "user_id": new_response.user_id,
                "is_fulfilled": new_response.is_fulfilled,
                "quantity_donated": new_response.quantity_donated,
            }

            return jsonify({"message": "Request matched to pledge successfully", "response_details": response_details}), 200
        else:
            return jsonify({"error": "Unable to match request to pledge due to insufficient quantity"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
