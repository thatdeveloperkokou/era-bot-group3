"""
Seed data for Nigerian DisCo regional profiles derived from NERC Q2 2025 report.
"""
from __future__ import annotations

from typing import List, Dict


DISCO_Q2_DATA = [
    {
        "id": "abuja",
        "disco_name": "Abuja Electricity Distribution Plc (AEDC)",
        "states": ["fct", "abuja", "niger", "kogi", "nasarawa"],
        "keywords": ["abuja", "fct", "gwarinpa", "lokoja", "mina", "lafia"],
        "avg_offtake": 547.84,
        "avg_pcc": 611.00,
        "pct": 89.66,
    },
    {
        "id": "benin",
        "disco_name": "Benin Electricity Distribution Plc (BEDC)",
        "states": ["edo", "delta", "ondo", "ekiti"],
        "keywords": ["benin", "asaba", "warri", "akure", "ado ekiti", "sapele"],
        "avg_offtake": 338.35,
        "avg_pcc": 338.35,
        "pct": 100.0,
    },
    {
        "id": "eko",
        "disco_name": "Eko Electricity Distribution Plc (EKEDC)",
        "states": ["lagos island", "eti osa", "apapa", "lagos south"],
        "keywords": ["victoria island", "lekki", "ajah", "apapa", "surulere", "ikoyi"],
        "avg_offtake": 481.59,
        "avg_pcc": 508.87,
        "pct": 94.64,
    },
    {
        "id": "enugu",
        "disco_name": "Enugu Electricity Distribution Plc (EEDC)",
        "states": ["enugu", "ebonyi", "anambra", "abia", "imo"],
        "keywords": ["enugu", "awka", "aba", "owerri", "umahia", "onitsha"],
        "avg_offtake": 307.03,
        "avg_pcc": 313.81,
        "pct": 97.84,
    },
    {
        "id": "ibadan",
        "disco_name": "Ibadan Electricity Distribution Plc (IBEDC)",
        "states": ["oyo", "ogun", "osun", "kwara", "ekiti north"],
        "keywords": ["ibadan", "ilorin", "abeokuta", "osogbo", "shaki"],
        "avg_offtake": 418.76,
        "avg_pcc": 461.37,
        "pct": 90.76,
    },
    {
        "id": "ikeja",
        "disco_name": "Ikeja Electric Plc (IE)",
        "states": ["lagos mainland"],
        "keywords": ["ikeja", "agege", "ikorodu", "ikotun", "oshodi", "alimosho"],
        "avg_offtake": 567.76,
        "avg_pcc": 591.29,
        "pct": 96.02,
    },
    {
        "id": "jos",
        "disco_name": "Jos Electricity Distribution Plc (JED)",
        "states": ["plateau", "gombe", "bauchi", "benue"],
        "keywords": ["jos", "gombe", "bauchi", "makurdi", "otukpo"],
        "avg_offtake": 168.07,
        "avg_pcc": 208.69,
        "pct": 80.54,
    },
    {
        "id": "kaduna",
        "disco_name": "Kaduna Electricity Distribution Plc (KAEDC)",
        "states": ["kaduna", "zamfara", "sokoto", "kebbi"],
        "keywords": ["kaduna", "zaria", "sokoto", "gusau", "birnin kebbi"],
        "avg_offtake": 176.81,
        "avg_pcc": 234.58,
        "pct": 75.37,
    },
    {
        "id": "kano",
        "disco_name": "Kano Electricity Distribution Plc (KEDCO)",
        "states": ["kano", "jigawa", "katsina"],
        "keywords": ["kano", "dutse", "katsina", "kazaure"],
        "avg_offtake": 204.11,
        "avg_pcc": 246.34,
        "pct": 82.86,
    },
    {
        "id": "port_harcourt",
        "disco_name": "Port Harcourt Electricity Distribution Plc (PHED)",
        "states": ["rivers", "akwa ibom", "bayelsa", "cross river"],
        "keywords": ["port harcourt", "uyo", "calabar", "yenagoa"],
        "avg_offtake": 266.78,
        "avg_pcc": 278.32,
        "pct": 95.85,
    },
    {
        "id": "yola",
        "disco_name": "Yola Electricity Distribution Plc (YEDC)",
        "states": ["adamawa", "taraba", "borno", "yobe"],
        "keywords": ["yola", "maiduguri", "jalingo", "damaturu", "mubi"],
        "avg_offtake": 105.51,
        "avg_pcc": 110.82,
        "pct": 95.2,
    },
]


def build_schedule_template(full_load_hours: float) -> List[Dict[str, str]]:
    """
    Construct a simplistic ON-block schedule based on the estimated full-load hours.
    Each block represents a window of expected supply based on NERC Q2 2025 data.
    """
    if full_load_hours >= 23:
        return [{"start": "00:00", "end": "23:59"}]
    if full_load_hours >= 21.5:
        return [
            {"start": "00:00", "end": "11:00"},
            {"start": "14:00", "end": "23:59"},
        ]
    if full_load_hours >= 19.5:
        return [
            {"start": "05:00", "end": "11:00"},
            {"start": "16:00", "end": "23:30"},
        ]
    if full_load_hours >= 17.5:
        return [
            {"start": "05:30", "end": "10:30"},
            {"start": "13:30", "end": "17:30"},
            {"start": "19:30", "end": "23:30"},
        ]
    return [
        {"start": "05:00", "end": "09:00"},
        {"start": "12:00", "end": "16:00"},
        {"start": "19:00", "end": "22:00"},
    ]


def _build_seed_entry(entry: Dict[str, object]) -> Dict[str, object]:
    avg_offtake = float(entry["avg_offtake"])
    pct = float(entry["pct"])
    estimated_daily_mwh = round(avg_offtake * 24, 2)
    estimated_full_load_hours = round((pct / 100.0) * 24, 2)
    schedule = build_schedule_template(estimated_full_load_hours)
    return {
        "id": entry["id"],
        "disco_name": entry["disco_name"],
        "states": entry["states"],
        "keywords": entry["keywords"],
        "avg_offtake_mwh_per_hour": avg_offtake,
        "avg_available_pcc_mwh_per_hour": float(entry["avg_pcc"]),
        "utilisation_percent": pct,
        "estimated_daily_mwh": estimated_daily_mwh,
        "estimated_full_load_hours": estimated_full_load_hours,
        "schedule_template": schedule,
        "source": "NERC Q2 2025",
    }


REGION_PROFILE_SEED_DATA: List[Dict[str, object]] = [
    _build_seed_entry(row) for row in DISCO_Q2_DATA
]


