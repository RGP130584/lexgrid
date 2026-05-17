import pytest
import numpy as np
from ai_ops.embeddings.poisoning_detector import EmbeddingPoisoningDetector
from ai_ops.evaluation.hallucination_tests import HallucinationEvaluator
from ai_ops.governance.ai_risk_matrix import AIRiskMatrix, AIRiskLevel
from ai_ops.prompt_governance.prompt_registry import PromptGovernance

def test_embedding_poisoning_detection():
    # Vetor normal (norma ~ 1.0)
    safe_vector = [0.1, 0.2, 0.3, 0.4, 0.8]
    assert EmbeddingPoisoningDetector.is_vector_safe(safe_vector) is True
    
    # Vetor anômalo / Envenenado (Norma Extrema)
    poisoned_vector = [999.0, -999.0, 0.0]
    assert EmbeddingPoisoningDetector.is_vector_safe(poisoned_vector) is False

def test_hallucination_evaluator():
    context = "A empresa pagou R$ 500 em tributos."
    # Resposta coerente e ancorada
    good_response = "A empresa recolheu tributos no valor de R$ 500."
    score_good = HallucinationEvaluator.evaluate_groundedness(context, good_response)
    
    # Resposta não ancorada (Alucinação)
    bad_response = "O presidente vendeu 1000 ações no mercado europeu."
    score_bad = HallucinationEvaluator.evaluate_groundedness(context, bad_response)
    
    assert score_good > score_bad
    assert score_bad == 0.0

def test_prompt_approval_separation_of_duties():
    version = PromptGovernance.create_prompt("tax_analyzer", "System: You are tax agent", "dev_joao", "CRITICAL")
    
    # Owner não pode aprovar seu próprio prompt crítico (Segregação de funções)
    with pytest.raises(PermissionError):
        PromptGovernance.approve_prompt("tax_analyzer", version, "dev_joao")
        
    # Manager consegue aprovar
    PromptGovernance.approve_prompt("tax_analyzer", version, "manager_maria")