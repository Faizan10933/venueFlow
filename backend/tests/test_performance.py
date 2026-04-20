import pytest
import time
from crowd_simulator import CrowdSimulator

def test_simulator_performance_benchmark():
    """
    Performance benchmark: Ensure simulation tick runs in under 5ms.
    Critical for real-time WebSocket broadcasting.
    """
    sim = CrowdSimulator()
    start_time = time.time()
    
    # Run 100 ticks
    for _ in range(100):
        sim.tick()
        
    end_time = time.time()
    avg_tick_time = (end_time - start_time) / 100
    
    print(f"Average tick time: {avg_tick_time*1000:.4f}ms")
    assert avg_tick_time < 0.005  # Must be faster than 5ms
