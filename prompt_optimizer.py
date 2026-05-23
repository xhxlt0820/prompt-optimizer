#!/usr/bin/env python3
"""
Prompt Optimizer - AI Prompt Quality Analyzer & Optimizer
A utility tool for optimizing AI prompts for better results.

Usage:
    python prompt_optimizer.py "Your prompt here" --model gpt-4
    python prompt_optimizer.py --file prompt.txt --improve
    python prompt_optimizer.py --analyze "Your prompt" --verbose

Install:
    pip install prompt-optimizer
    # or
    pip install openai tiktoken

License: MIT
"""

import json
import re
import sys
from typing import Optional, Dict, List

try:
    import tiktoken
except ImportError:
    tiktoken = None

PROMPT_FRAMEWORKS = {
    "RTF": {
        "name": "Role-Task-Format",
        "description": "Assign role, define task, specify format",
        "template": "Act as a [ROLE]. Your task is to [TASK]. Format the output as [FORMAT]."
    },
    "CREATE": {
        "name": "Context-Request-Example-Action-Task-Expectation",
        "description": "Comprehensive prompt structure for complex tasks",
        "template": "Context: [SITUATION]\nRequest: [WHAT]\nExample: [FORMAT]\nAction: [STEPS]\nTask: [DETAIL]\nExpectation: [QUALITY]"
    },
    "CREATE-MORE": {
        "name": "Context-Request-Example-Action-Task-Expectation-Meta",
        "description": "Extended framework with meta-instructions",
        "template": "Context: [SITUATION]\nRequest: [WHAT]\nExample: [FORMAT]\nAction: [STEPS]\nTask: [DETAIL]\nExpectation: [QUALITY]\nMeta: [ADDITIONAL CONSTRAINTS]"
    }
}

def analyze_prompt(prompt: str) -> Dict:
    """Analyze a prompt and return quality metrics."""
    analysis = {
        "length": len(prompt),
        "word_count": len(prompt.split()),
        "has_role": bool(re.search(r'(act as|you are|imagine you|you are a)', prompt, re.IGNORECASE)),
        "has_task": bool(re.search(r'(create|write|generate|build|design|develop|analyze|summarize)', prompt, re.IGNORECASE)),
        "has_format": bool(re.search(r'(format|structure|output|json|table|markdown|bullet)', prompt, re.IGNORECASE)),
        "has_example": bool(re.search(r'(example|such as|for instance|like this|e\.g\.)', prompt, re.IGNORECASE)),
        "has_constraint": bool(re.search(r'(do not|don\'t|avoid|must|should|only|no more than)', prompt, re.IGNORECASE)),
        "has_context": bool(re.search(r'(context|background|situation|scenario|context is|given that)', prompt, re.IGNORECASE)),
        "has_examples": len(re.findall(r'(example|instance|sample)', prompt, re.IGNORECASE)),
        "has_steps": bool(re.search(r'(step|first|then|next|finally|begin by)', prompt, re.IGNORECASE)),
        "sentences": len(re.split(r'[.!?]+', prompt)),
        "avg_word_length": sum(len(w) for w in prompt.split()) / max(len(prompt.split()), 1),
    }
    
    # Calculate quality score (0-100)
    score = 0
    score += min(20, analysis["word_count"] / 5)  # Up to 20 for length
    score += 15 if analysis["has_role"] else 0
    score += 15 if analysis["has_task"] else 0
    score += 10 if analysis["has_format"] else 0
    score += 10 if analysis["has_example"] else 0
    score += 10 if analysis["has_constraint"] else 0
    score += 10 if analysis["has_context"] else 0
    score += 5 if analysis["has_steps"] else 0
    score = min(100, score)
    
    analysis["quality_score"] = round(score, 1)
    
    # Identify improvement areas
    improvements = []
    if not analysis["has_role"]:
        improvements.append("Add a role/persona for the AI to adopt")
    if not analysis["has_format"]:
        improvements.append("Specify the output format (JSON, markdown, etc.)")
    if not analysis["has_example"]:
        improvements.append("Provide an example of desired output")
    if not analysis["has_constraint"]:
        improvements.append("Add constraints to guide the output quality")
    if not analysis["has_context"]:
        improvements.append("Provide context for the AI to understand the situation")
    if not analysis["has_steps"]:
        improvements.append("Break down complex tasks into step-by-step instructions")
    if analysis["quality_score"] < 50:
        improvements.append("Consider using a structured prompt framework (RTF or CREATE)")
    
    analysis["improvements"] = improvements
    analysis["score_label"] = (
        "Excellent" if score >= 80 else
        "Good" if score >= 60 else
        "Fair" if score >= 40 else
        "Needs Improvement"
    )
    
    return analysis


def optimize_prompt(prompt: str, framework: str = "RTF") -> str:
    """Optimize a prompt using a selected framework."""
    framework_map = {
        "RTF": PROMPT_FRAMEWORKS["RTF"]["template"],
        "CREATE": PROMPT_FRAMEWORKS["CREATE"]["template"],
        "CREATE-MORE": PROMPT_FRAMEWORKS["CREATE-MORE"]["template"]
    }
    
    template = framework_map.get(framework, framework_map["RTF"])
    
    # Extract key components from the prompt
    words = prompt.split()
    
    # Simple keyword extraction for role
    role_keywords = ['developer', 'engineer', 'writer', 'analyst', 'designer', 'consultant', 'expert']
    role = None
    for kw in role_keywords:
        if kw in prompt.lower():
            role = kw
            break
    
    # Generate optimized prompt
    if role:
        optimized = template.replace("[ROLE]", role)
    else:
        optimized = template.replace("[ROLE]", "expert")
    
    # Replace other placeholders with original prompt context
    optimized = optimized.replace("[TASK]", prompt[:100])
    optimized = optimized.replace("[FORMAT]", "clear, structured output")
    
    return optimized


def get_token_estimate(prompt: str) -> int:
    """Estimate token count for a prompt."""
    if tiktoken:
        try:
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(prompt))
        except:
            pass
    # Fallback: rough estimate
    return len(prompt) / 4


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Prompt Optimizer - AI Prompt Quality Analyzer & Optimizer")
        print()
        print("Usage:")
        print("  python prompt_optimizer.py <prompt>")
        print("  python prompt_optimizer.py <prompt> --framework RTF|CREATE|CREATE-MORE")
        print("  python prompt_optimizer.py <prompt> --improve")
        print("  python prompt_optimizer.py <prompt> --analyze --verbose")
        print()
        print("Examples:")
        print("  python prompt_optimizer.py "Write a blog about Python" --improve")
        print("  python prompt_optimizer.py "Code a web scraper" --framework CREATE")
        return
    
    prompt = " ".join(sys.argv[1:])
    framework = "RTF"
    improve = False
    verbose = False
    
    if "--improve" in sys.argv:
        improve = True
    if "--verbose" in sys.argv:
        verbose = True
    if "--framework" in sys.argv:
        idx = sys.argv.index("--framework")
        if idx + 1 < len(sys.argv):
            framework = sys.argv[idx + 1]
    
    # Analyze
    analysis = analyze_prompt(prompt)
    
    print("=" * 60)
    print("  📊 Prompt Quality Analysis")
    print("=" * 60)
    print(f"  Score:     {analysis['quality_score']}/100 ({analysis['score_label']})")
    print(f"  Length:    {analysis['length']} chars, {analysis['word_count']} words")
    print(f"  Tokens:    ~{get_token_estimate(prompt)}")
    print()
    print("  Components:")
    print(f"    ✓ Role:      {'Yes' if analysis['has_role'] else 'No'}")
    print(f"    ✓ Task:      {'Yes' if analysis['has_task'] else 'No'}")
    print(f"    ✓ Format:    {'Yes' if analysis['has_format'] else 'No'}")
    print(f"    ✓ Example:   {'Yes' if analysis['has_example'] else 'No'}")
    print(f"    ✓ Constraint:{'Yes' if analysis['has_constraint'] else 'No'}")
    print(f"    ✓ Context:   {'Yes' if analysis['has_context'] else 'No'}")
    print()
    
    if analysis["improvements"]:
        print("  💡 Improvements:")
        for imp in analysis["improvements"]:
            print(f"    → {imp}")
    
    if improve:
        print()
        print("  ✨ Optimized Prompt:")
        print("=" * 60)
        optimized = optimize_prompt(prompt, framework)
        print(optimized)
        print("=" * 60)
    
    if verbose:
        print()
        print("  📋 Full Analysis (JSON):")
        print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
