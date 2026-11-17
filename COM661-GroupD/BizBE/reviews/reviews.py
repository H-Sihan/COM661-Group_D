from flask import Blueprint, make_response, jsonify, request
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals

review_bp = Blueprint("review_bp", __name__)

businesses = globals.db.biz

@review_bp.route("/api/v1.0/businesses/<string:biz_id>/reviews", methods=['GET'])
@jwt_required
def get_all_reviews(biz_id):
    for business in businesses:
        if business['id'] == biz_id:
            break

    return make_response(jsonify(business["reviews"]), 200)

@review_bp.route("/api/v1.0/businesses/<string:biz_id>/reviews", methods=['POST'])
@jwt_required
def add_new_review(biz_id): 
    new_review = {
        "_id": ObjectId(),
        "username": request.form['username'],
        "comments": request.form['comments'],
        "stars": request.form['stars']
        }
        
    businesses.update_one({ "_id" : ObjectId(biz_id) },\
        {"$push": {"review":new_review}})

    new_review_link = "http://127.0.0.1:5001/api/v1.0/businesses/"+ biz_id +"/reviews"\
        + str(new_review["_id"])
    
    return make_response(jsonify({"url": new_review_link}), 201)
    


@review_bp.route("/api/v1.0/businesses/<int:biz_id>/reviews/<int:rev_id>", methods=['GET'])
@jwt_required
def fetch_one_review(biz_id, rev_id):
    for business in businesses:
        if business["id"] == biz_id:
            for review in business["reviews"]:
                if review["id"] == rev_id:
                    break
            break
    
    return make_response(jsonify(review), 200)

@review_bp.route("/api/v1.0/businesses/<int:biz_id>/reviews/<int:rev_id>", methods=['PUT'])
@jwt_required
def update_review(biz_id, rev_id):
    for business in businesses:
        if business["id"] == biz_id:
            for review in business["reviews"]:
                if review["id"] == rev_id:
                    review["username"] = request.form["username"]
                    review["comments"] = request.form["comments"]
                    review["stars"] = request.form["stars"]
                    break
            break
    
    return make_response(jsonify(review), 200)


@review_bp.route("/api/v1.0/businesses/<int:biz_id>/reviews/<int:rev_id>", methods=['DELETE'])
@jwt_required
def delete_review(biz_id, rev_id):
    for business in businesses:
        if business["id"] == biz_id:
            for review in business["reviews"]:
                if review["id"] == rev_id:
                    business["review"].remove(review)
                    break
            break
    
    return make_response(jsonify({"Message":"Review Deleted successfully!!!"}), 200)