from flask import Flask
from config import Config, RESOURCE_DIR
from app.models import db, Species, Breed, FarmSettings

def seed_reference_biological_parameters():
    """Seeds scientifically established species parameters and default KES farm settings if empty."""
    if not FarmSettings.query.first():
        db.session.add(FarmSettings(
            farm_name='AgriPulse Livestock Enterprise',
            location='Chuka, Tharaka-Nithi County, Kenya',
            owner_name='Farm Manager',
            currency='KES',
            weight_unit='kg',
            milk_unit='Liters'
        ))

    if Species.query.count() == 0:
        default_species = [
            ('Cattle', 283, 21, 35, 90, 15, 3.0, 'Dairy', ['Friesian', 'Ayrshire', 'Jersey', 'Boran', 'Sahiwal']),
            ('Dairy Goats', 150, 21, 30, 60, 7, 3.5, 'Dairy', ['Saanen', 'Toggenburg', 'Alpine', 'Norwegian']),
            ('Meat Goats', 150, 21, 30, 60, 7, 3.0, 'Meat', ['Boer', 'Galla', 'Small East African']),
            ('Sheep', 147, 17, 30, 60, 7, 3.0, 'Meat', ['Dorper', 'Red Maasai', 'Merino', 'Hampshire Down']),
            ('Pigs', 114, 21, 28, 35, 6, 4.0, 'Meat', ['Large White', 'Landrace', 'Duroc', 'Hampshire']),
            ('Poultry', 21, 1, 7, 28, 5, 8.0, 'Egg Production', ['Kuroiler', 'Kenbro', 'ISA Brown', 'Cobb 500', 'Indigenous Kienyeji']),
            ('Rabbits', 31, 14, 14, 35, 4, 5.0, 'Meat', ['New Zealand White', 'Californian', 'Flemish Giant', 'Chinchilla'])
        ]
        for name, gest, est, preg, wean, pub, dmi, sys_type, breeds in default_species:
            sp = Species(
                name=name,
                gestation_days=gest,
                estrous_cycle_days=est,
                pregnancy_check_days=preg,
                weaning_days=wean,
                puberty_months=pub,
                dmi_pct_body_weight=dmi,
                default_production_system=sys_type
            )
            db.session.add(sp)
            db.session.flush()
            for b_name in breeds:
                db.session.add(Breed(species_id=sp.id, name=b_name, purpose=sys_type))

    db.session.commit()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=str(RESOURCE_DIR / 'templates'),
        static_folder=str(RESOURCE_DIR / 'static')
    )
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.api_routes import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
        seed_reference_biological_parameters()

    return app
app = create_app()

