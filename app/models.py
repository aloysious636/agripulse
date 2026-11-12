from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FarmSettings(db.Model):
    __tablename__ = 'farm_settings'
    id = db.Column(db.Integer, primary_key=True)
    farm_name = db.Column(db.String(120), nullable=False, default='AgriPulse Livestock Enterprise')
    location = db.Column(db.String(150), default='Chuka, Tharaka-Nithi County, Kenya')
    owner_name = db.Column(db.String(100), default='Farm Manager')
    currency = db.Column(db.String(10), default='KES')
    weight_unit = db.Column(db.String(10), default='kg')
    milk_unit = db.Column(db.String(10), default='Liters')
    date_format = db.Column(db.String(20), default='YYYY-MM-DD')
    lead_alert_days = db.Column(db.Integer, default=7)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'farm_name': self.farm_name,
            'location': self.location,
            'owner_name': self.owner_name,
            'currency': self.currency,
            'weight_unit': self.weight_unit,
            'milk_unit': self.milk_unit,
            'date_format': self.date_format,
            'lead_alert_days': self.lead_alert_days
        }

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False, index=True)
    gestation_days = db.Column(db.Integer, nullable=False)
    estrous_cycle_days = db.Column(db.Integer, nullable=False)
    pregnancy_check_days = db.Column(db.Integer, nullable=False, default=35)
    weaning_days = db.Column(db.Integer, nullable=False)
    puberty_months = db.Column(db.Integer, nullable=False, default=8)
    dmi_pct_body_weight = db.Column(db.Float, nullable=False, default=3.0)
    default_production_system = db.Column(db.String(40), nullable=False)

    animals = db.relationship('Animal', backref='species_ref', lazy=True)
    breeds = db.relationship('Breed', backref='species_ref', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gestation_days': self.gestation_days,
            'estrous_cycle_days': self.estrous_cycle_days,
            'pregnancy_check_days': self.pregnancy_check_days,
            'weaning_days': self.weaning_days,
            'puberty_months': self.puberty_months,
            'dmi_pct_body_weight': self.dmi_pct_body_weight,
            'default_production_system': self.default_production_system
        }

class Breed(db.Model):
    __tablename__ = 'breeds'
    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    purpose = db.Column(db.String(50), default='Dual-Purpose')

    def to_dict(self):
        return {'id': self.id, 'species_id': self.species_id, 'name': self.name, 'purpose': self.purpose}

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    tag_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False, index=True)
    breed = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    acquisition_date = db.Column(db.Date, nullable=False, default=date.today)
    acquisition_source = db.Column(db.String(80), default='Born on Farm')
    dam_tag = db.Column(db.String(50), nullable=True)
    sire_tag = db.Column(db.String(50), nullable=True)
    birth_weight = db.Column(db.Float, nullable=True)
    current_weight = db.Column(db.Float, nullable=True)
    production_category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Active', index=True)
    is_pregnant = db.Column(db.Boolean, default=False)
    photo_path = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    breedings = db.relationship('BreedingRecord', backref='animal', cascade='all, delete-orphan', lazy=True)
    health_records = db.relationship('HealthRecord', backref='animal', cascade='all, delete-orphan', lazy=True)
    routine_tasks = db.relationship('RoutineTask', backref='animal', cascade='all, delete-orphan', lazy=True)
    production_records = db.relationship('ProductionRecord', backref='animal', cascade='all, delete-orphan', lazy=True)
    weight_records = db.relationship('WeightRecord', backref='animal', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tag_number': self.tag_number,
            'name': self.name or '',
            'species_id': self.species_id,
            'species_name': self.species_ref.name if self.species_ref else '',
            'breed': self.breed,
            'sex': self.sex,
            'dob': self.dob.isoformat() if self.dob else None,
            'acquisition_date': self.acquisition_date.isoformat() if self.acquisition_date else None,
            'acquisition_source': self.acquisition_source,
            'dam_tag': self.dam_tag or '',
            'sire_tag': self.sire_tag or '',
            'birth_weight': self.birth_weight,
            'current_weight': self.current_weight,
            'production_category': self.production_category,
            'status': self.status,
            'is_pregnant': self.is_pregnant,
            'photo_path': self.photo_path or '',
            'notes': self.notes or ''
        }

class BreedingRecord(db.Model):
    __tablename__ = 'breeding_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False, index=True)
    heat_date = db.Column(db.Date, nullable=True)
    service_date = db.Column(db.Date, nullable=True, index=True)
    service_method = db.Column(db.String(40), default='Artificial Insemination')
    sire_tag = db.Column(db.String(60), nullable=True)
    expected_next_heat = db.Column(db.Date, nullable=True)
    preg_check_date = db.Column(db.Date, nullable=True)
    pregnancy_status = db.Column(db.String(30), default='Pending')
    expected_delivery_date = db.Column(db.Date, nullable=True, index=True)
    actual_delivery_date = db.Column(db.Date, nullable=True)
    birth_outcome = db.Column(db.String(50), nullable=True)
    offspring_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'tag_number': self.animal.tag_number if self.animal else '',
            'animal_name': self.animal.name if self.animal else '',
            'species_name': self.animal.species_ref.name if self.animal and self.animal.species_ref else '',
            'heat_date': self.heat_date.isoformat() if self.heat_date else None,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'service_method': self.service_method,
            'sire_tag': self.sire_tag or '',
            'expected_next_heat': self.expected_next_heat.isoformat() if self.expected_next_heat else None,
            'preg_check_date': self.preg_check_date.isoformat() if self.preg_check_date else None,
            'pregnancy_status': self.pregnancy_status,
            'expected_delivery_date': self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            'actual_delivery_date': self.actual_delivery_date.isoformat() if self.actual_delivery_date else None,
            'birth_outcome': self.birth_outcome or '',
            'offspring_count': self.offspring_count,
            'notes': self.notes or ''
        }

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False, index=True)
    record_type = db.Column(db.String(40), nullable=False)
    event_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    disease_or_condition = db.Column(db.String(120), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.String(150), nullable=True)
    medication = db.Column(db.String(120), nullable=True)
    dosage = db.Column(db.String(80), nullable=True)
    withdrawal_days = db.Column(db.Integer, default=0)
    withdrawal_end_date = db.Column(db.Date, nullable=True)
    next_due_date = db.Column(db.Date, nullable=True, index=True)
    veterinarian = db.Column(db.String(100), nullable=True)
    recovery_status = db.Column(db.String(40), default='Under Observation')
    cost = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'tag_number': self.animal.tag_number if self.animal else '',
            'record_type': self.record_type,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'disease_or_condition': self.disease_or_condition,
            'symptoms': self.symptoms or '',
            'diagnosis': self.diagnosis or '',
            'medication': self.medication or '',
            'dosage': self.dosage or '',
            'withdrawal_days': self.withdrawal_days,
            'withdrawal_end_date': self.withdrawal_end_date.isoformat() if self.withdrawal_end_date else None,
            'next_due_date': self.next_due_date.isoformat() if self.next_due_date else None,
            'veterinarian': self.veterinarian or '',
            'recovery_status': self.recovery_status,
            'cost': self.cost,
            'notes': self.notes or ''
        }

class RoutineTask(db.Model):
    __tablename__ = 'routine_tasks'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(100), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=True, index=True)
    target_group = db.Column(db.String(80), nullable=True)
    species_name = db.Column(db.String(60), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False, index=True)
    completion_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), default='Pending', index=True)
    priority = db.Column(db.String(20), default='Medium')
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'activity_name': self.activity_name,
            'animal_id': self.animal_id,
            'tag_number': self.animal.tag_number if self.animal else (self.target_group or 'Group'),
            'target_group': self.target_group or '',
            'species_name': self.species_name,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'status': self.status,
            'priority': self.priority,
            'notes': self.notes or ''
        }

class FeedInventory(db.Model):
    __tablename__ = 'feed_inventory'
    id = db.Column(db.Integer, primary_key=True)
    feed_name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity_kg = db.Column(db.Float, nullable=False, default=0.0)
    reorder_level_kg = db.Column(db.Float, nullable=False, default=50.0)
    unit_cost_per_kg = db.Column(db.Float, nullable=False, default=0.0)
    dry_matter_pct = db.Column(db.Float, nullable=False, default=88.0)
    crude_protein_pct = db.Column(db.Float, nullable=False, default=14.0)
    metabolizable_energy_mj = db.Column(db.Float, nullable=False, default=10.5)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    feeding_logs = db.relationship('FeedingRecord', backref='feed_item', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'feed_name': self.feed_name,
            'category': self.category,
            'quantity_kg': round(self.quantity_kg, 2),
            'reorder_level_kg': self.reorder_level_kg,
            'unit_cost_per_kg': self.unit_cost_per_kg,
            'dry_matter_pct': self.dry_matter_pct,
            'crude_protein_pct': self.crude_protein_pct,
            'metabolizable_energy_mj': self.metabolizable_energy_mj
        }

class FeedingRecord(db.Model):
    __tablename__ = 'feeding_records'
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed_inventory.id'), nullable=False, index=True)
    feeding_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=True)
    target_group = db.Column(db.String(80), nullable=True)
    animal_count = db.Column(db.Integer, nullable=False, default=1)
    quantity_kg = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)

    animal_ref = db.relationship('Animal', foreign_keys=[animal_id])

    def to_dict(self):
        return {
            'id': self.id,
            'feed_id': self.feed_id,
            'feed_name': self.feed_item.feed_name if self.feed_item else '',
            'feeding_date': self.feeding_date.isoformat() if self.feeding_date else None,
            'animal_id': self.animal_id,
            'target': self.animal_ref.tag_number if self.animal_ref else (self.target_group or 'General Herd'),
            'animal_count': self.animal_count,
            'quantity_kg': round(self.quantity_kg, 2),
            'total_cost': round(self.total_cost, 2),
            'notes': self.notes or ''
        }

class ProductionRecord(db.Model):
    __tablename__ = 'production_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=True, index=True)
    flock_or_group = db.Column(db.String(80), nullable=True)
    production_type = db.Column(db.String(30), nullable=False, index=True)
    record_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    morning_yield = db.Column(db.Float, default=0.0)
    evening_yield = db.Column(db.Float, default=0.0)
    total_yield = db.Column(db.Float, nullable=False, default=0.0)
    flock_size = db.Column(db.Integer, nullable=True)
    damaged_or_rejected = db.Column(db.Float, default=0.0)
    carcass_weight = db.Column(db.Float, nullable=True)
    live_slaughter_weight = db.Column(db.Float, nullable=True)
    quality_notes = db.Column(db.String(150), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'tag_number': self.animal.tag_number if self.animal else (self.flock_or_group or 'Flock/Group'),
            'production_type': self.production_type,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'morning_yield': self.morning_yield,
            'evening_yield': self.evening_yield,
            'total_yield': round(self.total_yield, 2),
            'flock_size': self.flock_size,
            'damaged_or_rejected': self.damaged_or_rejected,
            'carcass_weight': self.carcass_weight,
            'live_slaughter_weight': self.live_slaughter_weight,
            'quality_notes': self.quality_notes or ''
        }

class WeightRecord(db.Model):
    __tablename__ = 'weight_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False, index=True)
    measurement_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    weight_kg = db.Column(db.Float, nullable=False)
    previous_weight_kg = db.Column(db.Float, nullable=True)
    weight_change_kg = db.Column(db.Float, nullable=True)
    adg_kg_per_day = db.Column(db.Float, nullable=True)
    body_condition_score = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(150), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'tag_number': self.animal.tag_number if self.animal else '',
            'animal_name': self.animal.name if self.animal else '',
            'measurement_date': self.measurement_date.isoformat() if self.measurement_date else None,
            'weight_kg': round(self.weight_kg, 2),
            'previous_weight_kg': round(self.previous_weight_kg, 2) if self.previous_weight_kg is not None else None,
            'weight_change_kg': round(self.weight_change_kg, 2) if self.weight_change_kg is not None else None,
            'adg_kg_per_day': round(self.adg_kg_per_day, 3) if self.adg_kg_per_day is not None else None,
            'body_condition_score': self.body_condition_score,
            'notes': self.notes or ''
        }

class FinancialTransaction(db.Model):
    __tablename__ = 'financial_transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    transaction_type = db.Column(db.String(20), nullable=False, index=True)
    category = db.Column(db.String(60), nullable=False, index=True)
    enterprise = db.Column(db.String(50), default='General Farm')
    amount = db.Column(db.Float, nullable=False)
    animal_tag = db.Column(db.String(50), nullable=True)
    payment_reference = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'enterprise': self.enterprise,
            'amount': round(self.amount, 2),
            'animal_tag': self.animal_tag or '',
            'payment_reference': self.payment_reference or '',
            'description': self.description or ''
        }

class NotificationReadState(db.Model):
    __tablename__ = 'notification_read_states'
    id = db.Column(db.Integer, primary_key=True)
    alert_key = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_resolved = db.Column(db.Boolean, default=True)
    resolved_at = db.Column(db.DateTime, default=datetime.utcnow)