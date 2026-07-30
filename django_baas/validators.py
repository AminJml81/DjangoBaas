import jsonschema
from django.core.exceptions import ValidationError


def validate_entity_data(data:dict, schema_definition:dict):
    """ validates data against given json schema definition"""

    if not schema_definition:
        return

    try:
        jsonschema.validate(instance=data, schema=schema_definition)

    except jsonschema.ValidationError as e:
        error_message = f"Validation Error in field {'/'.join(e.path) if e.path else 'root'}: {e.message}"
        raise ValidationError({'data': error_message})
    
    except jsonschema.exceptions.SchemaError as e:
        raise ValidationError(f"Invalid Schema Definition: {e.message}")