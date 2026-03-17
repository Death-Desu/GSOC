from pydantic import BaseModel, Field, AliasChoices, field_validator
from typing import Optional, Union
import ipaddress

class IntelOwlObservable(BaseModel):
    # Mapping common AI hallucinations to our strict keys
    observable_name: str = Field(
        ..., 
        validation_alias=AliasChoices('observable_name', 'ip', 'target', 'ipAddress', 'address', 'ip_str')
    )
    observable_type: str = Field(
        "ip", 
        validation_alias=AliasChoices('observable_type', 'type', 'kind', 'observable_kind')
    )
    malicious_score: Optional[Union[int, float]] = Field(
        0, 
        validation_alias=AliasChoices('malicious_score', 'score', 'abuseConfidenceScore', 'malicious')
    )
    vendor_name: str = Field(
        "unknown",
        validation_alias=AliasChoices('vendor_name', 'vendor', 'provider', 'source')
    )

    @field_validator('malicious_score', mode='before')
    @classmethod
    def scale_score(cls, v):
        """Converts floats/decimals to 0-100 integers automatically."""
        if isinstance(v, (float, int)) and v <= 1.0 and v > 0:
            return int(v * 100)
        return v