from datetime import datetime

# Phase distribution percentages by project type
PHASE_DISTRIBUTIONS = {
    "software": {
        "Planning":               0.08,
        "Requirements Analysis":  0.12,
        "System Design":          0.15,
        "Development":            0.35,
        "Testing":                0.15,
        "Deployment":             0.07,
        "Documentation":          0.05,
        "Reporting":              0.03,
    },
    "research": {
        "Planning":               0.10,
        "Requirements Analysis":  0.18,
        "System Design":          0.10,
        "Development":            0.25,
        "Testing":                0.10,
        "Deployment":             0.05,
        "Documentation":          0.12,
        "Reporting":              0.10,
    },
    "departmental": {
        "Planning":               0.12,
        "Requirements Analysis":  0.15,
        "System Design":          0.12,
        "Development":            0.28,
        "Testing":                0.12,
        "Deployment":             0.08,
        "Documentation":          0.08,
        "Reporting":              0.05,
    },
}

# Complexity multipliers
COMPLEXITY_MULTIPLIERS = {
    "low":    0.75,
    "medium": 1.00,
    "high":   1.40,
    "critical": 1.80,
}

# Base effort (person-hours) per size unit
SIZE_BASE_HOURS = {
    "small":      200,
    "medium":     500,
    "large":     1200,
    "enterprise": 2500,
}

# Recommended staffing per size
RECOMMENDED_STAFF = {
    "small":      2,
    "medium":     4,
    "large":      8,
    "enterprise": 15,
}


def calculate_project_estimates(data: dict) -> dict:
    project_type   = data.get("project_type", "software").lower()
    size           = data.get("project_size", "medium").lower()
    complexity     = data.get("complexity", "medium").lower()
    num_staff      = int(data.get("num_staff", 4))
    hours_per_day  = float(data.get("hours_per_day", 8))
    hourly_rate    = float(data.get("hourly_rate", 25))

    # Base effort
    base_hours = SIZE_BASE_HOURS.get(size, 500)
    complexity_mult = COMPLEXITY_MULTIPLIERS.get(complexity, 1.0)
    total_effort_hours = base_hours * complexity_mult

    # Duration in working days
    daily_team_hours = num_staff * hours_per_day
    duration_days = total_effort_hours / daily_team_hours
    duration_weeks = duration_days / 5
    duration_months = duration_weeks / 4.33

    # Recommended staffing
    recommended_staff = RECOMMENDED_STAFF.get(size, 4)

    # Budget
    total_labour_cost = total_effort_hours * hourly_rate
    contingency = total_labour_cost * 0.10
    total_budget = total_labour_cost + contingency

    # Phase distribution
    phases = PHASE_DISTRIBUTIONS.get(project_type, PHASE_DISTRIBUTIONS["software"])
    phase_breakdown = {}
    for phase, pct in phases.items():
        phase_hours = round(total_effort_hours * pct, 1)
        phase_days  = round(phase_hours / daily_team_hours, 1)
        phase_cost  = round(phase_hours * hourly_rate, 2)
        phase_breakdown[phase] = {
            "percentage": round(pct * 100, 1),
            "hours":      phase_hours,
            "days":       phase_days,
            "cost":       phase_cost,
        }

    return {
        "total_effort_hours":   round(total_effort_hours, 1),
        "duration_days":        round(duration_days, 1),
        "duration_weeks":       round(duration_weeks, 1),
        "duration_months":      round(duration_months, 1),
        "recommended_staff":    recommended_staff,
        "total_labour_cost":    round(total_labour_cost, 2),
        "contingency":          round(contingency, 2),
        "total_budget":         round(total_budget, 2),
        "phase_breakdown":      phase_breakdown,
        "complexity_multiplier": complexity_mult,
        "base_hours":           base_hours,
    }


def generate_report_text(data: dict, result: dict) -> str:
    now  = datetime.now().strftime("%d %B %Y, %H:%M")
    ref  = f"MTN-UG-PPE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    sep  = "=" * 72
    sep2 = "-" * 72

    lines = [
        sep,
        "   ███╗   ███╗████████╗███╗   ██╗    ██╗   ██╗ ██████╗  █████╗ ███╗   ██╗██████╗  █████╗ ",
        "   ████╗ ████║╚══██╔══╝████╗  ██║    ██║   ██║██╔════╝ ██╔══██╗████╗  ██║██╔══██╗██╔══██╗",
        "   ██╔████╔██║   ██║   ██╔██╗ ██║    ██║   ██║██║  ███╗███████║██╔██╗ ██║██║  ██║███████║",
        "   ██║╚██╔╝██║   ██║   ██║╚██╗██║    ██║   ██║██║   ██║██╔══██║██║╚██╗██║██║  ██║██╔══██║",
        "   ██║ ╚═╝ ██║   ██║   ██║ ╚████║    ╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║",
        "   ╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═══╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝",
        sep,
        "              PROJECT PLANNING & ESTIMATION REPORT",
        sep,
        f"  Generated On  : {now}",
        f"  Report Ref    : {ref}",
        f"  Organisation  : MTN Uganda Limited",
        sep,
        "",
        "  PROJECT DETAILS",
        sep2,
        f"  Project Title      : {data.get('project_title', 'N/A')}",
        f"  Department         : {data.get('department', 'N/A')}",
        f"  Project Manager    : {data.get('project_manager', 'N/A')}",
        f"  Project Type       : {data.get('project_type', 'N/A').capitalize()}",
        f"  Project Size       : {data.get('project_size', 'N/A').capitalize()}",
        f"  Complexity Level   : {data.get('complexity', 'N/A').capitalize()}",
        f"  Number of Staff    : {data.get('num_staff', 'N/A')}",
        f"  Working Hours/Day  : {data.get('hours_per_day', 'N/A')} hrs",
        f"  Hourly Rate        : UGX {float(data.get('hourly_rate', 0)):,.0f}",
        "",
        "  ASSUMPTIONS",
        sep2,
        f"  • Base effort for '{data.get('project_size','').capitalize()}' size project  : {result['base_hours']} person-hours",
        f"  • Complexity multiplier ({data.get('complexity','').capitalize()})            : x{result['complexity_multiplier']}",
        f"  • Daily team capacity ({data.get('num_staff')} staff x {data.get('hours_per_day')} hrs)   : {int(data.get('num_staff',4)) * float(data.get('hours_per_day',8))} hrs/day",
        f"  • Contingency reserve                                  : 10%",
        f"  • All estimates based on MTN Uganda project standards.",
        "",
        "  EFFORT & DURATION ESTIMATES",
        sep2,
        f"  Total Effort Required    : {result['total_effort_hours']} person-hours",
        f"  Estimated Duration       : {result['duration_days']} working days",
        f"                           : {result['duration_weeks']} weeks",
        f"                           : {result['duration_months']} months (approx.)",
        f"  Recommended Staffing     : {result['recommended_staff']} staff members",
        "",
        "  BUDGET SUMMARY",
        sep2,
        f"  Total Labour Cost        : UGX {result['total_labour_cost']:>18,.0f}",
        f"  Contingency (10%)        : UGX {result['contingency']:>18,.0f}",
        f"  {'─'*50}",
        f"  TOTAL PROJECT BUDGET     : UGX {result['total_budget']:>18,.0f}",
        "",
        "  PHASE-BY-PHASE EFFORT DISTRIBUTION",
        sep2,
        f"  {'Phase':<28} {'%':>5}  {'Hours':>8}  {'Days':>6}  {'Cost (UGX)':>18}",
        f"  {'─'*28} {'─'*5}  {'─'*8}  {'─'*6}  {'─'*18}",
    ]

    for phase, info in result["phase_breakdown"].items():
        lines.append(
            f"  {phase:<28} {info['percentage']:>4.1f}%  {info['hours']:>8.1f}  {info['days']:>6.1f}  {info['cost']:>18,.0f}"
        )

    lines += [
        f"  {'─'*28} {'─'*5}  {'─'*8}  {'─'*6}  {'─'*18}",
        f"  {'TOTAL':<28} {'100.0':>5}%  {result['total_effort_hours']:>8.1f}  {result['duration_days']:>6.1f}  {result['total_labour_cost']:>18,.0f}",
        "",
        sep,
        "  NOTES & RECOMMENDATIONS",
        sep2,
        "  1. Estimates are based on industry-standard benchmarks adapted for",
        "     MTN Uganda project delivery guidelines.",
        "  2. Actual effort may vary based on team experience and scope changes.",
        "  3. A 10% contingency reserve has been included to cover unforeseen risks.",
        "  4. Regular milestone reviews are recommended at the end of each phase.",
        "  5. All estimates assume full-time staff availability during working hours.",
        "  6. This report should be reviewed and approved by the Project Manager",
        "     before project commencement.",
        "",
        sep,
        "  © MTN Uganda Limited — Project Planning & Estimation Tool",
        "  This report is confidential and intended for internal use only.",
        "  Unauthorised distribution is strictly prohibited.",
        sep,
    ]

    return "\n".join(lines)
