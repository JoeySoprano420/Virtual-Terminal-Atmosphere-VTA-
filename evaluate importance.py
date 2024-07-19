# error_handler.py
class ErrorHandler:
    def __init__(self):
        self.web_crawler = WebCrawler()

    def evaluate_importance(self, script):
        # Analyze the script to determine importance
        if "critical" in script:
            return "high"
        elif "warning" in script:
            return "medium"
        else:
            return "low"
