from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import re

app = FastAPI()

class ValidateRequest(BaseModel):
    data: Dict[str, Any]
    rules: Optional[Dict[str, str]] = None

class ValidationError(BaseModel):
    field: str
    error: str

class ValidateResponse(BaseModel):
    valid: bool
    errors: List[ValidationError]
    checked_fields: int

def validate_email(value: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(value)))

def validate_phone(value: str) -> bool:
    # Saudi phone format
    pattern = r'^(\+966|966|05|5)[0-9]{8,9}$'
    cleaned = re.sub(r'[\s\-\(\)]', '', str(value))
    return bool(re.match(pattern, cleaned))

def validate_url(value: str) -> bool:
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, str(value)))

def validate_required(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    return True

def validate_number(value: Any) -> bool:
    try:
        float(value)
        return True
    except:
        return False

def validate_min_length(value: str, min_len: int) -> bool:
    return len(str(value)) >= min_len

def validate_max_length(value: str, max_len: int) -> bool:
    return len(str(value)) <= max_len

VALIDATORS = {
    "email": validate_email,
    "phone": validate_phone,
    "url": validate_url,
    "required": validate_required,
    "number": validate_number,
}

@app.post("/api/validate")
async def validate(request: ValidateRequest) -> ValidateResponse:
    """التحقق من صحة البيانات"""
    try:
        errors = []
        checked = 0
        
        rules = request.rules or {}
        
        # Auto-detect rules if not provided
        if not rules:
            for field, value in request.data.items():
                if 'email' in field.lower():
                    rules[field] = 'email'
                elif 'phone' in field.lower() or 'mobile' in field.lower():
                    rules[field] = 'phone'
                elif 'url' in field.lower() or 'link' in field.lower():
                    rules[field] = 'url'
                else:
                    rules[field] = 'required'
        
        for field, rule_str in rules.items():
            value = request.data.get(field)
            checked += 1
            
            # Parse rules (e.g., "required|email|min:5")
            field_rules = rule_str.split('|')
            
            for rule in field_rules:
                rule = rule.strip()
                
                if ':' in rule:
                    rule_name, param = rule.split(':', 1)
                    if rule_name == 'min':
                        if not validate_min_length(value or '', int(param)):
                            errors.append(ValidationError(
                                field=field,
                                error=f"Minimum length is {param}"
                            ))
                    elif rule_name == 'max':
                        if not validate_max_length(value or '', int(param)):
                            errors.append(ValidationError(
                                field=field,
                                error=f"Maximum length is {param}"
                            ))
                else:
                    validator = VALIDATORS.get(rule)
                    if validator and not validator(value):
                        errors.append(ValidationError(
                            field=field,
                            error=f"Invalid {rule}"
                        ))
        
        return ValidateResponse(
            valid=len(errors) == 0,
            errors=errors,
            checked_fields=checked
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/validate")
async def validate_info():
    return {
        "name": "Data Validator",
        "description": "التحقق من صحة البيانات",
        "price": "$0.02/request",
        "method": "POST",
        "body": {
            "data": {"field": "value"},
            "rules": {"field": "required|email"}
        },
        "available_rules": ["required", "email", "phone", "url", "number", "min:N", "max:N"]
    }
