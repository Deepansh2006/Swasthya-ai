"""
rule_engine.py
Deterministic Red-Flag Safety Engine.
Fires BEFORE any LLM call to guarantee ZERO under-triage on emergency cases.
Uses rapidfuzz fuzzy string matching and regex pattern matching.
"""

import os
import yaml
from typing import Optional, Dict, Any, Tuple
from rapidfuzz import fuzz
from backend.app.models.schemas import UrgencyLevel

class RedFlagRuleEngine:
    def __init__(self, rules_path: Optional[str] = None):
        if rules_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            rules_path = os.path.join(base_dir, "rules", "redflags.yaml")
        self.rules_path = rules_path
        self.protocols = []
        self.load_rules()

    def load_rules(self):
        if not os.path.exists(self.rules_path):
            raise FileNotFoundError(f"Rules YAML not found: {self.rules_path}")
        with open(self.rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            self.protocols = data.get("protocols", [])

    def evaluate(self, text: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Evaluate raw transcript against emergency red-flag rules.
        Returns: (is_emergency, match_details)
        """
        if not text or not text.strip():
            return False, None

        normalized_text = text.lower().strip()

        for protocol in self.protocols:
            protocol_id = protocol.get("id")
            name = protocol.get("name")
            action_hi = protocol.get("action_hi")
            source = protocol.get("source")
            triggers = protocol.get("triggers", [])

            for trigger in triggers:
                trig_norm = trigger.lower().strip()
                
                # 1. Exact substring check
                if trig_norm in normalized_text:
                    return True, {
                        "protocol_id": protocol_id,
                        "protocol_name": name,
                        "matched_trigger": trigger,
                        "match_type": "exact_substring",
                        "urgency": UrgencyLevel.EMERGENCY,
                        "action_hi": action_hi,
                        "source": source
                    }

                # 2. Token set ratio and fuzzy similarity check (handles intervening words like 'बहुत', word order)
                if len(trig_norm) >= 4:
                    ts_ratio = fuzz.token_set_ratio(trig_norm, normalized_text)
                    p_ratio = fuzz.partial_ratio(trig_norm, normalized_text)
                    if ts_ratio >= 85 or p_ratio >= 85:
                        return True, {
                            "protocol_id": protocol_id,
                            "protocol_name": name,
                            "matched_trigger": trigger,
                            "match_type": f"fuzzy_ts_{ts_ratio}_p_{p_ratio}",
                            "urgency": UrgencyLevel.EMERGENCY,
                            "action_hi": action_hi,
                            "source": source
                        }

        return False, None

# Singleton instance
rule_engine = RedFlagRuleEngine()
