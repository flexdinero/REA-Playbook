"""Provider-neutral selection over explicitly supplied task-level qualifications.

This is a policy helper, not a model gateway or a benchmark measurement engine.
The caller owns current price/quality evidence and account availability.
"""

import math
from .storage import check


def select_model(candidates, required_capabilities, budget_per_task):
    check(isinstance(budget_per_task, (float, int)) and math.isfinite(budget_per_task) and budget_per_task >= 0, 'invalid task budget')
    eligible = []
    for item in candidates:
        cost = item.get('cost_per_task')
        check(type(cost) in (int, float) and math.isfinite(cost) and cost >= 0, 'invalid candidate cost')
        if item.get('quality_passed') is True and set(required_capabilities) <= set(item['capabilities']) and cost <= budget_per_task:
            eligible.append(item)
    check(eligible, 'no qualified model within budget; improve evidence, raise budget or hand off explicitly')
    return min(eligible, key=lambda item: (item['cost_per_task'], item['id']))
