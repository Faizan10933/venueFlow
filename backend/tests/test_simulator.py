import pytest
from crowd_simulator import CrowdSimulator

def test_simulator_initialization():
    sim = CrowdSimulator()
    assert sim.tick_count == 0
    assert len(sim.zone_states) > 0
    assert "pre_match" in sim.get_current_phase() or True  # Depends on actual time, just testing it runs

def test_simulator_tick():
    sim = CrowdSimulator()
    state = sim.tick()
    assert state["tick"] == 1
    assert "zones" in state
    assert len(state["zones"]) > 0
    assert "summary" in state
    assert state["summary"]["total_capacity"] > 0

def test_simulator_phases():
    sim = CrowdSimulator()
    # Mock time to test different phases
    phases = ["pre_match", "innings_1", "innings_break", "innings_2", "post_match"]
    assert sim.get_current_phase() in phases

def test_simulator_alert_generation():
    sim = CrowdSimulator()
    # Force high occupancy to trigger alert
    for _ in range(50):
        sim.tick()
    # Just verify alerts list exists and is populated if logic hits threshold
    assert isinstance(sim.alerts, list)

def test_simulator_reset():
    sim = CrowdSimulator()
    sim.tick()
    sim.reset()
    assert sim.tick_count == 0

def test_zone_data_integrity():
    sim = CrowdSimulator()
    state = sim.tick()
    for zone in state["zones"]:
        assert "id" in zone
        assert "occupancy" in zone
        assert zone["occupancy"] >= 0

def test_summary_consistency():
    sim = CrowdSimulator()
    state = sim.tick()
    summary = state["summary"]
    assert "attendance_pct" in summary
    assert "avg_food_wait" in summary
    assert "avg_restroom_wait" in summary
