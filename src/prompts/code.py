PATCH_PROMPT = """
You are a Python security engineer.

Vulnerability

{vuln}

Plan

{plan}

Repository Code

{snippet}

Return ONLY the modified code.

"""
