from flask import Flask, make_response, jsonify, request

# pip install pymongo --> run this command in terminal
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017')
db = client.bizDB
businesses = db.biz


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return make_response("<h1>Welcome to Flask</h1>", 200)


@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    
    page_num, page_size = 1, 2
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
        
    page_start = (page_size * (page_num - 1))
    
    data_to_return = []
    
    for business in businesses.find().skip(page_start).limit(page_size):
        business['_id'] = str(business['_id'])
        
        #for review in business['reviews']:
            #review['_id'] = str(review['_id'])
            
        data_to_return.append(business)
    
    return make_response(jsonify(data_to_return), 200)


# fetch by ID
@app.route("/api/v1.0/businesses/<int:biz_id>", methods=["GET"])
def show_one_businesses(biz_id):
    data_to_return = [business for business in businesses
                      if business["id"] == biz_id]

    return make_response(jsonify(data_to_return[0]), 200)


# Post method to add new business
@app.route("/api/v1.0/businesses/", methods=["POST"])
def add_new_business():
    next_id = businesses[-1]["id"] + 1

    new_business = {
        "id": next_id,
        "name": request.form["name"],
        "town": request.form["town"],
        "rating": request.form["rating"],
        "reviews": []
    }

    businesses.append(new_business)

    return make_response(jsonify(new_business), 201)

# PUT method to modify existing record
@app.route("/api/v1.0/businesses/<int:biz_id>", methods=["PUT"])
def edit_business(biz_id):
    for business in businesses:
        if business['id'] == biz_id:
            business['name'] = request.form['name']
            business['town'] = request.form['town']
            business['rating'] = request.form['rating']
            break
    
    return make_response(jsonify(business), 200)

# DELETE Method 
@app.route("/api/v1.0/businesses/<int:biz_id>", methods=["DELETE"])
def delete_business(biz_id):
    for business in businesses:
        if business['id'] == biz_id:
            businesses.remove(business)

    return make_response(jsonify({"Message":"Business removed successfully!!!"}))

if __name__ == "__main__":
    app.run(debug=True)