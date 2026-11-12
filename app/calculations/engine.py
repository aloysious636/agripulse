from datetime import date, timedelta
from typing import Dict, Any, Optional

class CalculationEngine:
    """Pure, deterministic livestock calculation engine."""

    @staticmethod
    def calculate_age(dob: date, reference_date: Optional[date] = None) -> Dict[str, Any]:
        if not dob:
            return {'days': 0, 'months': 0, 'years': 0, 'display': 'Unknown'}
        ref = reference_date or date.today()
        if dob > ref:
            return {'days': 0, 'months': 0, 'years': 0, 'display': 'Invalid Future Date'}

        total_days = (ref - dob).days
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30

        parts = []
        if years > 0:
            parts.append(f"{years}y")
        if months > 0:
            parts.append(f"{months}m")
        if years == 0 and days >= 0:
            parts.append(f"{days}d")

        return {
            'total_days': total_days,
            'months_float': round(total_days / 30.4375, 1),
            'years': years,
            'months': months,
            'days': days,
            'display': " ".join(parts) if parts else "0d"
        }

    @staticmethod
    def calculate_reproductive_dates(
        heat_date: Optional[date],
        service_date: Optional[date],
        gestation_days: int,
        estrous_cycle_days: int,
        preg_check_days: int = 35,
        reference_date: Optional[date] = None
    ) -> Dict[str, Any]:
        ref = reference_date or date.today()
        base_heat = service_date or heat_date
        expected_next_heat = None
        if base_heat and estrous_cycle_days > 0:
            expected_next_heat = base_heat + timedelta(days=estrous_cycle_days)

        expected_delivery = None
        preg_check_date = None
        days_remaining = None

        if service_date and gestation_days > 0:
            expected_delivery = service_date + timedelta(days=gestation_days)
            preg_check_date = service_date + timedelta(days=preg_check_days)
            days_remaining = (expected_delivery - ref).days

        return {
            'expected_next_heat': expected_next_heat,
            'preg_check_date': preg_check_date,
            'expected_delivery_date': expected_delivery,
            'days_remaining': days_remaining
        }

    @staticmethod
    def calculate_adg(
        prev_weight: float,
        prev_date: date,
        curr_weight: float,
        curr_date: date
    ) -> Dict[str, Optional[float]]:
        if prev_weight is None or curr_weight is None or not prev_date or not curr_date:
            return {'weight_change': None, 'days_elapsed': 0, 'adg': None}

        days_elapsed = (curr_date - prev_date).days
        weight_change = round(curr_weight - prev_weight, 3)
        if days_elapsed <= 0:
            return {'weight_change': weight_change, 'days_elapsed': days_elapsed, 'adg': None}

        adg = round(weight_change / days_elapsed, 3)
        return {
            'weight_change': weight_change,
            'days_elapsed': days_elapsed,
            'adg': adg
        }

    @staticmethod
    def calculate_nutrition_metrics(
        quantity_fed_kg: float,
        animal_count: int,
        dm_pct: float,
        cp_pct: float,
        me_mj_per_kg_dm: float,
        avg_animal_weight_kg: Optional[float] = None,
        target_dmi_pct_bw: float = 3.0
    ) -> Dict[str, float]:
        count = max(animal_count, 1)
        as_fed_per_head = quantity_fed_kg / count
        total_dm_kg = quantity_fed_kg * (dm_pct / 100.0)
        dm_per_head_kg = total_dm_kg / count
        total_cp_kg = total_dm_kg * (cp_pct / 100.0)
        cp_per_head_g = (total_cp_kg / count) * 1000.0
        total_me_mj = total_dm_kg * me_mj_per_kg_dm
        me_per_head_mj = total_me_mj / count

        recommended_dmi_kg = 0.0
        if avg_animal_weight_kg and avg_animal_weight_kg > 0:
            recommended_dmi_kg = avg_animal_weight_kg * (target_dmi_pct_bw / 100.0)

        return {
            'as_fed_per_head_kg': round(as_fed_per_head, 2),
            'total_dm_kg': round(total_dm_kg, 2),
            'dm_per_head_kg': round(dm_per_head_kg, 2),
            'cp_per_head_g': round(cp_per_head_g, 1),
            'me_per_head_mj': round(me_per_head_mj, 2),
            'recommended_dmi_kg': round(recommended_dmi_kg, 2)
        }

    @staticmethod
    def calculate_fcr(total_feed_kg: float, total_weight_gain_kg: float) -> Optional[float]:
        if not total_weight_gain_kg or total_weight_gain_kg <= 0 or total_feed_kg <= 0:
            return None
        return round(total_feed_kg / total_weight_gain_kg, 2)

    @staticmethod
    def calculate_hen_day_egg_percentage(eggs_collected: float, active_hens: int) -> float:
        if not active_hens or active_hens <= 0 or eggs_collected < 0:
            return 0.0
        pct = (eggs_collected / active_hens) * 100.0
        return round(min(pct, 100.0), 1)

    @staticmethod
    def calculate_dressing_percentage(carcass_weight: float, live_weight: float) -> Optional[float]:
        if not carcass_weight or not live_weight or live_weight <= 0:
            return None
        return round((carcass_weight / live_weight) * 100.0, 1)