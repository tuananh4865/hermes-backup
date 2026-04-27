#!/usr/bin/env python3
"""
confidence_scorer.py

Scores wiki content confidence based on:
- source_count: how many sources support the claim
- recency: how recently confirmed
- reinforcement: times accessed/confirmed
- contradiction: number of conflicting claims
"""

import math
from datetime import datetime, timedelta
from typing import Optional


class ConfidenceScorer:
    """Calculate confidence scores for wiki claims."""
    
    # Decay half-lives by content type
    HALF_LIVES = {
        "architecture_decision": 180,  # days
        "project_fact": 30,            # days
        "transient_bug": 7,            # days
        "default": 90,                 # days
    }
    
    # Weights for each factor
    WEIGHTS = {
        "source_count": 0.25,
        "recency": 0.25,
        "reinforcement": 0.20,
        "contradiction": 0.30,
    }
    
    def __init__(self, content_type: str = "default"):
        self.content_type = content_type
        self.half_life = self.HALF_LIVES.get(content_type, self.HALF_LIVES["default"])
        
    def decay(self, days_elapsed: float) -> float:
        """
        Calculate decay factor using exponential decay.
        Returns value between 0 and 1.
        """
        if days_elapsed <= 0:
            return 1.0
        return math.pow(0.5, days_elapsed / self.half_life)
        
    def score(
        self,
        source_count: int = 1,
        days_since_confirm: int = 0,
        reinforcement_count: int = 0,
        contradiction_count: int = 0,
    ) -> float:
        """
        Calculate confidence score (0-1).
        
        Args:
            source_count: Number of independent sources supporting this claim
            days_since_confirm: Days since last confirmation
            reinforcement_count: Times accessed and confirmed
            contradiction_count: Number of contradicting claims
            
        Returns:
            float: Confidence score between 0 and 1
        """
        # Source factor (max 5 sources)
        source_factor = min(source_count, 5) / 5
        
        # Recency factor (decay over half-life)
        recency_factor = self.decay(days_since_confirm)
        
        # Reinforcement factor (max 10 reinforcements)
        reinforcement_factor = min(reinforcement_count, 10) / 10
        
        # Contradiction penalty
        contradiction_penalty = self.WEIGHTS["contradiction"] * contradiction_count * 0.1
        
        # Calculate weighted score
        score = (
            self.WEIGHTS["source_count"] * source_factor +
            self.WEIGHTS["recency"] * recency_factor +
            self.WEIGHTS["reinforcement"] * reinforcement_factor -
            contradiction_penalty
        )
        
        # Clamp to 0-1
        return max(0.0, min(1.0, score))
        
    def get_retention(self, initial_confidence: float, days_elapsed: float) -> float:
        """
        Calculate retention after time has passed.
        Uses Ebbinghaus forgetting curve.
        """
        return initial_confidence * self.decay(days_elapsed)
        
    def suggest_action(self, confidence: float) -> str:
        """
        Suggest action based on confidence level.
        """
        if confidence >= 0.8:
            return "excellent"  # Full priority in queries
        elif confidence >= 0.6:
            return "good"  # Normal priority
        elif confidence >= 0.4:
            return "fair"  # Deprioritized
        elif confidence >= 0.2:
            return "poor"  # Archive candidate
        else:
            return "critical"  # Review immediately


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Confidence scorer")
    parser.add_argument("--sources", type=int, default=1, help="Number of sources")
    parser.add_argument("--days", type=int, default=0, help="Days since confirm")
    parser.add_argument("--reinforce", type=int, default=0, help="Reinforcement count")
    parser.add_argument("--contradict", type=int, default=0, help="Contradiction count")
    parser.add_argument("--type", default="default", 
                       choices=["architecture_decision", "project_fact", "transient_bug", "default"],
                       help="Content type for half-life")
    parser.add_argument("--retention", action="store_true", 
                       help="Calculate retention instead of score")
    parser.add_argument("--initial", type=float, default=0.8,
                       help="Initial confidence for retention calc")
    
    args = parser.parse_args()
    
    scorer = ConfidenceScorer(args.type)
    
    if args.retention:
        result = scorer.get_retention(args.initial, args.days)
        print(f"Retention after {args.days} days: {result:.3f}")
    else:
        result = scorer.score(
            source_count=args.sources,
            days_since_confirm=args.days,
            reinforcement_count=args.reinforce,
            contradiction_count=args.contradict
        )
        action = scorer.suggest_action(result)
        print(f"Confidence: {result:.3f}")
        print(f"Action: {action}")


if __name__ == "__main__":
    main()
