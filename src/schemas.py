from pydantic import BaseModel, Field
from typing import List


class EvaluationCheck(BaseModel):
    passed: bool
    reason: str
    improvement: str


class EvaluationResult(BaseModel):
    overall_pass: bool

    accuracy: EvaluationCheck
    beginner_friendly: EvaluationCheck
    example_based: EvaluationCheck
    jargon_free: EvaluationCheck
    key_points: EvaluationCheck
    coherent_flow: EvaluationCheck

    failed_checks: List[str] = Field(default_factory=list)