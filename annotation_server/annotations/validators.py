import requests
from django.core.exceptions import ValidationError

def validate_annotation_type(annotation_type):
    # Retrieves the JSON-LD schema.
    response = requests.get("https://www.w3.org/ns/anno.jsonld")

    # If the schema could not be retrieved, raises a validation error.
    if response.status_code != 200:
        raise ValidationError("Failed to retrieve annotation JSON-LD schema.")

    w3_jsonld = response.json()

    # If the annotation_type is not a property in the schema, raises a validation error.
    if annotation_type not in w3_jsonld["@context"]:
        raise ValidationError("The annotation_type is not a valid annotation JSON-LD property.")
