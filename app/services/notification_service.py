from datetime import date, timedelta
from typing import List, Dict, Any
from app.models import (
    Animal, BreedingRecord, HealthRecord, RoutineTask,
    FeedInventory, NotificationReadState, FarmSettings
)

class NotificationService:
    @staticmethod
    def generate_active_alerts(include_resolved: bool = False) -> List[Dict[str, Any]]:
        today = date.today()
        settings = FarmSettings.query.first()
        lead_days = settings.lead_alert_days if settings else 7
        horizon = today + timedelta(days=lead_days)

        resolved_keys = {
            r.alert_key for r in NotificationReadState.query.filter_by(is_resolved=True).all()
        }

        alerts: List[Dict[str, Any]] = []

        def append_alert(key: str, severity: str, category: str, title: str, message: str, due_date: date, animal_tag: str = ''):
            is_res = key in resolved_keys
            if is_res and not include_resolved:
                return
            alerts.append({
                'alert_key': key,
                'severity': severity,
                'category': category,
                'title': title,
                'message': message,
                'due_date': due_date.isoformat() if due_date else today.isoformat(),
                'animal_tag': animal_tag,
                'is_resolved': is_res
            })

        # 1. Expected deliveries & pregnancy checks
        breedings = BreedingRecord.query.filter(
            BreedingRecord.pregnancy_status.in_(['Pending', 'Confirmed']),
            BreedingRecord.actual_delivery_date.is_(None)
        ).all()

        for b in breedings:
            tag = b.animal.tag_number if b.animal else f"ID-{b.animal_id}"
            if b.expected_delivery_date:
                days_left = (b.expected_delivery_date - today).days
                if days_left < 0:
                    append_alert(
                        f"birth_overdue_{b.id}", "Critical", "Breeding",
                        f"Overdue Delivery: {tag}",
                        f"Animal {tag} passed expected delivery date ({b.expected_delivery_date}) by {abs(days_left)} days.",
                        b.expected_delivery_date, tag
                    )
                elif days_left <= lead_days:
                    append_alert(
                        f"birth_due_{b.id}_{b.expected_delivery_date}", "High Priority", "Breeding",
                        f"Imminent Birth: {tag}",
                        f"Expected to deliver in {days_left} day(s) on {b.expected_delivery_date}. Prepare maternity pen.",
                        b.expected_delivery_date, tag
                    )

            if b.pregnancy_status == 'Pending' and b.preg_check_date:
                if b.preg_check_date <= horizon:
                    sev = "Overdue" if b.preg_check_date < today else "Upcoming"
                    append_alert(
                        f"preg_check_{b.id}", sev, "Breeding",
                        f"Pregnancy Check Required: {tag}",
                        f"Confirm pregnancy status for {tag} (serviced on {b.service_date}).",
                        b.preg_check_date, tag
                    )

        # 2. Scheduled Vaccinations, Deworming & Withdrawal Periods
        health_due = HealthRecord.query.filter(HealthRecord.next_due_date.isnot(None)).all()
        for h in health_due:
            tag = h.animal.tag_number if h.animal else ''
            if h.next_due_date < today:
                append_alert(
                    f"health_overdue_{h.id}_{h.next_due_date}", "Overdue", "Health",
                    f"Overdue {h.record_type}: {tag}",
                    f"{h.disease_or_condition} follow-up was due on {h.next_due_date}.",
                    h.next_due_date, tag
                )
            elif h.next_due_date <= horizon:
                append_alert(
                    f"health_upcoming_{h.id}_{h.next_due_date}", "High Priority", "Health",
                    f"Upcoming {h.record_type}: {tag}",
                    f"{h.disease_or_condition} scheduled for {h.next_due_date}.",
                    h.next_due_date, tag
                )

        active_withdrawals = HealthRecord.query.filter(
            HealthRecord.withdrawal_end_date.isnot(None),
            HealthRecord.withdrawal_end_date >= today
        ).all()
        for w in active_withdrawals:
            tag = w.animal.tag_number if w.animal else ''
            append_alert(
                f"withdrawal_{w.id}", "Critical", "Health",
                f"Active Drug Withdrawal: {tag}",
                f"Do not harvest milk/meat from {tag} treated with {w.medication} until after {w.withdrawal_end_date}.",
                w.withdrawal_end_date, tag
            )

        # 3. Routine Management Tasks
        pending_tasks = RoutineTask.query.filter_by(status='Pending').all()
        for t in pending_tasks:
            tag = t.animal.tag_number if t.animal else (t.target_group or t.species_name)
            if t.scheduled_date < today:
                append_alert(
                    f"task_overdue_{t.id}", "Overdue", "Management",
                    f"Overdue Task: {t.activity_name}",
                    f"Scheduled on {t.scheduled_date} for {tag}.",
                    t.scheduled_date, tag
                )
            elif t.scheduled_date <= horizon:
                sev = "High Priority" if t.priority == "High" else "Upcoming"
                append_alert(
                    f"task_upcoming_{t.id}", sev, "Management",
                    f"Upcoming Task: {t.activity_name}",
                    f"Scheduled for {t.scheduled_date} ({tag}).",
                    t.scheduled_date, tag
                )

        # 4. Low Feed Inventory
        feeds = FeedInventory.query.all()
        for f in feeds:
            if f.quantity_kg <= f.reorder_level_kg:
                sev = "Critical" if f.quantity_kg <= (f.reorder_level_kg * 0.25) else "High Priority"
                append_alert(
                    f"low_feed_{f.id}_{int(f.quantity_kg)}", sev, "Nutrition",
                    f"Low Feed Stock: {f.feed_name}",
                    f"Remaining stock is {round(f.quantity_kg, 1)} kg (Reorder threshold: {f.reorder_level_kg} kg).",
                    today, ''
                )

        # 5. Missing Critical Animal Records
        active_animals = Animal.query.filter_by(status='Active').all()
        for a in active_animals:
            if a.current_weight is None or a.current_weight <= 0:
                append_alert(
                    f"missing_weight_{a.id}", "Informational", "Animal Records",
                    f"Missing Weight: {a.tag_number}",
                    f"Active {a.species_ref.name if a.species_ref else 'animal'} ({a.tag_number}) has no recorded body weight.",
                    today, a.tag_number
                )

        severity_order = {'Critical': 0, 'Overdue': 1, 'High Priority': 2, 'Upcoming': 3, 'Informational': 4}
        alerts.sort(key=lambda x: (severity_order.get(x['severity'], 5), x['due_date']))
        return alerts