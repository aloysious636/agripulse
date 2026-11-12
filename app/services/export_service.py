import csv
import io
from datetime import date
from typing import Tuple, List, Any
from app.models import (
    Animal, BreedingRecord, HealthRecord, RoutineTask,
    FeedingRecord, ProductionRecord, WeightRecord, FinancialTransaction
)
from app.services.notification_service import NotificationService

class ExportService:
    @staticmethod
    def fetch_report_data(report_type: str, start_date: date = None, end_date: date = None, species_id: int = None) -> Tuple[str, List[str], List[List[Any]]]:
        if report_type == 'animal_inventory':
            q = Animal.query
            if species_id:
                q = q.filter_by(species_id=species_id)
            rows = q.order_by(Animal.tag_number).all()
            headers = ['Tag Number', 'Name', 'Species', 'Breed', 'Sex', 'DOB', 'Weight (kg)', 'Category', 'Status']
            data = [[
                r.tag_number, r.name or '-', r.species_ref.name if r.species_ref else '-',
                r.breed, r.sex, r.dob.isoformat(), r.current_weight or 0, r.production_category, r.status
            ] for r in rows]
            return "Livestock Inventory & Registration Report", headers, data

        elif report_type == 'breeding':
            q = BreedingRecord.query
            if start_date:
                q = q.filter(BreedingRecord.service_date >= start_date)
            if end_date:
                q = q.filter(BreedingRecord.service_date <= end_date)
            rows = q.order_by(BreedingRecord.service_date.desc()).all()
            headers = ['Animal Tag', 'Species', 'Heat Date', 'Service Date', 'Method', 'Sire', 'Pregnancy Status', 'Expected Delivery', 'Actual Delivery', 'Offspring']
            data = [[
                r.animal.tag_number if r.animal else '-',
                r.animal.species_ref.name if r.animal and r.animal.species_ref else '-',
                r.heat_date.isoformat() if r.heat_date else '-',
                r.service_date.isoformat() if r.service_date else '-',
                r.service_method, r.sire_tag or '-', r.pregnancy_status,
                r.expected_delivery_date.isoformat() if r.expected_delivery_date else '-',
                r.actual_delivery_date.isoformat() if r.actual_delivery_date else '-',
                r.offspring_count
            ] for r in rows]
            return "Breeding & Reproductive Performance Report", headers, data

        elif report_type == 'health':
            q = HealthRecord.query
            if start_date:
                q = q.filter(HealthRecord.event_date >= start_date)
            if end_date:
                q = q.filter(HealthRecord.event_date <= end_date)
            rows = q.order_by(HealthRecord.event_date.desc()).all()
            headers = ['Date', 'Animal Tag', 'Type', 'Condition/Vaccine', 'Medication', 'Dosage', 'Withdrawal End', 'Next Due', 'Status', 'Cost']
            data = [[
                r.event_date.isoformat(), r.animal.tag_number if r.animal else '-',
                r.record_type, r.disease_or_condition, r.medication or '-', r.dosage or '-',
                r.withdrawal_end_date.isoformat() if r.withdrawal_end_date else '-',
                r.next_due_date.isoformat() if r.next_due_date else '-',
                r.recovery_status, f"{r.cost:.2f}"
            ] for r in rows]
            return "Veterinary Health & Vaccination Report", headers, data

        elif report_type == 'feeding':
            q = FeedingRecord.query
            if start_date:
                q = q.filter(FeedingRecord.feeding_date >= start_date)
            if end_date:
                q = q.filter(FeedingRecord.feeding_date <= end_date)
            rows = q.order_by(FeedingRecord.feeding_date.desc()).all()
            headers = ['Date', 'Feed Item', 'Target Animal/Group', 'Head Count', 'Quantity (kg)', 'Total Cost']
            data = [[
                r.feeding_date.isoformat(), r.feed_item.feed_name if r.feed_item else '-',
                r.animal_ref.tag_number if r.animal_ref else (r.target_group or 'Herd'),
                r.animal_count, f"{r.quantity_kg:.2f}", f"{r.total_cost:.2f}"
            ] for r in rows]
            return "Nutrition & Feed Consumption Report", headers, data

        elif report_type == 'production':
            q = ProductionRecord.query
            if start_date:
                q = q.filter(ProductionRecord.record_date >= start_date)
            if end_date:
                q = q.filter(ProductionRecord.record_date <= end_date)
            rows = q.order_by(ProductionRecord.record_date.desc()).all()
            headers = ['Date', 'Animal/Flock', 'Production Type', 'Morning', 'Evening', 'Total Yield', 'Quality Notes']
            data = [[
                r.record_date.isoformat(),
                r.animal.tag_number if r.animal else (r.flock_or_group or 'Group'),
                r.production_type, r.morning_yield, r.evening_yield, f"{r.total_yield:.2f}",
                r.quality_notes or '-'
            ] for r in rows]
            return "Farm Production Summary Report", headers, data

        elif report_type == 'growth':
            q = WeightRecord.query
            if start_date:
                q = q.filter(WeightRecord.measurement_date >= start_date)
            if end_date:
                q = q.filter(WeightRecord.measurement_date <= end_date)
            rows = q.order_by(WeightRecord.measurement_date.desc()).all()
            headers = ['Date', 'Animal Tag', 'Previous Weight (kg)', 'Current Weight (kg)', 'Gain (kg)', 'ADG (kg/day)', 'BCS']
            data = [[
                r.measurement_date.isoformat(), r.animal.tag_number if r.animal else '-',
                r.previous_weight_kg if r.previous_weight_kg is not None else '-',
                r.weight_kg,
                r.weight_change_kg if r.weight_change_kg is not None else '-',
                r.adg_kg_per_day if r.adg_kg_per_day is not None else '-',
                r.body_condition_score or '-'
            ] for r in rows]
            return "Livestock Weight & Growth Performance Report", headers, data

        elif report_type == 'tasks':
            q = RoutineTask.query.order_by(RoutineTask.scheduled_date.asc()).all()
            headers = ['Scheduled Date', 'Activity', 'Animal/Group', 'Species', 'Priority', 'Status', 'Completed Date']
            data = [[
                r.scheduled_date.isoformat(), r.activity_name,
                r.animal.tag_number if r.animal else (r.target_group or 'Group'),
                r.species_name, r.priority, r.status,
                r.completion_date.isoformat() if r.completion_date else '-'
            ] for r in q]
            return "Routine Management Tasks & Overdue Activities Report", headers, data

        elif report_type == 'finance':
            q = FinancialTransaction.query
            if start_date:
                q = q.filter(FinancialTransaction.transaction_date >= start_date)
            if end_date:
                q = q.filter(FinancialTransaction.transaction_date <= end_date)
            rows = q.order_by(FinancialTransaction.transaction_date.desc()).all()
            headers = ['Date', 'Type', 'Category', 'Enterprise', 'Animal Tag', 'Amount', 'Description']
            data = [[
                r.transaction_date.isoformat(), r.transaction_type, r.category,
                r.enterprise, r.animal_tag or '-', f"{r.amount:.2f}", r.description or '-'
            ] for r in rows]
            return "Farm Financial Income & Expenditure Report", headers, data

        else:
            alerts = NotificationService.generate_active_alerts(include_resolved=False)
            headers = ['Severity', 'Category', 'Due Date', 'Animal Tag', 'Alert Title', 'Details']
            data = [[
                a['severity'], a['category'], a['due_date'], a['animal_tag'] or '-', a['title'], a['message']
            ] for a in alerts]
            return "Active Farm Alerts & Overdue Reminders Report", headers, data

    @staticmethod
    def generate_csv_string(headers: List[str], rows: List[List[Any]]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
        return output.getvalue()