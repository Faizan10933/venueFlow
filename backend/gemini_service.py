"""
VenueFlow — Gemini Chat Service (Demo Mode)
Provides AI-powered stadium assistant responses.
Falls back to intelligent demo responses if no API key is set.
"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Gemini
try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai package not found. AI chat will use demo fallback.")


SYSTEM_PROMPT = """You are "MatchDay AI", the intelligent stadium assistant for VenueFlow at Wankhede Stadium, Mumbai during an IPL match (Mumbai Indians vs Chennai Super Kings).

Your role:
- Help fans navigate the stadium
- Suggest the best food options, restrooms, and gates based on current crowd density
- Provide real-time wait time information
- Give personalized recommendations
- Share match schedule and timeline info
- Help with emergency situations (lost child, medical, etc.)

Stadium context:
- Wankhede Stadium, Mumbai — 33,000 capacity
- 4 entry gates (North, South, East, West)
- 8 seating sections (North/South/East/West Stands + 4 Pavilions)
- 6 food courts spread around the venue
- 8 restroom blocks
- 2 merchandise stores

Personality: Friendly, concise, helpful. Use emojis sparingly. Always provide actionable advice.
When suggesting zones, always mention current occupancy and wait times from the provided data.

CRITICAL INSTRUCTION: You MUST respond in the language requested by the user. If they request Hindi, respond in Hindi. If Marathi, respond in Marathi.
"""


DEMO_RESPONSES = {
    "food": {
        "keywords": ["food", "eat", "hungry", "snack", "restaurant", "lunch", "dinner", "vada pav", "biryani", "drink", "beverage", "coffee"],
        "response": """🍔 **Food Recommendations**

Based on current crowd data, here are your best options:

**Lowest Wait:** {best_food_zone} — ~{best_food_wait} min wait
**Avoid:** {worst_food_zone} — ~{worst_food_wait} min wait

**Popular Items:**
• 🥘 Vada Pav — ₹60 (2 min prep)
• 🌯 Chicken Tikka Roll — ₹180 (5 min prep)
• ☕ Cold Coffee — ₹120 (3 min prep)

💡 **Pro tip:** {food_tip}"""
    },
    "restroom": {
        "keywords": ["restroom", "bathroom", "toilet", "washroom", "loo"],
        "response": """🚻 **Nearest Low-Wait Restrooms**

**Best option:** {best_rest_zone} — ~{best_rest_wait} min wait ({best_rest_pct}% full)
**Also good:** {second_rest_zone}

**Avoid:** {worst_rest_zone} — currently {worst_rest_pct}% full

💡 Walk towards the {best_rest_direction} for the shortest lines right now."""
    },
    "gate": {
        "keywords": ["gate", "entry", "entrance", "exit", "leave", "go out", "parking"],
        "response": """🚪 **Gate Status**

**Recommended:** {best_gate} — ~{best_gate_wait} min wait
**Current Status:**
{gate_status}

💡 **Tip:** {gate_tip}"""
    },
    "seat": {
        "keywords": ["seat", "section", "stand", "pavilion", "where am i", "find my seat", "row"],
        "response": """💺 **Finding Your Seat**

The stadium has 8 seating sections:
• North Stand, South Stand, East Stand, West Stand
• NE Pavilion, NW Pavilion, SE Pavilion, SW Pavilion

Check your ticket for section and row number. Follow the signs from your nearest gate, or ask any of the ushers in blue vests.

🧭 **Quick guide:** Enter from the gate closest to your section — check the stadium map in the app for the optimal route!"""
    },
    "schedule": {
        "keywords": ["schedule", "time", "when", "innings", "break", "toss", "start", "end", "timeline"],
        "response": """📅 **Match Timeline — IPL 2026**
🏏 MI vs CSK at Wankhede Stadium

• **17:30** — Gates Open
• **19:00** — Toss
• **19:30** — First Innings
• **21:00** — Innings Break (20 min) 🍔
• **21:20** — Second Innings
• **~22:50** — Match Ends
• **22:55** — Staggered Exit Begins

⏰ **Current phase:** {current_phase}
💡 **Tip:** Order food 10 min before the innings break to skip the rush!"""
    },
    "emergency": {
        "keywords": ["emergency", "lost", "child", "medical", "help", "police", "fire", "security", "ambulance", "hurt", "injured"],
        "response": """🆘 **Emergency Assistance**

**Medical Emergency:** Look for the nearest First Aid booth (located at each gate area) or call the stadium helpline displayed on screens.

**Lost Child:** Report immediately to the nearest security personnel (in yellow vests) or visit the Information Desk at the North Gate.

**Security Concern:** Contact stadium security at any gate or flag down staff.

📞 **Stadium Helpline:** Available on the venue screens
📍 **First Aid:** Near all 4 main gates

Stay calm — help is always nearby. 💙"""
    },
    "crowd": {
        "keywords": ["crowd", "busy", "crowded", "rush", "congestion", "density", "packed", "empty", "quiet"],
        "response": """📊 **Live Crowd Status**

**Overall Attendance:** {attendance}% of capacity
**Busiest Zone:** {busiest_zone} ({busiest_pct}%)
**Current Phase:** {current_phase}

**Zone Summary:**
• 🟢 Low crowd: Merch stores, some restrooms
• 🟡 Moderate: Most food courts
• 🔴 High: {busiest_zone}

💡 **Tip:** {crowd_tip}"""
    },
    "default": {
        "keywords": [],
        "response": """👋 **Hey there! I'm MatchDay AI**

I can help you with:
• 🍔 **Food** — "Where should I eat?" / "Best food near me"
• 🚻 **Restrooms** — "Nearest low-wait restroom"
• 🚪 **Gates** — "Which gate should I use?"
• 📅 **Schedule** — "When is the innings break?"
• 📊 **Crowd** — "How crowded is it?"
• 🆘 **Emergency** — "I need medical help"

Just type your question naturally! I have real-time data from the stadium. 🏟️"""
    },
}


class GeminiService:
    """AI chat service with Gemini integration and smart demo fallback."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.use_gemini = False

        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                # Keep prompt exactly as original
                system_instruction = (
                    "You are 'MatchDay AI', the official AI assistant for VenueFlow "
                    "at the Wankhede Stadium. You answer questions about stadium queues, "
                    "food, and crowd density. Keep answers brief (under 3 sentences), "
                    "fun, and helpful. Format your responses with Markdown and emojis where appropriate.\n"
                    "If the user asks a question in a specific language (Hindi, Marathi, etc.), "
                    "you MUST answer entirely in that language. "
                    "Never hallucinate queue times, use the provided live data."
                )
                self.model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
                self.use_gemini = True
                logger.info("Gemini AI loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {e}")
                self.use_gemini = False

    async def chat(self, message: str, live_data: Dict[str, Any], language: str = "English") -> str:
        """Process a chat message and return a response."""
        if self.use_gemini:
            # Extract real wait times
            zones_info = "\n".join([f"- {z['name']}: {z['wait_time_min']} min wait ({int(z['occupancy_pct']*100)}% full)" for z in live_data['zones']])
            
            prompt = (
                f"User Question: {message}\n"
                f"Requested Language: {language}\n\n"
                f"Current Match Time: {live_data['sim_time']['display']}\n"
                f"Match Phase: {live_data['phase']}\n"
                f"Live Zone Status:\n{zones_info}\n\n"
                f"Answer the user's question accurately using ONLY the live zone status provided above. "
                f"Answer completely in {language}."
            )
            
            # Using GenerationConfig as requested for strictness
            config = GenerationConfig(
                temperature=0.4,
                top_p=0.9,
                top_k=40,
                max_output_tokens=300
            )

            try:
                # Need await for actual async calls if generativeai supports it, else use run_in_executor
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, 
                    lambda: self.model.generate_content(prompt, generation_config=config)
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini API Error: {e}")
                return "⚠️ Sorry, my AI brain is taking a break right now. Please check the dashboard for live wait times!"
            
        else:
            # Demo mode only supports English out of the box, but we'll prepend a note
            resp = self._demo_response(message, live_data)
            if language.lower() != "english":
                return f"*(Google Translate integration requires API Key. Showing default English demo)*\n\n{resp}"
            return resp

    def _demo_response(self, message: str, live_data: dict) -> str:
        """Generate intelligent demo response based on keywords and live data."""
        msg_lower = message.lower()
        summary = live_data.get("summary", {})
        zones = live_data.get("zones", [])
        phase = live_data.get("phase", "pre_match")

        # Find matching category
        matched_category = "default"
        for category, data in DEMO_RESPONSES.items():
            if category == "default":
                continue
            if any(kw in msg_lower for kw in data["keywords"]):
                matched_category = category
                break

        template = DEMO_RESPONSES[matched_category]["response"]

        # Build context data for template
        food_zones = sorted(
            [z for z in zones if z.get("type") == "food_court"],
            key=lambda x: x.get("occupancy_pct", 0),
        )
        rest_zones = sorted(
            [z for z in zones if z.get("type") == "restroom"],
            key=lambda x: x.get("occupancy_pct", 0),
        )
        gate_zones = sorted(
            [z for z in zones if z.get("type") == "gate"],
            key=lambda x: x.get("occupancy_pct", 0),
        )

        phase_display = {
            "pre_match": "Pre-Match (Fans Arriving)",
            "innings_1": "First Innings In Progress 🏏",
            "innings_break": "Innings Break — Rush Hour! 🍔",
            "innings_2": "Second Innings In Progress 🏏",
            "post_match": "Post-Match (Exit Time)",
        }.get(phase, phase)

        # Generate food tips
        food_tips = {
            "pre_match": "Grab food now before the match starts — lines will be much shorter!",
            "innings_1": "Lines are short during play. Great time to grab a quick snack!",
            "innings_break": "It's the innings break — expect long lines. Use pre-order to skip the queue!",
            "innings_2": "Most fans are watching. Quick runs for food will be easy!",
            "post_match": "Food courts are closing. Grab a drink for the road!",
        }

        gate_tips = {
            "pre_match": "Arrive early to avoid the last-minute rush before toss!",
            "innings_1": "Gates are quiet — no wait if you're arriving late.",
            "innings_break": "Gates are quiet. Focus on food instead!",
            "innings_2": "Gates are quiet. Match is on!",
            "post_match": "Exit will be staggered by section. Wait for your section's call to avoid the crush.",
        }

        crowd_tips = {
            "pre_match": "Arrive by 18:00 for the smoothest entry experience.",
            "innings_1": "Great time to visit food courts or restrooms — most fans are seated.",
            "innings_break": "Peak rush! Try to pre-order food or visit less popular food courts.",
            "innings_2": "Crowd is settled. Good time for restroom breaks.",
            "post_match": "Follow the staggered exit plan — don't rush to the gates.",
        }

        # Gate status
        gate_status_lines = []
        for g in gate_zones:
            pct = round(g.get("occupancy_pct", 0) * 100)
            icon = "🟢" if pct < 50 else "🟡" if pct < 80 else "🔴"
            gate_status_lines.append(f"  {icon} {g['name']}: {pct}% ({g.get('wait_time_min', 0)} min wait)")
        gate_status_str = "\n".join(gate_status_lines) if gate_status_lines else "  No gate data"

        context = {
            "best_food_zone": food_zones[0]["name"] if food_zones else "N/A",
            "best_food_wait": food_zones[0].get("wait_time_min", 0) if food_zones else 0,
            "worst_food_zone": food_zones[-1]["name"] if food_zones else "N/A",
            "worst_food_wait": food_zones[-1].get("wait_time_min", 0) if food_zones else 0,
            "food_tip": food_tips.get(phase, ""),
            "best_rest_zone": rest_zones[0]["name"] if rest_zones else "N/A",
            "best_rest_wait": rest_zones[0].get("wait_time_min", 0) if rest_zones else 0,
            "best_rest_pct": round(rest_zones[0].get("occupancy_pct", 0) * 100) if rest_zones else 0,
            "second_rest_zone": rest_zones[1]["name"] if len(rest_zones) > 1 else "N/A",
            "worst_rest_zone": rest_zones[-1]["name"] if rest_zones else "N/A",
            "worst_rest_pct": round(rest_zones[-1].get("occupancy_pct", 0) * 100) if rest_zones else 0,
            "best_rest_direction": rest_zones[0]["name"].split()[0] if rest_zones else "North",
            "best_gate": gate_zones[0]["name"] if gate_zones else "N/A",
            "best_gate_wait": gate_zones[0].get("wait_time_min", 0) if gate_zones else 0,
            "gate_status": gate_status_str,
            "gate_tip": gate_tips.get(phase, ""),
            "current_phase": phase_display,
            "attendance": summary.get("attendance_pct", 0),
            "busiest_zone": summary.get("busiest_zone", "N/A"),
            "busiest_pct": summary.get("busiest_zone_pct", 0),
            "crowd_tip": crowd_tips.get(phase, ""),
        }

        try:
            return template.format(**context)
        except KeyError as e:
            return template  # Return unformatted if key missing
