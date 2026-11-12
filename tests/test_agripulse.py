import pytest
from datetime import date, timedelta
from config import TestConfig
from app import create_app

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_database_and_species_initialization(client):
    res = client.get('/api/species')
    assert res.status_code == 200
    species = res.get_json()
    names = {s['name']: s for s in species}
    assert 'Cattle' in names and names['Cattle']['gestation_days'] == 283
    assert 'Pigs' in names and names['Pigs']['gestation_days'] == 114
    assert 'Dairy Goats' in names and names['Dairy Goats']['gestation_days'] == 150

def test_animal_registration_and_duplicate_tag_prevention(client):
    sp = client.get('/api/species').get_json()[0]
    payload = {
        'tag_number': 'KE-FR-101',
        'name': 'Baraka',
        'species_id': sp['id'],
        'breed': 'Friesian',
        'sex': 'Female',
        'dob': '2024-02-29',
        'birth_weight': 32.0,
        'current_weight': 380.0,
        'production_category': 'Dairy'
    }
    res1 = client.post('/api/animals', json=payload)
    assert res1.status_code == 201

    res_dup = client.post('/api/animals', json=payload)
    assert res_dup.status_code == 400
    assert 'Duplicate' in res_dup.get_json()['error']

def test_species_specific_breeding_calculations(client):
    species_list = {s['name']: s['id'] for s in client.get('/api/species').get_json()}

    cow = client.post('/api/animals', json={
        'tag_number': 'COW-01', 'species_id': species_list['Cattle'],
        'breed': 'Ayrshire', 'sex': 'Female', 'dob': '2023-01-10', 'production_category': 'Dairy'
    }).get_json()

    sow = client.post('/api/animals', json={
        'tag_number': 'SOW-01', 'species_id': species_list['Pigs'],
        'breed': 'Large White', 'sex': 'Female', 'dob': '2024-01-10', 'production_category': 'Breeding'
    }).get_json()

    service_dt = date(2026, 1, 1)
    b_cow = client.post('/api/breeding', json={
        'animal_id': cow['id'], 'service_date': service_dt.isoformat(), 'pregnancy_status': 'Confirmed'
    }).get_json()

    b_sow = client.post('/api/breeding', json={
        'animal_id': sow['id'], 'service_date': service_dt.isoformat(), 'pregnancy_status': 'Confirmed'
    }).get_json()

    assert b_cow['expected_delivery_date'] == (service_dt + timedelta(days=283)).isoformat()
    assert b_sow['expected_delivery_date'] == (service_dt + timedelta(days=114)).isoformat()

def test_weight_adg_and_nutrition_stock_deduction(client):
    sp_id = client.get('/api/species').get_json()[0]['id']
    steer = client.post('/api/animals', json={
        'tag_number': 'STEER-99', 'species_id': sp_id, 'breed': 'Boran',
        'sex': 'Castrated', 'dob': '2025-01-01', 'birth_weight': 28.0,
        'current_weight': 200.0, 'production_category': 'Meat'
    }).get_json()

    future_date = (date.today() + timedelta(days=50)).isoformat()
    w_res = client.post('/api/weights', json={
        'animal_id': steer['id'], 'measurement_date': future_date, 'weight_kg': 250.0
    }).get_json()
    assert w_res['weight_change_kg'] == 50.0
    assert w_res['adg_kg_per_day'] == 1.0

    feed = client.post('/api/feeds', json={
        'feed_name': 'High Yield Dairy Meal', 'category': 'Concentrate',
        'quantity_kg': 100.0, 'unit_cost_per_kg': 45.0,
        'dry_matter_pct': 90.0, 'crude_protein_pct': 18.0, 'metabolizable_energy_mj': 11.5
    }).get_json()

    log = client.post('/api/feeding-records', json={
        'feed_id': feed['id'], 'animal_id': steer['id'], 'animal_count': 1, 'quantity_kg': 10.0
    }).get_json()
    assert log['total_cost'] == 450.0
    assert log['nutrition']['dm_per_head_kg'] == 9.0

    updated_feeds = client.get('/api/feeds').get_json()
    assert updated_feeds[0]['quantity_kg'] == 90.0

def test_reports_csv_and_pdf_exports(client):
    csv_res = client.get('/reports/export?type=animal_inventory&format=csv')
    assert csv_res.status_code == 200
    assert 'text/csv' in csv_res.content_type

    pdf_res = client.get('/reports/export?type=finance&format=pdf')
    assert pdf_res.status_code == 200
    assert b'Print / Save as PDF' in pdf_res.data