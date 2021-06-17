
from flask import Flask
from flask_cors import CORS

from routes import employee_routes, reimbursement_routes

app: Flask = Flask(__name__)
CORS(app)
employee_routes.create_routes(app)
reimbursement_routes.create_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
