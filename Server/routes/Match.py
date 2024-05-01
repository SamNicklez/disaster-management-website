from flask import Blueprint, jsonify, request
from stores import db
from models.Pledges import Pledge
from models.DonationRequest import DonationRequest
from models.Response import Response
from models.Items import Item
from models.Users import User
from models.DisasterEvent import DisasterEvent, EventItem
from models.Users import User
from routes import admin_auth
from geopy.distance import geodesic

from sqlalchemy.exc import SQLAlchemyError
from routes import donor_auth
import jwt
from datetime import datetime


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

        pledges = Pledge.query.join(User, Pledge.user_id == User.UserId).filter(
            Pledge.item_id == event_item.item_id,
            Pledge.quantity_remaining > 0
        ).all()
        
        pledges = sorted(
            pledges,
            key=lambda x: geodesic(
                (User.query.get(x.user_id).Latitude, User.query.get(x.user_id).Longitude),
                event_location).kilometers
        )

        potential_pledges = []
        for pledge in pledges:
            user = User.query.get(pledge.user_id) 
            quantity_to_donate = min(donation_request.quantity_remaining, pledge.quantity_remaining)
            if quantity_to_donate > 0:
                pledge_details = {
                    "pledge_id": pledge.pledge_id,
                    "quantity": pledge.quantity_remaining,
                    "state": user.State  
                }
                potential_pledges.append(pledge_details)
                donation_request.quantity_remaining -= quantity_to_donate
                if donation_request.quantity_remaining <= 0:
                    break

        if not potential_pledges:
            return jsonify({"error": "No suitable pledges found"}), 404

        return jsonify({"potential_pledges": potential_pledges}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@matches_bp.route('/ManualMatchRequestToPledge', methods=['POST'])
# @admin_auth.login_required
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
        print(e)
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500    


    
@matches_bp.route('/grabAllActiveRequests', methods=['GET'])
@admin_auth.login_required
def grabAllActiveRequests():
    try:
        # Yes i know this is probs the worst way to do this but i'm tired
        requests = DonationRequest.query.filter_by(is_fulfilled=0).all()
        requests = [request.to_dict() for request in requests]
        return_requests = []
        for request in requests:
            event = DisasterEvent.query.filter_by(event_id=request['event_id']).first()
            if event.end_date != None:
                # Remove this request from list
                requests.remove(request)
            event_item = EventItem.query.filter_by(event_item_id=request['event_item_id']).first()
            request['event'] = event.to_dict_match()
            request['item'] = Item.query.filter_by(ItemID=event_item.item_id).first().to_dict_match()
            if request['item']['isActive'] != -1:
                request.pop('event_id')
                request.pop('event_item_id')
                request.pop('is_fulfilled')
                request.pop('user_id')
                return_requests.append(request)
        return jsonify(return_requests), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/grabPotentialMatches', methods=['POST'])
# @admin_auth.login_required
def grabPotentialMatches():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        pledges = Pledge.query.filter_by(item_id=item_id, is_fulfilled=0).all()
        pledges = [pledge.to_dict() for pledge in pledges]
        for pledge in pledges:
            pledge['location'] = User.query.filter_by(UserId=pledge['user_id']).first().return_state()
            pledge.pop('user_id')
        return jsonify(pledges), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@matches_bp.route('/completeshipment', methods=['POST'])
@donor_auth.login_required
def complete_shipment():
    try:
        response_id = request.json.get('response_id')
        print(response_id)
        shipping_number = request.json.get('shipping_number')
        response = Response.query.get(response_id)
        response.shipping_number = shipping_number
        response.shipped_date = datetime.now()
        db.session.commit()

        return jsonify({'message': 'Shipping information updated successfully.'}), 200


    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the shipment status.'}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500
