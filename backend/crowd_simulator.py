"""
VenueFlow — Crowd Simulation Engine
Generates realistic crowd density patterns for a live IPL match.
"""

import math
import random
import time
from typing import Dict, List, Optional
from stadium_data import ZONES, MATCH_TIMELINE

# Match phases and their crowd behavior profiles
PHASE_PROFILES = {
    "pre_match": {
        "gate": {"base": 0.6, "variance": 0.25, "trend_bias": 0.3},
        "seating": {"base": 0.3, "variance": 0.15, "trend_bias": 0.4},
        "food_court": {"base": 0.4, "variance": 0.2, "trend_bias": 0.1},
        "restroom": {"base": 0.3, "variance": 0.15, "trend_bias": 0.05},
        "merch_store": {"base": 0.5, "variance": 0.2, "trend_bias": 0.2},
    },
    "innings_1": {
        "gate": {"base": 0.1, "variance": 0.05, "trend_bias": -0.2},
        "seating": {"base": 0.9, "variance": 0.05, "trend_bias": 0.0},
        "food_court": {"base": 0.2, "variance": 0.1, "trend_bias": -0.1},
        "restroom": {"base": 0.2, "variance": 0.1, "trend_bias": 0.0},
        "merch_store": {"base": 0.15, "variance": 0.1, "trend_bias": -0.1},
    },
    "innings_break": {
        "gate": {"base": 0.05, "variance": 0.03, "trend_bias": 0.0},
        "seating": {"base": 0.4, "variance": 0.15, "trend_bias": -0.3},
        "food_court": {"base": 0.85, "variance": 0.1, "trend_bias": 0.4},
        "restroom": {"base": 0.75, "variance": 0.15, "trend_bias": 0.3},
        "merch_store": {"base": 0.6, "variance": 0.15, "trend_bias": 0.2},
    },
    "innings_2": {
        "gate": {"base": 0.05, "variance": 0.03, "trend_bias": 0.0},
        "seating": {"base": 0.85, "variance": 0.08, "trend_bias": 0.1},
        "food_court": {"base": 0.25, "variance": 0.1, "trend_bias": -0.15},
        "restroom": {"base": 0.25, "variance": 0.1, "trend_bias": -0.1},
        "merch_store": {"base": 0.1, "variance": 0.08, "trend_bias": -0.1},
    },
    "post_match": {
        "gate": {"base": 0.8, "variance": 0.15, "trend_bias": 0.3},
        "seating": {"base": 0.3, "variance": 0.2, "trend_bias": -0.4},
        "food_court": {"base": 0.1, "variance": 0.05, "trend_bias": -0.2},
        "restroom": {"base": 0.4, "variance": 0.15, "trend_bias": 0.1},
        "merch_store": {"base": 0.3, "variance": 0.15, "trend_bias": 0.1},
    },
}


class CrowdSimulator:
    """Simulates realistic crowd patterns in a stadium."""

    def __init__(self):
        self.start_time = time.time()
        self.zone_states: Dict[str, dict] = {}
        self.alerts: List[dict] = []
        self.tick_count = 0
        # Time compression: 1 real second = 2 simulated minutes
        self.time_compression = 120
        # Match starts at 17:30 in sim time
        self.match_start_hour = 17
        self.match_start_min = 30
        self._initialize_zones()

    def _initialize_zones(self):
        """Set initial zone states."""
        for zone in ZONES:
            self.zone_states[zone["id"]] = {
                "id": zone["id"],
                "name": zone["name"],
                "type": zone["type"],
                "capacity": zone["capacity"],
                "current_occupancy": 0,
                "occupancy_pct": 0.0,
                "trend": "stable",
                "wait_time_min": 0,
                "previous_occupancy": 0,
                "cx": zone["cx"],
                "cy": zone["cy"],
                "rx": zone.get("rx", 15),
                "ry": zone.get("ry", 15),
            }

    def get_simulated_time(self) -> dict:
        """Get current simulated match time."""
        elapsed_real = time.time() - self.start_time
        elapsed_sim_minutes = (elapsed_real * self.time_compression) / 60
        total_minutes = self.match_start_hour * 60 + self.match_start_min + elapsed_sim_minutes
        hours = int(total_minutes // 60) % 24
        minutes = int(total_minutes % 60)
        return {
            "hours": hours,
            "minutes": minutes,
            "display": f"{hours:02d}:{minutes:02d}",
            "total_minutes": total_minutes,
            "elapsed_sim_minutes": elapsed_sim_minutes,
        }

    def get_current_phase(self) -> str:
        """Determine current match phase based on simulated time."""
        sim_time = self.get_simulated_time()
        h, m = sim_time["hours"], sim_time["minutes"]
        time_val = h * 60 + m

        if time_val < 19 * 60 + 30:
            return "pre_match"
        elif time_val < 21 * 60:
            return "innings_1"
        elif time_val < 21 * 60 + 20:
            return "innings_break"
        elif time_val < 22 * 60 + 50:
            return "innings_2"
        else:
            return "post_match"

    def _generate_noise(self, amplitude: float = 0.05) -> float:
        """Perlin-like noise using sine waves."""
        t = self.tick_count * 0.1
        noise = (
            math.sin(t * 1.3) * 0.4
            + math.sin(t * 2.7 + 1.5) * 0.3
            + math.sin(t * 4.1 + 3.0) * 0.2
            + random.gauss(0, 0.3) * 0.1
        )
        return noise * amplitude

    def tick(self) -> dict:
        """Advance simulation by one tick and return current state."""
        self.tick_count += 1
        phase = self.get_current_phase()
        sim_time = self.get_simulated_time()
        profile = PHASE_PROFILES.get(phase, PHASE_PROFILES["pre_match"])
        new_alerts = []

        for zone in ZONES:
            zid = zone["id"]
            ztype = zone["type"]
            state = self.zone_states[zid]
            type_profile = profile.get(ztype, {"base": 0.3, "variance": 0.1, "trend_bias": 0.0})

            # Calculate target occupancy
            base = type_profile["base"]
            variance = type_profile["variance"]
            noise = self._generate_noise(variance)

            # Add zone-specific variation
            zone_seed = hash(zid) % 100 / 100.0
            zone_variation = math.sin(self.tick_count * 0.05 + zone_seed * 10) * variance * 0.5

            target_pct = max(0.0, min(1.0, base + noise + zone_variation))

            # Smooth transition from current to target
            prev_pct = state["occupancy_pct"]
            smoothing = 0.15
            new_pct = prev_pct + (target_pct - prev_pct) * smoothing
            new_pct = max(0.0, min(1.0, new_pct))

            # Calculate occupancy
            new_occupancy = int(new_pct * zone["capacity"])
            prev_occupancy = state["current_occupancy"]

            # Determine trend
            diff = new_occupancy - prev_occupancy
            if diff > zone["capacity"] * 0.02:
                trend = "rising"
            elif diff < -zone["capacity"] * 0.02:
                trend = "falling"
            else:
                trend = "stable"

            # Calculate wait time (for food courts, restrooms, gates)
            wait_time = 0
            if ztype in ("food_court", "restroom", "gate"):
                if new_pct > 0.8:
                    wait_time = int(new_pct * 20 + random.randint(-2, 2))
                elif new_pct > 0.5:
                    wait_time = int(new_pct * 10 + random.randint(-1, 1))
                elif new_pct > 0.3:
                    wait_time = int(new_pct * 5)
                wait_time = max(0, wait_time)

            # Generate alerts for high occupancy
            if new_pct > 0.9 and prev_pct <= 0.9:
                alert = {
                    "id": f"alert_{self.tick_count}_{zid}",
                    "type": "critical",
                    "zone_id": zid,
                    "zone_name": zone["name"],
                    "message": f"🔴 {zone['name']} at {int(new_pct*100)}% capacity! Consider alternatives.",
                    "time": sim_time["display"],
                    "timestamp": time.time(),
                }
                new_alerts.append(alert)
            elif new_pct > 0.7 and prev_pct <= 0.7:
                alert = {
                    "id": f"alert_{self.tick_count}_{zid}",
                    "type": "warning",
                    "zone_id": zid,
                    "zone_name": zone["name"],
                    "message": f"🟡 {zone['name']} is getting crowded ({int(new_pct*100)}%). Wait time: ~{wait_time} min.",
                    "time": sim_time["display"],
                    "timestamp": time.time(),
                }
                new_alerts.append(alert)
            elif new_pct < 0.3 and prev_pct >= 0.3 and ztype in ("food_court", "restroom"):
                alert = {
                    "id": f"alert_{self.tick_count}_{zid}",
                    "type": "info",
                    "zone_id": zid,
                    "zone_name": zone["name"],
                    "message": f"🟢 {zone['name']} is now clear! Great time to visit.",
                    "time": sim_time["display"],
                    "timestamp": time.time(),
                }
                new_alerts.append(alert)

            # Update state
            state["previous_occupancy"] = prev_occupancy
            state["current_occupancy"] = new_occupancy
            state["occupancy_pct"] = round(new_pct, 3)
            state["trend"] = trend
            state["wait_time_min"] = wait_time

        # Keep alerts (last 50)
        self.alerts = (new_alerts + self.alerts)[:50]

        # Compute summary stats
        total_occupancy = sum(s["current_occupancy"] for s in self.zone_states.values() if s["type"] == "seating")
        total_capacity = sum(z["capacity"] for z in ZONES if z["type"] == "seating")
        
        food_zones = [s for s in self.zone_states.values() if s["type"] == "food_court"]
        avg_food_wait = sum(s["wait_time_min"] for s in food_zones) / len(food_zones) if food_zones else 0

        restroom_zones = [s for s in self.zone_states.values() if s["type"] == "restroom"]
        avg_restroom_wait = sum(s["wait_time_min"] for s in restroom_zones) / len(restroom_zones) if restroom_zones else 0

        busiest_zone = max(self.zone_states.values(), key=lambda s: s["occupancy_pct"])
        active_alerts = len([a for a in self.alerts if a["type"] == "critical"])

        return {
            "sim_time": sim_time,
            "phase": phase,
            "zones": list(self.zone_states.values()),
            "alerts": self.alerts[:20],
            "new_alerts": new_alerts,
            "summary": {
                "total_attendance": total_occupancy,
                "total_capacity": total_capacity,
                "attendance_pct": round(total_occupancy / total_capacity * 100, 1) if total_capacity else 0,
                "avg_food_wait": round(avg_food_wait, 1),
                "avg_restroom_wait": round(avg_restroom_wait, 1),
                "busiest_zone": busiest_zone["name"],
                "busiest_zone_pct": round(busiest_zone["occupancy_pct"] * 100, 1),
                "active_alerts": active_alerts,
            },
            "tick": self.tick_count,
        }

    def get_zone_recommendation(self, zone_type: str) -> dict:
        """Get the best zone of a given type (lowest occupancy)."""
        zones_of_type = [
            s for s in self.zone_states.values() if s["type"] == zone_type
        ]
        if not zones_of_type:
            return {"error": f"No zones of type {zone_type}"}
        best = min(zones_of_type, key=lambda z: z["occupancy_pct"])
        return {
            "recommended": best["name"],
            "occupancy_pct": round(best["occupancy_pct"] * 100, 1),
            "wait_time_min": best["wait_time_min"],
            "all_options": [
                {
                    "name": z["name"],
                    "occupancy_pct": round(z["occupancy_pct"] * 100, 1),
                    "wait_time_min": z["wait_time_min"],
                    "trend": z["trend"],
                }
                for z in sorted(zones_of_type, key=lambda x: x["occupancy_pct"])
            ],
        }
