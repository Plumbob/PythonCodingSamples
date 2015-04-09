# JSON schema validator
# Requires Python3

import jsonschema

class SHJsonValidator:

    def __init__(self):
        """
        Initialize a JSON validator for SH Challenge input.

        """
        self.SH_input_schema =  {
                                         "title": "SH Challenge Schema",
                                         "type": "object",
                                         "properties": {
                                             "message": {
                                                 "type": "string"
                                             },
                                             "recipients": {
                                                 "type": "array",
                                                 "minItems": 1 ,
                                                 "items": {"type": "string"},
                                                 "uniqueItems": True
                                             }
                                         },
                                         "required": ["message", "recipients"]
                                      } 

 
    def validate_input(self, SH_input):
        jsonschema.validate(SH_input, self.SH_input_schema)
        
        
