import json
from pathlib import Path
import unicodedata, re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "symptom_to_specialty.json"

def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s).strip().lower())

def test_mapping_integrity():
    p = json.loads(DATA.read_text(encoding="utf-8"))
    m = p["symptom_to_specialty"]
    assert len(m) >= 80
    assert len({norm(k) for k in m}) == len(m)
    assert all(norm(k) == k for k in m)
    assert all(isinstance(v, str) and v for v in m.values())

def test_required_examples():
    p = json.loads(DATA.read_text(encoding="utf-8"))
    m = p["symptom_to_specialty"]
    assert m["skin rash"] == "Dermatology"
    assert m["chest tightness"] == "Cardiology"
    assert m["migraine"] == "Neurology"
    assert m["painful urination"] == "Urology"

def test_emergency_overrides():
    p = json.loads(DATA.read_text(encoding="utf-8"))
    o = p["emergency_overrides"]
    assert o["sudden one-sided weakness"] == "Emergency"
    assert o["severe breathing difficulty"] == "Emergency"
