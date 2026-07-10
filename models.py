from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ================= USER MODEL =================
class User(db.Model):

    __tablename__ = 'Users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    company_id = db.Column(
    db.Integer,
    nullable=False
)

def to_dict(self):

    return {
        'id': self.id,
        'username': self.username,
        'password': self.password,
        'company_id': self.company_id
    }

# ================= LEAD MODEL =================
class Lead(db.Model):

    __tablename__ = 'leads'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fullName = db.Column(
        db.String(150),
        nullable=False
    )

    gender = db.Column(db.String(10))

    address = db.Column(db.String(255))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(120))

    company = db.Column(db.String(150))

    company_id = db.Column(db.Integer, nullable=False )

    industry = db.Column(db.String(100))

    status = db.Column(
        db.String(50),
        default='In Progress'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
   
    # RELATIONSHIP
    followups = db.relationship(
        'FollowUp',
        backref='lead',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):

        return {
            'id': self.id,
            'fullName': self.fullName,
            'gender': self.gender,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'company_id': self.company_id,
            'industry': self.industry,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ================= FOLLOWUP MODEL =================
class FollowUp(db.Model):

    __tablename__ = 'followups'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    lead_id = db.Column(
        db.Integer,
        db.ForeignKey('leads.id'),
        nullable=False
    )

    action_type = db.Column(
        db.String(100)
    )

    notes = db.Column(
        db.Text
    )

    next_followup_date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50),
        default='Pending'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'action_type': self.action_type,
            'notes': self.notes,
            'next_followup_date': self.next_followup_date,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }