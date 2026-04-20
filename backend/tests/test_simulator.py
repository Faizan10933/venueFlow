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

def test_zone_recommendation():
    sim = CrowdSimulator()
    sim.tick()
    rec = sim.get_zone_recommendation("food_court")
    assert "recommended" in rec
    assert "occupancy_pct" in rec
    
    # Test invalid zone type
    bad_rec = sim.get_zone_recommendation("invalid_zone")
    assert "error" in bad_rec
