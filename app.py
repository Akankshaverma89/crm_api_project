from flask import Flask, request, jsonify
from flask_cors import CORS

from config import Config
from models import db, User, Lead, FollowUp

# ================= CREATE APP =================
app = Flask(__name__)

app.config.from_object(Config)

# ================= ENABLE CORS =================
CORS(app)

# ================= INITIALIZE DATABASE =================
db.init_app(app)

# ================= CREATE TABLES =================
with app.app_context():
    db.create_all()


# =====================================================
# HOME
# =====================================================
@app.route('/')
def home():

    return jsonify({
        'message': 'CRM API Running Successfully'
    })


# =====================================================
# LOGIN API
# =====================================================
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(
        username=username
    ).first()

    # USER NOT FOUND
    if not user:
        return jsonify({
            'success': False,
            'message': 'User does not exist'
        }), 404

    # WRONG PASSWORD
    if user.password != password:
        return jsonify({
            'success': False,
            'message': 'Incorrect password'
        }), 401

    # SUCCESS
    return jsonify({
    'success': True,
    'message': 'Login successful',
    'user': {
    'id': user.id,
    'username': user.username,
    'company_id': user.company_id
}
}), 200


# =====================================================
# CREATE USER
# =====================================================
@app.route('/users', methods=['POST'])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'No data provided'
        }), 400

    existing_user = User.query.filter_by(
        username=data.get('username')
    ).first()

    if existing_user:
        return jsonify({
            'message': 'Username already exists'
        }), 400

    user = User(
    username=data.get('username'),
    password=data.get('password'),
    company_id=data.get('company_id')
)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


# =====================================================
# GET ALL USERS
# =====================================================
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.order_by(
        User.id.desc()
    ).all()

    return jsonify([
        user.to_dict()
        for user in users
    ])


# =====================================================
# GET SINGLE USER
# =====================================================
@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):

    user = User.query.get_or_404(user_id)

    return jsonify(
        user.to_dict()
    )


# =====================================================
# UPDATE USER
# =====================================================
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    user = User.query.get_or_404(user_id)

    data = request.get_json()

    # CHECK DUPLICATE USERNAME
    existing_user = User.query.filter(
        User.username == data.get('username'),
        User.id != user_id
    ).first()

    if existing_user:
        return jsonify({
            'message': 'Username already exists'
        }), 400

    user.username = data.get(
        'username',
        user.username
    )

    user.password = data.get(
        'password',
        user.password
    )

    user.company_id = data.get(
    'company_id',
    user.company_id
    )

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    })


# =====================================================
# DELETE USER
# =====================================================
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return jsonify({
        'message': 'User deleted successfully'
    })


# =====================================================
# SUMMARY LEADS
# SMALL TABLE
# =====================================================
@app.route('/summary-leads', methods=['GET'])
def summary_leads():

    leads = Lead.query.order_by(
        Lead.id.desc()
    ).all()

    summary = []

    for lead in leads:

        summary.append({
            'id': lead.id,
            'fullName': lead.fullName,
            'company': lead.company,
            'status': lead.status
        })

    return jsonify(summary)


# =====================================================
# GET ALL LEADS
# =====================================================
@app.route('/leads', methods=['GET'])
def get_leads():

    leads = Lead.query.order_by(
        Lead.id.desc()
    ).all()

    return jsonify([
        lead.to_dict()
        for lead in leads
    ])

# =====================================================
# COMPANY LEADS
# =====================================================
@app.route('/company-leads/<username>', methods=['GET'])
def company_leads(username):

    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    leads = Lead.query.filter_by(
        company_id=user.company_id
    ).order_by(
        Lead.id.desc()
    ).all()

    return jsonify([
        lead.to_dict()
        for lead in leads
    ])

# =====================================================
# GET SINGLE LEAD
# =====================================================
@app.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):

    lead = Lead.query.get_or_404(lead_id)

    return jsonify(
        lead.to_dict()
    )


# =====================================================
# LEAD DETAILS + FOLLOWUPS
# =====================================================
@app.route('/lead-details/<int:lead_id>', methods=['GET'])
def lead_details(lead_id):

    lead = Lead.query.get_or_404(lead_id)

    followups = FollowUp.query.filter_by(
        lead_id=lead_id
    ).order_by(
        FollowUp.id.desc()
    ).all()

    return jsonify({

        'lead': lead.to_dict(),

        'followups': [
            followup.to_dict()
            for followup in followups
        ]
    })


# =====================================================
# CREATE LEAD
# =====================================================
@app.route('/leads', methods=['POST'])
def create_lead():

    data = request.get_json()

    gender_map = {
        'Male': 'M',
        'Female': 'F'
    }

    lead = Lead(

        fullName=data.get('fullName'),

        gender=gender_map.get(
            data.get('gender'),
            data.get('gender')
        ),

        address=data.get('address'),

        phone=data.get('phone'),

        email=data.get('email'),

        company=data.get('company'),

        company_id=data.get('company_id'),

        industry=data.get('industry'),

        status=data.get(
            'status',
            'In Progress'
        )
    )

    db.session.add(lead)

    db.session.commit()

    return jsonify({
        'message': 'Lead created successfully',
        'lead': lead.to_dict()
    }), 201


# =====================================================
# UPDATE LEAD
# =====================================================
@app.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):

    lead = Lead.query.get_or_404(lead_id)

    data = request.get_json()

    gender_map = {
        'Male': 'M',
        'Female': 'F'
    }

    lead.fullName = data.get(
        'fullName',
        lead.fullName
    )

    lead.gender = gender_map.get(
        data.get('gender'),
        lead.gender
    )

    lead.address = data.get(
        'address',
        lead.address
    )

    lead.phone = data.get(
        'phone',
        lead.phone
    )

    lead.email = data.get(
        'email',
        lead.email
    )

    lead.company = data.get(
        'company',
        lead.company
    )

    lead.company_id = data.get(
    'company_id',
    lead.company_id
)

    lead.industry = data.get(
        'industry',
        lead.industry
    )

    lead.status = data.get(
        'status',
        lead.status
    )

    db.session.commit()

    return jsonify({
        'message': 'Lead updated successfully',
        'lead': lead.to_dict()
    })


# =====================================================
# DELETE LEAD
# =====================================================
@app.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):

    lead = Lead.query.get_or_404(lead_id)

    db.session.delete(lead)

    db.session.commit()

    return jsonify({
        'message': 'Lead deleted successfully'
    })


# =====================================================
# CREATE FOLLOWUP
# =====================================================
@app.route('/followups', methods=['POST'])
def create_followup():

    data = request.get_json()

    lead = Lead.query.get_or_404(
        data.get('lead_id')
    )

    followup = FollowUp(

        lead_id=lead.id,

        action_type=data.get('action_type'),

        notes=data.get('notes'),

        next_followup_date=data.get(
            'next_followup_date'
        ),

        status=data.get(
            'status',
            'Pending'
        )
    )

    db.session.add(followup)

    db.session.commit()

    return jsonify({
        'message': 'Follow-up created successfully',
        'followup': followup.to_dict()
    }), 201


# =====================================================
# GET ALL FOLLOWUPS
# =====================================================
@app.route('/followups', methods=['GET'])
def get_all_followups():

    followups = FollowUp.query.order_by(
        FollowUp.id.desc()
    ).all()

    return jsonify([
        followup.to_dict()
        for followup in followups
    ])


# =====================================================
# GET FOLLOWUPS BY LEAD
# =====================================================
@app.route('/leads/<int:lead_id>/followups', methods=['GET'])
def get_followups_by_lead(lead_id):

    Lead.query.get_or_404(lead_id)

    followups = FollowUp.query.filter_by(
        lead_id=lead_id
    ).order_by(
        FollowUp.id.desc()
    ).all()

    return jsonify([
        followup.to_dict()
        for followup in followups
    ])


# =====================================================
# UPDATE FOLLOWUP
# =====================================================
@app.route('/followups/<int:followup_id>', methods=['PUT'])
def update_followup(followup_id):

    followup = FollowUp.query.get_or_404(
        followup_id
    )

    data = request.get_json()

    followup.action_type = data.get(
        'action_type',
        followup.action_type
    )

    followup.notes = data.get(
        'notes',
        followup.notes
    )

    followup.next_followup_date = data.get(
        'next_followup_date',
        followup.next_followup_date
    )

    followup.status = data.get(
        'status',
        followup.status
    )

    db.session.commit()

    return jsonify({
        'message': 'Follow-up updated successfully',
        'followup': followup.to_dict()
    })


# =====================================================
# DELETE FOLLOWUP
# =====================================================
@app.route('/followups/<int:followup_id>', methods=['DELETE'])
def delete_followup(followup_id):

    followup = FollowUp.query.get_or_404(
        followup_id
    )

    db.session.delete(followup)

    db.session.commit()

    return jsonify({
        'message': 'Follow-up deleted successfully'
    })

# =====================================================
# DASHBOARD COUNTS
# =====================================================
@app.route('/dashboard-counts', methods=['GET'])
def dashboard_counts():

    return jsonify({

        'total_users': User.query.count(),

        'total_leads': Lead.query.count(),

        'total_followups': FollowUp.query.count()
    })


# =====================================================
# RUN APP
# =====================================================
if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )