import os
from datetime import datetime, date, timedelta
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app.models import (
    db, FarmSettings, Species, Breed, Animal, BreedingRecord,
    HealthRecord, RoutineTask, FeedInventory, FeedingRecord,
    ProductionRecord, WeightRecord, FinancialTransaction, NotificationReadState
)
from app.calculations.engine import CalculationEngine
from app.services.notification_service import NotificationService
from app.services.backup_service import BackupService

api_bp = Blueprint('api', __name__, url_prefix='/api')

def parse_date(val):
    if not val:
        return None
    if isinstance(val, date):
        return val
    return datetime.strptime(str(val)[:10], '%Y-%m-%d').date()

# --- DASHBOARD & ANALYTICS ---
@api_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    active_animals = Animal.query.filter_by(status='Active').all()
    total_active = len(active_animals)

    species_counts = {}
    sex_counts = {}
    category_counts = {}
    breed_counts = {}
    pregnant_count = 0

    for a in active_animals:
        sp_name = a.species_ref.name if a.species_ref else 'Other'
        species_counts[sp_name] = species_counts.get(sp_name, 0) + 1
        sex_counts[a.sex] = sex_counts.get(a.sex, 0) + 1
        category_counts[a.production_category] = category_counts.get(a.production_category, 0) + 1
        breed_counts[a.breed] = breed_counts.get(a.breed, 0) + 1
        if a.is_pregnant:
            pregnant_count += 1

    active_females = [a for a in active_animals if a.sex == 'Female']
    due_for_service = [a for a in active_females if not a.is_pregnant]

    expected_births = BreedingRecord.query.filter(
        BreedingRecord.pregnancy_status.in_(['Pending', 'Confirmed']),
        BreedingRecord.actual_delivery_date.is_(None),
        BreedingRecord.expected_delivery_date >= today
    ).count()

    overdue_tasks = RoutineTask.query.filter(
        RoutineTask.status == 'Pending',
        RoutineTask.scheduled_date < today
    ).count()
    upcoming_tasks = RoutineTask.query.filter(
        RoutineTask.status == 'Pending',
        RoutineTask.scheduled_date >= today,
        RoutineTask.scheduled_date <= today + timedelta(days=14)
    ).count()

    milk_30d = db.session.query(func.sum(ProductionRecord.total_yield)).filter(
        ProductionRecord.production_type == 'Milk',
        ProductionRecord.record_date >= thirty_days_ago
    ).scalar() or 0.0

    eggs_30d = db.session.query(func.sum(ProductionRecord.total_yield)).filter(
        ProductionRecord.production_type == 'Eggs',
        ProductionRecord.record_date >= thirty_days_ago
    ).scalar() or 0.0

    milk_trend = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        day_milk = db.session.query(func.sum(ProductionRecord.total_yield)).filter(
            ProductionRecord.production_type == 'Milk',
            ProductionRecord.record_date == d
        ).scalar() or 0.0
        milk_trend.append({'date': d.strftime('%b %d'), 'yield': round(day_milk, 1)})

    total_income = db.session.query(func.sum(FinancialTransaction.amount)).filter_by(transaction_type='Income').scalar() or 0.0
    total_expense = db.session.query(func.sum(FinancialTransaction.amount)).filter_by(transaction_type='Expense').scalar() or 0.0

    expense_by_cat_rows = db.session.query(
        FinancialTransaction.category, func.sum(FinancialTransaction.amount)
    ).filter_by(transaction_type='Expense').group_by(FinancialTransaction.category).all()
    expense_by_category = {r[0]: round(r[1], 2) for r in expense_by_cat_rows}

    recent_health = [h.to_dict() for h in HealthRecord.query.order_by(HealthRecord.event_date.desc()).limit(5).all()]
    recent_tx = [t.to_dict() for t in FinancialTransaction.query.order_by(FinancialTransaction.transaction_date.desc()).limit(5).all()]
    alerts = NotificationService.generate_active_alerts(include_resolved=False)

    return jsonify({
        'kpis': {
            'total_animals': total_active,
            'active_breeding_females': len(active_females),
            'pregnant_animals': pregnant_count,
            'due_for_service': len(due_for_service),
            'expected_births': expected_births,
            'upcoming_tasks': upcoming_tasks,
            'overdue_tasks': overdue_tasks,
            'milk_30d': round(milk_30d, 1),
            'eggs_30d': int(eggs_30d),
            'total_income': round(total_income, 2),
            'total_expense': round(total_expense, 2),
            'net_balance': round(total_income - total_expense, 2),
            'active_alerts_count': len(alerts)
        },
        'distributions': {
            'by_species': species_counts,
            'by_sex': sex_counts,
            'by_category': category_counts,
            'by_breed': breed_counts,
            'expense_by_category': expense_by_category
        },
        'milk_trend': milk_trend,
        'recent_health': recent_health,
        'recent_transactions': recent_tx,
        'top_alerts': alerts[:8]
    })

# --- SPECIES & SETTINGS ---
@api_bp.route('/species', methods=['GET', 'POST'])
def handle_species():
    if request.method == 'GET':
        species = Species.query.order_by(Species.name).all()
        return jsonify([s.to_dict() for s in species])

    data = request.json or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Species name is required'}), 400
    if Species.query.filter(func.lower(Species.name) == name.lower()).first():
        return jsonify({'error': 'Species already exists'}), 400

    sp = Species(
        name=name,
        gestation_days=int(data.get('gestation_days', 150)),
        estrous_cycle_days=int(data.get('estrous_cycle_days', 21)),
        pregnancy_check_days=int(data.get('pregnancy_check_days', 35)),
        weaning_days=int(data.get('weaning_days', 60)),
        puberty_months=int(data.get('puberty_months', 8)),
        dmi_pct_body_weight=float(data.get('dmi_pct_body_weight', 3.0)),
        default_production_system=data.get('default_production_system', 'Meat')
    )
    db.session.add(sp)
    db.session.commit()
    return jsonify(sp.to_dict()), 201

@api_bp.route('/species/<int:species_id>', methods=['PUT'])
def update_species(species_id):
    sp = db.session.get(Species, species_id)
    if not sp:
        return jsonify({'error': 'Species not found'}), 404
    data = request.json or {}
    sp.gestation_days = int(data.get('gestation_days', sp.gestation_days))
    sp.estrous_cycle_days = int(data.get('estrous_cycle_days', sp.estrous_cycle_days))
    sp.pregnancy_check_days = int(data.get('pregnancy_check_days', sp.pregnancy_check_days))
    sp.weaning_days = int(data.get('weaning_days', sp.weaning_days))
    sp.puberty_months = int(data.get('puberty_months', sp.puberty_months))
    sp.dmi_pct_body_weight = float(data.get('dmi_pct_body_weight', sp.dmi_pct_body_weight))
    sp.default_production_system = data.get('default_production_system', sp.default_production_system)
    db.session.commit()
    return jsonify(sp.to_dict())

@api_bp.route('/settings', methods=['GET', 'PUT'])
def handle_settings():
    settings = FarmSettings.query.first()
    if request.method == 'GET':
        return jsonify(settings.to_dict() if settings else {})

    data = request.json or {}
    if not settings:
        settings = FarmSettings()
        db.session.add(settings)

    settings.farm_name = data.get('farm_name', settings.farm_name)
    settings.location = data.get('location', settings.location)
    settings.owner_name = data.get('owner_name', settings.owner_name)
    settings.currency = data.get('currency', settings.currency)
    settings.weight_unit = data.get('weight_unit', settings.weight_unit)
    settings.milk_unit = data.get('milk_unit', settings.milk_unit)
    settings.lead_alert_days = int(data.get('lead_alert_days', settings.lead_alert_days))
    db.session.commit()
    return jsonify(settings.to_dict())

# --- MODULE 2: ANIMAL MANAGEMENT ---
@api_bp.route('/animals', methods=['GET', 'POST'])
def handle_animals():
    if request.method == 'GET':
        q = Animal.query
        search = request.args.get('search', '').strip()
        species_id = request.args.get('species_id', type=int)
        status = request.args.get('status', '')
        sex = request.args.get('sex', '')
        category = request.args.get('category', '')

        if search:
            like_str = f"%{search}%"
            q = q.filter(db.or_(Animal.tag_number.ilike(like_str), Animal.name.ilike(like_str), Animal.breed.ilike(like_str)))
        if species_id:
            q = q.filter_by(species_id=species_id)
        if status:
            q = q.filter_by(status=status)
        if sex:
            q = q.filter_by(sex=sex)
        if category:
            q = q.filter_by(production_category=category)

        animals = q.order_by(Animal.tag_number.asc()).all()
        result = []
        for a in animals:
            d = a.to_dict()
            d['age_info'] = CalculationEngine.calculate_age(a.dob)
            result.append(d)
        return jsonify(result)

    data = request.form if request.form else (request.json or {})
    tag_number = (data.get('tag_number') or '').strip().upper()
    if not tag_number:
        return jsonify({'error': 'Ear Tag / ID number is required.'}), 400

    existing = Animal.query.filter(func.upper(Animal.tag_number) == tag_number).first()
    if existing:
        return jsonify({'error': f'Duplicate Identification Number: {tag_number} is already registered.'}), 400

    dob = parse_date(data.get('dob'))
    if not dob or dob > date.today():
        return jsonify({'error': 'Valid Date of Birth (not in the future) is required.'}), 400

    species_id = int(data.get('species_id'))
    birth_wt = float(data['birth_weight']) if data.get('birth_weight') not in (None, '') else None
    curr_wt = float(data['current_weight']) if data.get('current_weight') not in (None, '') else birth_wt

    photo_filename = None
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename:
            safe_name = secure_filename(f"{tag_number}_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name))
            photo_filename = f"/uploads/{safe_name}"

    animal = Animal(
        tag_number=tag_number,
        name=(data.get('name') or '').strip(),
        species_id=species_id,
        breed=(data.get('breed') or 'Crossbreed').strip(),
        sex=data.get('sex', 'Female'),
        dob=dob,
        acquisition_date=parse_date(data.get('acquisition_date')) or date.today(),
        acquisition_source=data.get('acquisition_source', 'Born on Farm'),
        dam_tag=(data.get('dam_tag') or '').strip().upper(),
        sire_tag=(data.get('sire_tag') or '').strip().upper(),
        birth_weight=birth_wt,
        current_weight=curr_wt,
        production_category=data.get('production_category', 'Dairy'),
        status=data.get('status', 'Active'),
        is_pregnant=str(data.get('is_pregnant', 'false')).lower() in ('true', '1', 'yes'),
        photo_path=photo_filename,
        notes=data.get('notes', '')
    )
    db.session.add(animal)
    db.session.flush()

    if curr_wt and curr_wt > 0:
        w_rec = WeightRecord(
            animal_id=animal.id,
            measurement_date=dob if birth_wt == curr_wt else date.today(),
            weight_kg=curr_wt,
            previous_weight_kg=None,
            weight_change_kg=0.0,
            adg_kg_per_day=0.0,
            notes='Initial registration weight'
        )
        db.session.add(w_rec)

    db.session.commit()
    res = animal.to_dict()
    res['age_info'] = CalculationEngine.calculate_age(animal.dob)
    return jsonify(res), 201

@api_bp.route('/animals/<int:animal_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_animal(animal_id):
    animal = db.session.get(Animal, animal_id)
    if not animal:
        return jsonify({'error': 'Animal not found.'}), 404

    if request.method == 'GET':
        profile = animal.to_dict()
        profile['age_info'] = CalculationEngine.calculate_age(animal.dob)
        profile['breedings'] = [b.to_dict() for b in animal.breedings]
        profile['health_records'] = [h.to_dict() for h in animal.health_records]
        profile['routine_tasks'] = [t.to_dict() for t in animal.routine_tasks]
        profile['production_records'] = [p.to_dict() for p in animal.production_records]
        profile['weight_records'] = [w.to_dict() for w in sorted(animal.weight_records, key=lambda x: x.measurement_date)]
        feeding = FeedingRecord.query.filter_by(animal_id=animal.id).order_by(FeedingRecord.feeding_date.desc()).all()
        profile['feeding_records'] = [f.to_dict() for f in feeding]
        return jsonify(profile)

    if request.method == 'PUT':
        data = request.json or {}
        if 'tag_number' in data:
            new_tag = data['tag_number'].strip().upper()
            dup = Animal.query.filter(func.upper(Animal.tag_number) == new_tag, Animal.id != animal.id).first()
            if dup:
                return jsonify({'error': f'Tag {new_tag} already belongs to another animal.'}), 400
            animal.tag_number = new_tag

        animal.name = data.get('name', animal.name)
        if data.get('species_id'):
            animal.species_id = int(data['species_id'])
        animal.breed = data.get('breed', animal.breed)
        animal.sex = data.get('sex', animal.sex)
        if data.get('dob'):
            animal.dob = parse_date(data['dob'])
        animal.dam_tag = data.get('dam_tag', animal.dam_tag)
        animal.sire_tag = data.get('sire_tag', animal.sire_tag)
        animal.production_category = data.get('production_category', animal.production_category)
        animal.status = data.get('status', animal.status)
        if 'is_pregnant' in data:
            animal.is_pregnant = bool(data['is_pregnant'])
        animal.notes = data.get('notes', animal.notes)
        db.session.commit()
        return jsonify(animal.to_dict())

    if request.method == 'DELETE':
        mode = request.args.get('mode', 'archive')
        if mode == 'hard':
            db.session.delete(animal)
            db.session.commit()
            return jsonify({'message': 'Animal permanently deleted.'})
        else:
            animal.status = 'Archived'
            db.session.commit()
            return jsonify({'message': 'Animal archived safely.', 'animal': animal.to_dict()})

# --- MODULE 3: BREEDING & REPRODUCTION ---
@api_bp.route('/breeding', methods=['GET', 'POST'])
def handle_breeding():
    if request.method == 'GET':
        records = BreedingRecord.query.order_by(BreedingRecord.created_at.desc()).all()
        result = []
        for r in records:
            d = r.to_dict()
            if r.expected_delivery_date and not r.actual_delivery_date:
                d['days_remaining'] = (r.expected_delivery_date - date.today()).days
            else:
                d['days_remaining'] = None
            result.append(d)
        return jsonify(result)

    data = request.json or {}
    animal_id = int(data.get('animal_id', 0))
    animal = db.session.get(Animal, animal_id)
    if not animal:
        return jsonify({'error': 'Valid female animal is required.'}), 400

    sp = animal.species_ref
    heat_date = parse_date(data.get('heat_date'))
    service_date = parse_date(data.get('service_date'))

    calc = CalculationEngine.calculate_reproductive_dates(
        heat_date=heat_date,
        service_date=service_date,
        gestation_days=sp.gestation_days if sp else 283,
        estrous_cycle_days=sp.estrous_cycle_days if sp else 21,
        preg_check_days=sp.pregnancy_check_days if sp else 35
    )

    preg_status = data.get('pregnancy_status', 'Pending')
    actual_delivery = parse_date(data.get('actual_delivery_date'))
    if actual_delivery:
        preg_status = 'Delivered'

    rec = BreedingRecord(
        animal_id=animal.id,
        heat_date=heat_date,
        service_date=service_date,
        service_method=data.get('service_method', 'Artificial Insemination'),
        sire_tag=data.get('sire_tag', ''),
        expected_next_heat=calc['expected_next_heat'],
        preg_check_date=calc['preg_check_date'],
        pregnancy_status=preg_status,
        expected_delivery_date=calc['expected_delivery_date'],
        actual_delivery_date=actual_delivery,
        birth_outcome=data.get('birth_outcome', ''),
        offspring_count=int(data.get('offspring_count', 0) or 0),
        notes=data.get('notes', '')
    )

    if preg_status == 'Confirmed':
        animal.is_pregnant = True
    elif preg_status in ('Delivered', 'Open', 'Aborted'):
        animal.is_pregnant = False

    db.session.add(rec)
    db.session.commit()
    res = rec.to_dict()
    res['days_remaining'] = calc['days_remaining']
    return jsonify(res), 201

@api_bp.route('/breeding/<int:record_id>', methods=['PUT'])
def update_breeding(record_id):
    rec = db.session.get(BreedingRecord, record_id)
    if not rec:
        return jsonify({'error': 'Breeding record not found'}), 404
    data = request.json or {}
    if 'pregnancy_status' in data:
        rec.pregnancy_status = data['pregnancy_status']
    if data.get('actual_delivery_date'):
        rec.actual_delivery_date = parse_date(data['actual_delivery_date'])
        rec.pregnancy_status = 'Delivered'
    if 'birth_outcome' in data:
        rec.birth_outcome = data['birth_outcome']
    if 'offspring_count' in data:
        rec.offspring_count = int(data['offspring_count'] or 0)
    if 'notes' in data:
        rec.notes = data['notes']

    if rec.animal:
        if rec.pregnancy_status == 'Confirmed':
            rec.animal.is_pregnant = True
        elif rec.pregnancy_status in ('Delivered', 'Open', 'Aborted'):
            rec.animal.is_pregnant = False

    db.session.commit()
    return jsonify(rec.to_dict())

# --- MODULE 4: HEALTH MANAGEMENT ---
@api_bp.route('/health', methods=['GET', 'POST'])
def handle_health():
    if request.method == 'GET':
        records = HealthRecord.query.order_by(HealthRecord.event_date.desc()).all()
        return jsonify([r.to_dict() for r in records])

    data = request.json or {}
    animal_id = int(data.get('animal_id', 0))
    animal = db.session.get(Animal, animal_id)
    if not animal:
        return jsonify({'error': 'Animal not found.'}), 404

    event_date = parse_date(data.get('event_date')) or date.today()
    withdrawal_days = int(data.get('withdrawal_days', 0) or 0)
    withdrawal_end = event_date + timedelta(days=withdrawal_days) if withdrawal_days > 0 else None
    next_due = parse_date(data.get('next_due_date'))
    cost = float(data.get('cost', 0.0) or 0.0)
    rec_type = data.get('record_type', 'Treatment')
    recovery_status = data.get('recovery_status', 'Under Observation')

    rec = HealthRecord(
        animal_id=animal.id,
        record_type=rec_type,
        event_date=event_date,
        disease_or_condition=data.get('disease_or_condition', 'General Exam'),
        symptoms=data.get('symptoms', ''),
        diagnosis=data.get('diagnosis', ''),
        medication=data.get('medication', ''),
        dosage=data.get('dosage', ''),
        withdrawal_days=withdrawal_days,
        withdrawal_end_date=withdrawal_end,
        next_due_date=next_due,
        veterinarian=data.get('veterinarian', ''),
        recovery_status=recovery_status,
        cost=cost,
        notes=data.get('notes', '')
    )
    db.session.add(rec)

    if rec_type == 'Mortality' or recovery_status == 'Deceased':
        animal.status = 'Deceased'
        animal.is_pregnant = False

    if cost > 0:
        tx = FinancialTransaction(
            transaction_date=event_date,
            transaction_type='Expense',
            category='Veterinary & Medication',
            enterprise=animal.production_category,
            amount=cost,
            animal_tag=animal.tag_number,
            description=f"{rec_type}: {rec.disease_or_condition} ({animal.tag_number})"
        )
        db.session.add(tx)

    db.session.commit()
    return jsonify(rec.to_dict()), 201

# --- MODULE 5: ROUTINE MANAGEMENT ---
@api_bp.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = RoutineTask.query.order_by(RoutineTask.scheduled_date.asc()).all()
        return jsonify([t.to_dict() for t in tasks])

    data = request.json or {}
    animal_id = int(data['animal_id']) if data.get('animal_id') else None
    animal = db.session.get(Animal, animal_id) if animal_id else None
    species_name = animal.species_ref.name if animal and animal.species_ref else data.get('species_name', 'Cattle')

    task = RoutineTask(
        activity_name=data.get('activity_name', 'Routine Inspection'),
        animal_id=animal_id,
        target_group=data.get('target_group', ''),
        species_name=species_name,
        scheduled_date=parse_date(data.get('scheduled_date')) or date.today(),
        status=data.get('status', 'Pending'),
        priority=data.get('priority', 'Medium'),
        notes=data.get('notes', '')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.session.get(RoutineTask, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.json or {}
    if 'status' in data:
        task.status = data['status']
        if task.status == 'Completed':
            task.completion_date = date.today()
    if data.get('scheduled_date'):
        task.scheduled_date = parse_date(data['scheduled_date'])
    if 'priority' in data:
        task.priority = data['priority']
    if 'notes' in data:
        task.notes = data['notes']
    db.session.commit()
    return jsonify(task.to_dict())

# --- MODULE 6: NUTRITION & FEEDING ---
@api_bp.route('/feeds', methods=['GET', 'POST'])
def handle_feeds():
    if request.method == 'GET':
        feeds = FeedInventory.query.order_by(FeedInventory.feed_name).all()
        return jsonify([f.to_dict() for f in feeds])

    data = request.json or {}
    feed_name = (data.get('feed_name') or '').strip()
    if not feed_name:
        return jsonify({'error': 'Feed name is required'}), 400

    feed = FeedInventory.query.filter(func.lower(FeedInventory.feed_name) == feed_name.lower()).first()
    qty = float(data.get('quantity_kg', 0.0) or 0.0)
    unit_cost = float(data.get('unit_cost_per_kg', 0.0) or 0.0)

    if feed:
        feed.quantity_kg += qty
        if unit_cost > 0:
            feed.unit_cost_per_kg = unit_cost
    else:
        feed = FeedInventory(
            feed_name=feed_name,
            category=data.get('category', 'Concentrate'),
            quantity_kg=qty,
            reorder_level_kg=float(data.get('reorder_level_kg', 50.0) or 50.0),
            unit_cost_per_kg=unit_cost,
            dry_matter_pct=float(data.get('dry_matter_pct', 88.0) or 88.0),
            crude_protein_pct=float(data.get('crude_protein_pct', 16.0) or 16.0),
            metabolizable_energy_mj=float(data.get('metabolizable_energy_mj', 11.0) or 11.0)
        )
        db.session.add(feed)

    if qty > 0 and unit_cost > 0 and data.get('record_expense', True):
        tx = FinancialTransaction(
            transaction_date=date.today(),
            transaction_type='Expense',
            category='Feed Expenditure',
            enterprise='General Farm',
            amount=round(qty * unit_cost, 2),
            description=f"Purchased {qty} kg of {feed_name}"
        )
        db.session.add(tx)

    db.session.commit()
    return jsonify(feed.to_dict()), 201

@api_bp.route('/feeding-records', methods=['GET', 'POST'])
def handle_feeding_records():
    if request.method == 'GET':
        records = FeedingRecord.query.order_by(FeedingRecord.feeding_date.desc()).all()
        result = []
        for r in records:
            d = r.to_dict()
            if r.feed_item:
                avg_wt = r.animal_ref.current_weight if r.animal_ref else None
                d['nutrition'] = CalculationEngine.calculate_nutrition_metrics(
                    quantity_fed_kg=r.quantity_kg,
                    animal_count=r.animal_count,
                    dm_pct=r.feed_item.dry_matter_pct,
                    cp_pct=r.feed_item.crude_protein_pct,
                    me_mj_per_kg_dm=r.feed_item.metabolizable_energy_mj,
                    avg_animal_weight_kg=avg_wt
                )
            result.append(d)
        return jsonify(result)

    data = request.json or {}
    feed_id = int(data.get('feed_id', 0))
    feed = db.session.get(FeedInventory, feed_id)
    if not feed:
        return jsonify({'error': 'Feed item not found in inventory.'}), 404

    qty_kg = float(data.get('quantity_kg', 0.0) or 0.0)
    if qty_kg <= 0:
        return jsonify({'error': 'Quantity fed must be greater than zero.'}), 400
    if feed.quantity_kg < qty_kg:
        return jsonify({'error': f'Insufficient stock for {feed.feed_name}. Available: {round(feed.quantity_kg, 2)} kg.'}), 400

    animal_id = int(data['animal_id']) if data.get('animal_id') else None
    animal_count = int(data.get('animal_count', 1) or 1)
    total_cost = round(qty_kg * feed.unit_cost_per_kg, 2)

    feed.quantity_kg = round(feed.quantity_kg - qty_kg, 3)

    rec = FeedingRecord(
        feed_id=feed.id,
        feeding_date=parse_date(data.get('feeding_date')) or date.today(),
        animal_id=animal_id,
        target_group=data.get('target_group', ''),
        animal_count=animal_count,
        quantity_kg=qty_kg,
        total_cost=total_cost,
        notes=data.get('notes', '')
    )
    db.session.add(rec)
    db.session.commit()

    res = rec.to_dict()
    res['nutrition'] = CalculationEngine.calculate_nutrition_metrics(
        quantity_fed_kg=qty_kg,
        animal_count=animal_count,
        dm_pct=feed.dry_matter_pct,
        cp_pct=feed.crude_protein_pct,
        me_mj_per_kg_dm=feed.metabolizable_energy_mj
    )
    return jsonify(res), 201

# --- MODULE 7: PRODUCTION MANAGEMENT ---
@api_bp.route('/production', methods=['GET', 'POST'])
def handle_production():
    if request.method == 'GET':
        prod_type = request.args.get('type')
        q = ProductionRecord.query
        if prod_type:
            q = q.filter_by(production_type=prod_type)
        records = q.order_by(ProductionRecord.record_date.desc()).all()
        result = []
        for r in records:
            d = r.to_dict()
            if r.production_type == 'Eggs' and r.flock_size:
                d['laying_pct'] = CalculationEngine.calculate_hen_day_egg_percentage(r.total_yield, r.flock_size)
            elif r.production_type == 'Meat/Carcass' and r.carcass_weight and r.live_slaughter_weight:
                d['dressing_pct'] = CalculationEngine.calculate_dressing_percentage(r.carcass_weight, r.live_slaughter_weight)
            result.append(d)
        return jsonify(result)

    data = request.json or {}
    prod_type = data.get('production_type', 'Milk')
    morning = float(data.get('morning_yield', 0.0) or 0.0)
    evening = float(data.get('evening_yield', 0.0) or 0.0)
    total = float(data.get('total_yield', 0.0) or 0.0)
    if prod_type == 'Milk' and (morning > 0 or evening > 0):
        total = round(morning + evening, 2)

    animal_id = int(data['animal_id']) if data.get('animal_id') else None
    flock_size = int(data['flock_size']) if data.get('flock_size') else None
    carcass_wt = float(data['carcass_weight']) if data.get('carcass_weight') else None
    live_wt = float(data['live_slaughter_weight']) if data.get('live_slaughter_weight') else None

    rec = ProductionRecord(
        animal_id=animal_id,
        flock_or_group=data.get('flock_or_group', ''),
        production_type=prod_type,
        record_date=parse_date(data.get('record_date')) or date.today(),
        morning_yield=morning,
        evening_yield=evening,
        total_yield=total,
        flock_size=flock_size,
        damaged_or_rejected=float(data.get('damaged_or_rejected', 0.0) or 0.0),
        carcass_weight=carcass_wt,
        live_slaughter_weight=live_wt,
        quality_notes=data.get('quality_notes', '')
    )
    db.session.add(rec)
    db.session.commit()
    return jsonify(rec.to_dict()), 201

# --- MODULE 8: GROWTH & WEIGHT MONITORING ---
@api_bp.route('/weights', methods=['GET', 'POST'])
def handle_weights():
    if request.method == 'GET':
        animal_id = request.args.get('animal_id', type=int)
        q = WeightRecord.query
        if animal_id:
            q = q.filter_by(animal_id=animal_id)
        records = q.order_by(WeightRecord.measurement_date.desc(), WeightRecord.id.desc()).all()
        return jsonify([r.to_dict() for r in records])

    data = request.json or {}
    animal_id = int(data.get('animal_id', 0))
    animal = db.session.get(Animal, animal_id)
    if not animal:
        return jsonify({'error': 'Animal not found.'}), 404

    m_date = parse_date(data.get('measurement_date')) or date.today()
    weight_kg = float(data.get('weight_kg', 0.0) or 0.0)
    if weight_kg <= 0:
        return jsonify({'error': 'Weight must be a positive number.'}), 400

    prev_rec = WeightRecord.query.filter(
        WeightRecord.animal_id == animal.id,
        WeightRecord.measurement_date <= m_date
    ).order_by(WeightRecord.measurement_date.desc(), WeightRecord.id.desc()).first()

    prev_wt = prev_rec.weight_kg if prev_rec else animal.birth_weight
    prev_date = prev_rec.measurement_date if prev_rec else animal.dob

    adg_metrics = CalculationEngine.calculate_adg(prev_wt, prev_date, weight_kg, m_date)

    rec = WeightRecord(
        animal_id=animal.id,
        measurement_date=m_date,
        weight_kg=weight_kg,
        previous_weight_kg=prev_wt,
        weight_change_kg=adg_metrics['weight_change'],
        adg_kg_per_day=adg_metrics['adg'],
        body_condition_score=float(data['body_condition_score']) if data.get('body_condition_score') else None,
        notes=data.get('notes', '')
    )
    animal.current_weight = weight_kg
    db.session.add(rec)
    db.session.commit()
    return jsonify(rec.to_dict()), 201

# --- MODULE 9: FARM CALENDAR ---
@api_bp.route('/calendar', methods=['GET'])
def get_calendar_events():
    events = []
    for b in BreedingRecord.query.all():
        tag = b.animal.tag_number if b.animal else ''
        if b.expected_next_heat and b.pregnancy_status in ('Pending', 'Open'):
            events.append({
                'date': b.expected_next_heat.isoformat(),
                'type': 'Heat Watch',
                'title': f"Expected Heat: {tag}",
                'animal_id': b.animal_id,
                'tag_number': tag,
                'color': '#d97706'
            })
        if b.preg_check_date and b.pregnancy_status == 'Pending':
            events.append({
                'date': b.preg_check_date.isoformat(),
                'type': 'Pregnancy Check',
                'title': f"Preg Exam: {tag}",
                'animal_id': b.animal_id,
                'tag_number': tag,
                'color': '#2563eb'
            })
        if b.expected_delivery_date and not b.actual_delivery_date:
            events.append({
                'date': b.expected_delivery_date.isoformat(),
                'type': 'Expected Delivery',
                'title': f"Due to Deliver: {tag}",
                'animal_id': b.animal_id,
                'tag_number': tag,
                'color': '#dc2626'
            })

    for h in HealthRecord.query.filter(HealthRecord.next_due_date.isnot(None)).all():
        tag = h.animal.tag_number if h.animal else ''
        events.append({
            'date': h.next_due_date.isoformat(),
            'type': h.record_type,
            'title': f"{h.record_type}: {tag} ({h.disease_or_condition})",
            'animal_id': h.animal_id,
            'tag_number': tag,
            'color': '#059669'
        })

    for t in RoutineTask.query.filter_by(status='Pending').all():
        tag = t.animal.tag_number if t.animal else (t.target_group or t.species_name)
        events.append({
            'date': t.scheduled_date.isoformat(),
            'type': 'Routine Task',
            'title': f"{t.activity_name} ({tag})",
            'animal_id': t.animal_id,
            'tag_number': tag,
            'color': '#7c3aed'
        })

    events.sort(key=lambda e: e['date'])
    return jsonify(events)

# --- MODULE 10: NOTIFICATIONS ---
@api_bp.route('/notifications', methods=['GET'])
def get_notifications():
    include_res = request.args.get('include_resolved', 'false').lower() == 'true'
    return jsonify(NotificationService.generate_active_alerts(include_resolved=include_res))

@api_bp.route('/notifications/resolve', methods=['POST'])
def resolve_notification():
    data = request.json or {}
    key = data.get('alert_key')
    if not key:
        return jsonify({'error': 'alert_key required'}), 400
    state = NotificationReadState.query.filter_by(alert_key=key).first()
    if not state:
        state = NotificationReadState(alert_key=key, is_resolved=True)
        db.session.add(state)
    else:
        state.is_resolved = True
    db.session.commit()
    return jsonify({'status': 'resolved', 'alert_key': key})

# --- MODULE 11: FARM FINANCIAL MANAGEMENT ---
@api_bp.route('/finance', methods=['GET', 'POST'])
def handle_finance():
    if request.method == 'GET':
        tx_type = request.args.get('type')
        category = request.args.get('category')
        start_date = parse_date(request.args.get('start_date'))
        end_date = parse_date(request.args.get('end_date'))

        q = FinancialTransaction.query
        if tx_type:
            q = q.filter_by(transaction_type=tx_type)
        if category:
            q = q.filter_by(category=category)
        if start_date:
            q = q.filter(FinancialTransaction.transaction_date >= start_date)
        if end_date:
            q = q.filter(FinancialTransaction.transaction_date <= end_date)

        txs = q.order_by(FinancialTransaction.transaction_date.desc()).all()
        income = sum(t.amount for t in txs if t.transaction_type == 'Income')
        expense = sum(t.amount for t in txs if t.transaction_type == 'Expense')

        by_cat = {}
        by_ent = {}
        for t in txs:
            if t.transaction_type == 'Expense':
                by_cat[t.category] = round(by_cat.get(t.category, 0.0) + t.amount, 2)
            else:
                by_ent[t.enterprise] = round(by_ent.get(t.enterprise, 0.0) + t.amount, 2)

        return jsonify({
            'transactions': [t.to_dict() for t in txs],
            'summary': {
                'total_income': round(income, 2),
                'total_expense': round(expense, 2),
                'net_balance': round(income - expense, 2),
                'expense_by_category': by_cat,
                'income_by_enterprise': by_ent
            }
        })

    data = request.json or {}
    amount = float(data.get('amount', 0.0) or 0.0)
    if amount <= 0:
        return jsonify({'error': 'Transaction amount must be greater than zero.'}), 400

    tx = FinancialTransaction(
        transaction_date=parse_date(data.get('transaction_date')) or date.today(),
        transaction_type=data.get('transaction_type', 'Expense'),
        category=data.get('category', 'General Expense'),
        enterprise=data.get('enterprise', 'General Farm'),
        amount=amount,
        animal_tag=data.get('animal_tag', ''),
        payment_reference=data.get('payment_reference', ''),
        description=data.get('description', '')
    )
    db.session.add(tx)
    db.session.commit()
    return jsonify(tx.to_dict()), 201

# --- BACKUP & RESTORE ---
@api_bp.route('/backup', methods=['GET', 'POST'])
def handle_backups():
    if request.method == 'GET':
        return jsonify(BackupService.list_backups())
    info = BackupService.create_backup()
    return jsonify(info), 201

@api_bp.route('/backup/download/<path:filename>', methods=['GET'])
def download_backup(filename):
    safe = secure_filename(filename)
    path = Path(current_app.config['BACKUP_FOLDER']) / safe
    if not path.exists():
        return jsonify({'error': 'Backup file not found'}), 404
    return send_file(path, as_attachment=True)

@api_bp.route('/backup/restore', methods=['POST'])
def restore_backup():
    if 'backup_file' in request.files:
        f = request.files['backup_file']
        temp_path = Path(current_app.config['BACKUP_FOLDER']) / 'restore_upload_temp.db'
        f.save(temp_path)
        BackupService.restore_backup(temp_path)
        return jsonify({'message': 'Database successfully restored from uploaded file.'})

    data = request.json or {}
    filename = data.get('filename')
    if filename:
        path = Path(current_app.config['BACKUP_FOLDER']) / secure_filename(filename)
        BackupService.restore_backup(path)
        return jsonify({'message': f'Database restored from {filename}.'})

    return jsonify({'error': 'No backup file provided.'}), 400