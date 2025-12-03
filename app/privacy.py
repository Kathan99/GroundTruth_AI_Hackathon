from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import spacy

try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("Downloading en_core_web_lg model...")
    from spacy.cli import download
    download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")

class PrivacyManager:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        phone_pattern = Pattern(name="indian_phone_pattern", regex=r"\+91-\d{5}-\d{5}", score=1.0)
        phone_recognizer = PatternRecognizer(supported_entity="PHONE_NUMBER", patterns=[phone_pattern])
        self.analyzer.registry.add_recognizer(phone_recognizer)

    def anonymize(self, text: str):
        """
        Anonymizes the input text by replacing sensitive entities with placeholders.
        """
        if not text:
            return text

        results = self.analyzer.analyze(
            text=text,
            entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON", "LOCATION"],
            language='en'
        )
        
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "DEFAULT": OperatorConfig("replace", {"new_value": "<SENSITIVE_DATA>"}),
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE_NUMBER>"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_ADDRESS>"}),
                "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
                "LOCATION": OperatorConfig("replace", {"new_value": "<LOCATION>"}),
            }
        )
        
        return anonymized_result.text

if __name__ == "__main__":
    pm = PrivacyManager()
    text = "My name is John Doe, my email is john@example.com and my number is 555-0199."
    print(f"Original: {text}")
    print(f"Anonymized: {pm.anonymize(text)}")
