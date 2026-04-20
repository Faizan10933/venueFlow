"""
VenueFlow — Stadium Data Model
Wankhede Stadium, Mumbai — IPL Match Context
"""

STADIUM_INFO = {
    "name": "Wankhede Stadium",
    "city": "Mumbai",
    "capacity": 33000,
    "event": "IPL 2026 — Mumbai Indians vs Chennai Super Kings",
    "match_time": "19:30",
    "gates_open": "17:30",
}

# Zone types: "gate", "seating", "food_court", "restroom", "merch_store", "corridor"
ZONES = [
    # Entry Gates
    {"id": "gate_north", "name": "North Gate", "type": "gate", "capacity": 800, "cx": 250, "cy": 60, "rx": 50, "ry": 20},
    {"id": "gate_south", "name": "South Gate", "type": "gate", "capacity": 800, "cx": 250, "cy": 440, "rx": 50, "ry": 20},
    {"id": "gate_east", "name": "East Gate", "type": "gate", "capacity": 600, "cx": 440, "cy": 250, "rx": 20, "ry": 50},
    {"id": "gate_west", "name": "West Gate", "type": "gate", "capacity": 600, "cx": 60, "cy": 250, "rx": 20, "ry": 50},

    # Seating Sections (arranged around the oval)
    {"id": "stand_north", "name": "North Stand", "type": "seating", "capacity": 5000, "cx": 250, "cy": 110, "rx": 90, "ry": 25},
    {"id": "stand_south", "name": "South Stand", "type": "seating", "capacity": 5000, "cx": 250, "cy": 390, "rx": 90, "ry": 25},
    {"id": "stand_east", "name": "East Stand", "type": "seating", "capacity": 4500, "cx": 390, "cy": 250, "rx": 25, "ry": 90},
    {"id": "stand_west", "name": "West Stand", "type": "seating", "capacity": 4500, "cx": 110, "cy": 250, "rx": 25, "ry": 90},
    {"id": "stand_ne", "name": "North-East Pavilion", "type": "seating", "capacity": 3500, "cx": 370, "cy": 130, "rx": 40, "ry": 30},
    {"id": "stand_nw", "name": "North-West Pavilion", "type": "seating", "capacity": 3500, "cx": 130, "cy": 130, "rx": 40, "ry": 30},
    {"id": "stand_se", "name": "South-East Pavilion", "type": "seating", "capacity": 3500, "cx": 370, "cy": 370, "rx": 40, "ry": 30},
    {"id": "stand_sw", "name": "South-West Pavilion", "type": "seating", "capacity": 3500, "cx": 130, "cy": 370, "rx": 40, "ry": 30},

    # Food Courts
    {"id": "food_north", "name": "North Food Court", "type": "food_court", "capacity": 200, "cx": 250, "cy": 155, "rx": 20, "ry": 10},
    {"id": "food_south", "name": "South Food Court", "type": "food_court", "capacity": 200, "cx": 250, "cy": 345, "rx": 20, "ry": 10},
    {"id": "food_east", "name": "East Food Plaza", "type": "food_court", "capacity": 180, "cx": 345, "cy": 250, "rx": 10, "ry": 20},
    {"id": "food_west", "name": "West Food Plaza", "type": "food_court", "capacity": 180, "cx": 155, "cy": 250, "rx": 10, "ry": 20},
    {"id": "food_ne", "name": "NE Snack Bar", "type": "food_court", "capacity": 120, "cx": 340, "cy": 160, "rx": 12, "ry": 8},
    {"id": "food_sw", "name": "SW Snack Bar", "type": "food_court", "capacity": 120, "cx": 160, "cy": 340, "rx": 12, "ry": 8},

    # Restrooms
    {"id": "rest_north", "name": "North Restrooms", "type": "restroom", "capacity": 80, "cx": 200, "cy": 100, "rx": 10, "ry": 8},
    {"id": "rest_south", "name": "South Restrooms", "type": "restroom", "capacity": 80, "cx": 300, "cy": 400, "rx": 10, "ry": 8},
    {"id": "rest_east", "name": "East Restrooms", "type": "restroom", "capacity": 60, "cx": 400, "cy": 200, "rx": 8, "ry": 10},
    {"id": "rest_west", "name": "West Restrooms", "type": "restroom", "capacity": 60, "cx": 100, "cy": 300, "rx": 8, "ry": 10},
    {"id": "rest_ne", "name": "NE Restrooms", "type": "restroom", "capacity": 50, "cx": 380, "cy": 160, "rx": 8, "ry": 8},
    {"id": "rest_sw", "name": "SW Restrooms", "type": "restroom", "capacity": 50, "cx": 120, "cy": 340, "rx": 8, "ry": 8},
    {"id": "rest_se", "name": "SE Restrooms", "type": "restroom", "capacity": 50, "cx": 380, "cy": 340, "rx": 8, "ry": 8},
    {"id": "rest_nw", "name": "NW Restrooms", "type": "restroom", "capacity": 50, "cx": 120, "cy": 160, "rx": 8, "ry": 8},

    # Merchandise Stores
    {"id": "merch_north", "name": "MI Fan Store (North)", "type": "merch_store", "capacity": 100, "cx": 300, "cy": 95, "rx": 12, "ry": 8},
    {"id": "merch_south", "name": "Official Merch Store", "type": "merch_store", "capacity": 100, "cx": 200, "cy": 405, "rx": 12, "ry": 8},
]

FOOD_MENU = [
    {"id": "f1", "name": "Vada Pav", "price": 60, "category": "Snacks", "prep_time_min": 2, "veg": True},
    {"id": "f2", "name": "Chicken Tikka Roll", "price": 180, "category": "Main", "prep_time_min": 5, "veg": False},
    {"id": "f3", "name": "Paneer Tikka Roll", "price": 160, "category": "Main", "prep_time_min": 5, "veg": True},
    {"id": "f4", "name": "Masala Dosa", "price": 120, "category": "Main", "prep_time_min": 7, "veg": True},
    {"id": "f5", "name": "Pav Bhaji", "price": 100, "category": "Snacks", "prep_time_min": 4, "veg": True},
    {"id": "f6", "name": "Samosa (2 pcs)", "price": 50, "category": "Snacks", "prep_time_min": 2, "veg": True},
    {"id": "f7", "name": "Cold Coffee", "price": 120, "category": "Beverages", "prep_time_min": 3, "veg": True},
    {"id": "f8", "name": "Fresh Lime Soda", "price": 80, "category": "Beverages", "prep_time_min": 2, "veg": True},
    {"id": "f9", "name": "Mango Lassi", "price": 100, "category": "Beverages", "prep_time_min": 3, "veg": True},
    {"id": "f10", "name": "French Fries", "price": 90, "category": "Snacks", "prep_time_min": 4, "veg": True},
    {"id": "f11", "name": "Chicken Biryani", "price": 220, "category": "Main", "prep_time_min": 8, "veg": False},
    {"id": "f12", "name": "Pepsi 500ml", "price": 60, "category": "Beverages", "prep_time_min": 1, "veg": True},
    {"id": "f13", "name": "Ice Cream Sundae", "price": 140, "category": "Desserts", "prep_time_min": 3, "veg": True},
    {"id": "f14", "name": "Nachos with Cheese", "price": 150, "category": "Snacks", "prep_time_min": 4, "veg": True},
    {"id": "f15", "name": "Butter Chicken Meal", "price": 250, "category": "Main", "prep_time_min": 10, "veg": False},
]

MATCH_TIMELINE = [
    {"time": "17:30", "event": "Gates Open", "phase": "pre_match"},
    {"time": "18:00", "event": "Early Bird Entry Window", "phase": "pre_match"},
    {"time": "18:30", "event": "Peak Entry Rush", "phase": "pre_match"},
    {"time": "19:00", "event": "Toss", "phase": "pre_match"},
    {"time": "19:30", "event": "First Innings Starts", "phase": "innings_1"},
    {"time": "19:45", "event": "Powerplay Ends", "phase": "innings_1"},
    {"time": "20:15", "event": "Strategic Timeout 1", "phase": "innings_1"},
    {"time": "20:45", "event": "Strategic Timeout 2", "phase": "innings_1"},
    {"time": "21:00", "event": "First Innings Ends", "phase": "innings_break"},
    {"time": "21:00", "event": "Innings Break (20 min) — Best time to grab food!", "phase": "innings_break"},
    {"time": "21:20", "event": "Second Innings Starts", "phase": "innings_2"},
    {"time": "21:35", "event": "Powerplay Ends", "phase": "innings_2"},
    {"time": "22:05", "event": "Strategic Timeout 3", "phase": "innings_2"},
    {"time": "22:35", "event": "Strategic Timeout 4", "phase": "innings_2"},
    {"time": "22:50", "event": "Match Ends (approx)", "phase": "post_match"},
    {"time": "22:55", "event": "Staggered Exit Begins", "phase": "post_match"},
    {"time": "23:30", "event": "Venue Clears", "phase": "post_match"},
]
