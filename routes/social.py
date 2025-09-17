from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

social_bp = Blueprint('social_bp', __name__)

# -------------------------------
# Social / Rewards-related Routes
# -------------------------------

@social_bp.get("/available")  
# GET http://127.0.0.1:5001/social/available
def social_available():
    """List available rewards."""
    rewards = [
        {"id": 1, "name": "Coffee Voucher", "points": 50},
        {"id": 2, "name": "Amazon Gift Card", "points": 200},
    ]
    return jsonify({"status": "success", "rewards": rewards}), 200


@social_bp.post("/redeem")  
# POST http://127.0.0.1:5001/social/redeem
# Body: { "reward_id": 1 }
@jwt_required(optional=True)
def social_redeem():
    """Redeem points for a reward."""
    data = request.json or {}
    reward_id = data.get("reward_id")

    if not reward_id:
        return jsonify({"status": "error", "message": "reward_id is required"}), 400

    user = get_jwt_identity()
    return jsonify({"status": "success", "reward_id": reward_id, "redeemed_by": user}), 200


@social_bp.get("/my-points")  
# GET http://127.0.0.1:5001/social/my-points
@jwt_required(optional=True)
def social_my_points():
    """Check personal points balance."""
    user = get_jwt_identity()
    return jsonify({"status": "success", "user": user, "points": 120}), 200


@social_bp.post("/donate-points")  
# POST http://127.0.0.1:5001/social/donate-points
# Body: { "amount": 50, "charity": "Red Cross" }
@jwt_required(optional=True)
def social_donate_points():
    """Donate points to charity."""
    data = request.json or {}
    amount = data.get("amount")
    charity = data.get("charity")

    if not amount or not charity:
        return jsonify({"status": "error", "message": "amount and charity are required"}), 400

    user = get_jwt_identity()
    return jsonify({
        "status": "success",
        "donated": amount,
        "charity": charity,
        "donated_by": user
    }), 200


@social_bp.get("/store")  
# GET http://127.0.0.1:5001/social/store
def social_store():
    """Get rewards available in the office store."""
    store_items = [
        {"id": 101, "name": "Team Lunch", "points": 300},
        {"id": 102, "name": "Office Chair Upgrade", "points": 500},
    ]
    return jsonify({"status": "success", "store": store_items}), 200


@social_bp.post("/suggest")  
# POST http://127.0.0.1:5001/social/suggest
# Body: { "name": "Gym Membership", "points": 400 }
@jwt_required(optional=True)
def social_suggest():
    """Suggest a new reward."""
    data = request.json or {}
    name = data.get("name")
    points = data.get("points")

    if not name or not points:
        return jsonify({"status": "error", "message": "name and points are required"}), 400

    user = get_jwt_identity()
    return jsonify({
        "status": "success",
        "suggested_reward": {"name": name, "points": points},
        "suggested_by": user
    }), 201
