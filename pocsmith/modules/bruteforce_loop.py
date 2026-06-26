from .base import Module


MODULE = Module(
    name="bruteforce_loop",
    aliases=("bruteforce-loop",),
    imports=("import string", "import time"),
    functions=(
        'def bruteforce_candidates(candidates=None, delay=0):\n    # TODO: replace candidates with the target-specific search space.\n    candidates = candidates or string.ascii_letters + string.digits\n    for candidate in candidates:\n        yield candidate\n        if delay:\n            time.sleep(delay)\n\n\ndef run_bruteforce(check_candidate, candidates=None, delay=0):\n    for candidate in bruteforce_candidates(candidates, delay):\n        print(f"trying: {candidate}")\n        if check_candidate(candidate):\n            print(f"found: {candidate}")\n            return candidate\n    return None',
    ),
)
