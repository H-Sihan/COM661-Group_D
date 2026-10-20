from flask import Flask, make_response, jsonify, request

# pip install pymongo --> run this command in terminal
from pymongo import MongoClient
from bson import ObjectId

# pip install Pyjwt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client.bizDB
businesses = db.biz

app.config['SECRET_KEY'] = 'mysecret'

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return make_response(jsonify({"message": "Token is missing"}), 401)

        try:
            data = jwt.decode(token,
                    app.config['SECRET_KEY'],
                    algorithms="HS256")
        except:
            return make_response(jsonify({"message":"Token is invalid"}), 401)
        
        return func(*args, **kwargs)

    return jwt_required_wrapper

@app.route("/api/v1.0/login", methods=['GET'])
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({
            'user' : auth.username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=8)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
        )

        return make_response(jsonify({"token": token}),200)
    
    return make_response("Could not verify", 401, \
        {'WWW-Authenticate': 'Basic realm = "Login required"'})


#================================ Business ======================
@app.route("/", methods=["GET"])
def index():
    return make_response("<h1>Welcome to Flask</h1>", 200)


@app.route("/api/v1.0/businesses", methods=["GET"])
@jwt_required
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
@app.route("/api/v1.0/businesses/<string:biz_id>", methods=["GET"])
def show_one_businesses(biz_id):
    business = businesses.find_one({'_id':ObjectId(biz_id)})

    if business is not None:
        business['_id'] = str(business['_id'])

        #for review in business['reviews']:
            #review['_id'] = str(review['_id'])
        
        return make_response(jsonify(business), 200)

    else:
        return make_response(jsonify({"error":"Invalid business ID"}), 404)


# Post method to add new business
@app.route("/api/v1.0/businesses/", methods=["POST"])
def add_new_business():
    if "name" in request.form and "town" in request.form \
        and "rating" in request.form:

        new_business = {
            "name": request.form['name'],
            "town": request.form['town'],
            "rating": request.form['rating'],
            "review": [],
        }

        new_business_id = businesses.insert_one(new_business)

        new_business_link = "http://127.0.0.1:5000/api/v1.0/businesses/"\
            + str(new_business_id.inserted_id)

        return make_response(jsonify({"url": new_business_link}), 201)
    
    else:
        return make_response(jsonify({"error":"Missing form data"}), 404)


# PUT method to modify existing record
@app.route("/api/v1.0/businesses/<string:biz_id>", methods=["PUT"])
def edit_business(biz_id):
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        results = businesses.update_one(
            {"_id":ObjectId(biz_id)},{
                "$set": {
                    "name": request.form['name'],
                    "town": request.form['town'],
                    "rating": request.form['rating'],
                }
            }
        )

        if results.matched_count == 1:
            edited_link = "http://127.0.0.1:5000/api/v1.0/businesses/"\
                + biz_id
            
            return make_response(jsonify({"url": edited_link}),200)
        else:
            return make_response(jsonify({"error":"Invalid business ID"}), 404)
    
    else:
        return make_response(jsonify({"error":"Missing form data"}), 404)

# DELETE Method 
@app.route("/api/v1.0/businesses/<string:biz_id>", methods=["DELETE"])
def delete_business(biz_id):
    result = businesses.delete_one({"_id": ObjectId(biz_id)})

    if result.deleted_count == 1:
        return make_response(jsonify({"message":"Business deleted"}),200)
    
    else:
        return make_response(jsonify({"error":"Invalid Business ID"}),404)

if __name__ == "__main__":
    app.run(debug=True)