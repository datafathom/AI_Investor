import logging

logger = logging.getLogger(__name__)

class SharpeGrader:
    """Grades Sharpe ratios based on industry standard performance bands."""
    
    def grade_performance(self, sharpe: float) -> str:
        if sharpe >= 3.0:
            grade = "EXCEPTIONAL"
        elif sharpe >= 2.0:
            grade = "VERY_GOOD"
        elif sharpe >= 1.0:
            grade = "GOOD"
        elif sharpe >= 0.0:
            grade = "BELOW_AVERAGE"
        else:
            grade = "POOR"
            
        logger.info(f"QUANT_LOG: Sharpe {sharpe:.2f} graded as {grade}")
        return grade

    def get_color_code(self, grade: str) -> str:
        colors = {
            "EXCEPTIONAL": "#0000FF", # Blue
            "VERY_GOOD": "#00FF00",   # Green
            "GOOD": "#FFFF00",        # Yellow
            "BELOW_AVERAGE": "#FFA500", # Orange
            "POOR": "#FF0000"         # Red
        }
        return colors.get(grade, "#808080")
