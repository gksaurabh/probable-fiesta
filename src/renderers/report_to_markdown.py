from typing import List
from src.contracts.clarity_report import ClarityReport

def render_report_md(report: ClarityReport) -> str:
    """
    Renders a ClarityReport into a readable Markdown string.
    """
    md = []
    
    # --- Title & One-Liner ---
    md.append(f"# {report.idea.title}")
    md.append(f"_{report.idea.one_liner}_")
    md.append("")
    
    # --- Verdict ---
    verdict_emoji = {
        "PURSUE": "🟢",
        "PIVOT": "🟡",
        "KILL": "🔴"
    }.get(report.recommendation.verdict.value, "⚪")
    
    md.append(f"## Verdict: {verdict_emoji} {report.recommendation.verdict.value}")
    md.append(f"**Confidence:** {report.recommendation.confidence * 100:.0f}%")
    md.append(f"**Rationale:** {report.recommendation.rationale}")
    md.append("")

    # --- Executive Summary ---
    md.append("## Executive Summary")
    md.append(report.idea.expanded_summary)
    md.append("")
    
    # --- Audience ---
    md.append("## Target Audience")
    md.append("**Primary Users:**")
    for user in report.audience.primary_users:
        md.append(f"- {user}")
    
    if report.audience.jobs_to_be_done:
        md.append("")
        md.append("**Jobs to be Done:**")
        for job in report.audience.jobs_to_be_done:
            md.append(f"- {job}")
    md.append("")

    # --- Market Analysis ---
    md.append("## Market Analysis")
    md.append(f"**Positioning:** {report.market.positioning}")
    md.append("")
    
    if report.market.competitors:
        md.append("### Competitors")
        md.append("| Competitor |")
        md.append("| :--- |")
        for comp in report.market.competitors:
            md.append(f"| {comp} |")
        md.append("")
    
    if report.market.demand_signals:
        md.append("**Demand Signals:**")
        for signal in report.market.demand_signals:
            md.append(f"- {signal}")
        md.append("")

    # --- Risks ---
    md.append("## Risks & Mitigations")
    if report.risks.top_risks:
        for i, risk in enumerate(report.risks.top_risks):
            mitigation = "N/A"
            if i < len(report.risks.mitigations):
                mitigation = report.risks.mitigations[i]
            
            md.append(f"**Risk {i+1}:** {risk}")
            md.append(f"> *Mitigation:* {mitigation}")
            md.append("")
    else:
        md.append("No major risks identified.")
        md.append("")

    # --- Execution Plan ---
    md.append("## Execution Plan")
    
    md.append("### MVP Scope")
    if report.execution.mvp_scope:
        for item in report.execution.mvp_scope:
            md.append(f"- [ ] {item}")
    else:
        md.append("No MVP scope defined.")
    md.append("")
    
    md.append("### Immediate Next Steps (2 Weeks)")
    if report.execution.two_week_plan:
        for item in report.execution.two_week_plan:
            md.append(f"1. {item}")
    else:
        md.append("No immediate steps defined.")
    md.append("")

    # --- Sources ---
    if report.sources:
        md.append("## Sources")
        for source in report.sources:
            md.append(f"- [{source.title}]({source.url})")
            if source.snippet:
                md.append(f"  - *\"{source.snippet}\"*")
        md.append("")

    return "\n".join(md)
