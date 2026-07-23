"""
================================================================================
UI_COMPONENTS.PY — Modernized CSS, Metric Cards & Sidebar Filters
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
Premium UI layer implementing:
  - Complete CSS overhaul: glassmorphism, gradient headers, animated cards
  - Google Font (Inter) integration
  - Dark sidebar theme (#0F172A)
  - Reusable metric card & student profile card components
  - Advanced multi-parameter sidebar filter panel
================================================================================
"""

import streamlit as st
import pandas as pd

from config import COLORS


# ==============================================================================
# CUSTOM CSS INJECTION — Complete UI Overhaul
# ==============================================================================

def inject_custom_css():
    """
    Injects the complete custom CSS theme into the Streamlit page.
    Must be called once at the top of main.py after st.set_page_config().
    """
    st.markdown(f"""
    <style>
        /* ── Google Font Import ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Global Typography ── */
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        /* ── Sidebar Dark Theme ── */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['bg_dark']} 0%, #1E293B 100%) !important;
            color: #E2E8F0 !important;
            border-right: 3px solid {COLORS['primary']} !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{
            color: #CBD5E1 !important;
        }}
        section[data-testid="stSidebar"] .stRadio label:hover {{
            color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: #F1F5F9 !important;
        }}

        /* ── Main Content Area ── */
        .main .block-container {{
            padding-top: 2rem;
            max-width: 1200px;
        }}

        /* ── Hero Header ── */
        .hero-header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 0.2rem;
            line-height: 1.2;
        }}
        .hero-subtitle {{
            font-size: 1.05rem;
            color: {COLORS['text_muted']};
            margin-bottom: 1.8rem;
            font-weight: 400;
        }}

        /* ── Glassmorphism Metric Cards ── */
        .metric-card {{
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.6);
            border-radius: 16px;
            padding: 1.3rem 1.1rem;
            text-align: center;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 16px 16px 0 0;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15);
        }}
        .metric-card .metric-icon {{
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }}
        .metric-card .metric-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {COLORS['text_primary']};
            line-height: 1.1;
        }}
        .metric-card .metric-label {{
            font-size: 0.78rem;
            color: {COLORS['text_muted']};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.3rem;
        }}
        .metric-card .metric-delta {{
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 0.2rem;
        }}

        /* Card accent colors */
        .metric-card.indigo::before {{ background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']}); }}
        .metric-card.emerald::before {{ background: linear-gradient(90deg, {COLORS['success']}, #34D399); }}
        .metric-card.amber::before {{ background: linear-gradient(90deg, {COLORS['warning']}, #FBBF24); }}
        .metric-card.rose::before {{ background: linear-gradient(90deg, {COLORS['danger']}, #FB7185); }}
        .metric-card.cyan::before {{ background: linear-gradient(90deg, {COLORS['info']}, #22D3EE); }}

        /* ── Subject / Content Cards ── */
        .content-card {{
            background: linear-gradient(135deg, #FAFBFF 0%, #F0F4FF 100%);
            border-left: 5px solid {COLORS['primary']};
            padding: 1.4rem 1.6rem;
            border-radius: 12px;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
            transition: all 0.25s ease;
        }}
        .content-card:hover {{
            box-shadow: 0 6px 24px rgba(79, 70, 229, 0.1);
        }}
        .content-card h4 {{
            color: {COLORS['primary_dark']};
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        /* ── Example Box ── */
        .example-box {{
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
            border-left: 4px solid {COLORS['success']};
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #334155;
            margin: 10px 0 14px 0;
        }}

        /* ── Alert Cards ── */
        .alert-card {{
            background: linear-gradient(135deg, #FFF5F5 0%, #FEF2F2 100%);
            border: 1px solid #FECACA;
            border-left: 4px solid {COLORS['danger']};
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }}
        .alert-card:hover {{
            box-shadow: 0 4px 16px rgba(244, 63, 94, 0.1);
        }}

        /* ── Risk Badges ── */
        .badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}
        .badge-safe {{
            background: #D1FAE5;
            color: #065F46;
        }}
        .badge-watch {{
            background: #FEF3C7;
            color: #92400E;
        }}
        .badge-critical {{
            background: #FEE2E2;
            color: #991B1B;
        }}
        .badge-high {{
            background: #D1FAE5;
            color: #065F46;
        }}
        .badge-moderate {{
            background: #FEF3C7;
            color: #92400E;
        }}
        .badge-atrisk {{
            background: #FEE2E2;
            color: #991B1B;
        }}

        /* ── Student Profile Card ── */
        .student-profile {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        }}
        .student-profile .profile-name {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
        }}
        .student-profile .profile-roll {{
            font-size: 0.9rem;
            color: {COLORS['text_muted']};
        }}
        .student-profile .profile-stat {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #F1F5F9;
            font-size: 0.92rem;
        }}

        /* ── Section Headers ── */
        .section-header {{
            font-size: 1.4rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {COLORS['primary']};
            margin-bottom: 1rem;
            display: inline-block;
        }}

        /* ── Admin Panel Styles ── */
        .admin-status-present {{
            color: {COLORS['success']};
            font-weight: 600;
        }}
        .admin-status-absent {{
            color: {COLORS['danger']};
            font-weight: 600;
        }}
        .threshold-warning {{
            background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
            border: 1px solid #FDE68A;
            border-left: 4px solid {COLORS['warning']};
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }}

        /* ── Scrollable Table Enhancement ── */
        .stDataFrame {{ border-radius: 12px; overflow: hidden; }}

        /* ── Tab Styling ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;
            font-weight: 600;
        }}
    </style>
    """, unsafe_allow_html=True)


# ==============================================================================
# REUSABLE METRIC CARD COMPONENT
# ==============================================================================

def render_metric_card(
    icon: str, value: str, label: str,
    delta: str = None, accent: str = "indigo"
):
    """
    Renders a glassmorphism-styled KPI metric card.

    Args:
        icon: Emoji icon to display (e.g., "👥").
        value: The main metric value (e.g., "80").
        label: Description label below the value (e.g., "Total Students").
        delta: Optional delta indicator (e.g., "-12" for negative change).
        accent: CSS accent class: indigo | emerald | amber | rose | cyan.
    """
    delta_html = ""
    if delta is not None:
        delta_color = COLORS['success'] if not delta.startswith('-') else COLORS['danger']
        delta_html = f'<div class="metric-delta" style="color:{delta_color};">{delta}</div>'

    st.markdown(f"""
    <div class="metric-card {accent}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# RISK BADGE COMPONENT
# ==============================================================================

def get_risk_badge_html(risk_level: str) -> str:
    """Returns HTML for a colored risk badge pill."""
    badge_map = {
        "Safe": "badge-safe",
        "Watch": "badge-watch",
        "Critical": "badge-critical",
        "High Achievers": "badge-high",
        "Moderate Learners": "badge-moderate",
        "At-Risk & Backlog Vulnerable": "badge-atrisk",
    }
    css_class = badge_map.get(risk_level, "badge-watch")
    return f'<span class="badge {css_class}">{risk_level}</span>'


# ==============================================================================
# STUDENT PROFILE CARD
# ==============================================================================

def render_student_profile_card(student: pd.Series):
    """
    Renders a detailed student profile card with key stats and risk badge.

    Args:
        student: A single row from the student DataFrame.
    """
    cohort = student.get('Cohort', 'N/A')
    cohort_badge = get_risk_badge_html(cohort)

    risk = student.get('Risk_Level', '')
    risk_badge = get_risk_badge_html(risk) if risk else ''

    st.markdown(f"""
    <div class="student-profile">
        <div class="profile-name">{student['Student_Name']}</div>
        <div class="profile-roll">{student['Roll_No']} &middot; {student['Gender']}</div>
        <hr style="margin: 0.8rem 0; border-color: #F1F5F9;">
        <div class="profile-stat"><span>Overall Attendance</span><strong>{student['Overall_Attendance_Pct']}%</strong></div>
        <div class="profile-stat"><span>Composite Score</span><strong>{student.get('Composite_Score', 'N/A'):.1f}%</strong></div>
        <div class="profile-stat"><span>Backlogs</span><strong>{int(student['Backlogs'])}</strong></div>
        <div class="profile-stat"><span>Growth Trajectory</span><strong>{student.get('Trajectory', 'N/A')}</strong></div>
        <div class="profile-stat"><span>K-Means Cohort</span>{cohort_badge}</div>
        {'<div class="profile-stat"><span>Predicted Risk</span>' + risk_badge + '</div>' if risk else ''}
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# ADVANCED SIDEBAR FILTERS
# ==============================================================================

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders an advanced multi-parameter filter panel in the sidebar
    and returns the filtered DataFrame.

    Filters:
        - Gender (multiselect)
        - Attendance Range (slider)
        - Backlog Count (select_slider 0-4)
        - Risk Cohort (multiselect)

    Args:
        df: The full student DataFrame (must have Cohort column).

    Returns:
        pd.DataFrame: Filtered subset of the input DataFrame.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Advanced Filters")

    # Gender filter
    gender_options = sorted(df['Gender'].unique().tolist())
    gender_sel = st.sidebar.multiselect(
        "Gender",
        options=gender_options,
        default=gender_options,
        key="filter_gender"
    )

    # Attendance range slider
    att_min = float(df['Overall_Attendance_Pct'].min())
    att_max = float(df['Overall_Attendance_Pct'].max())
    att_range = st.sidebar.slider(
        "Attendance Range (%)",
        min_value=att_min,
        max_value=att_max,
        value=(att_min, att_max),
        step=1.0,
        key="filter_attendance"
    )

    # Backlog count range
    max_backlogs = int(df['Backlogs'].max())
    backlog_range = st.sidebar.select_slider(
        "Backlog Count",
        options=list(range(0, max_backlogs + 1)),
        value=(0, max_backlogs),
        key="filter_backlogs"
    )

    # Cohort filter
    if 'Cohort' in df.columns:
        cohort_options = sorted(df['Cohort'].unique().tolist())
        cohort_sel = st.sidebar.multiselect(
            "Risk Cohort",
            options=cohort_options,
            default=cohort_options,
            key="filter_cohort"
        )
    else:
        cohort_sel = None

    # Apply all filters
    filtered = df[
        (df['Gender'].isin(gender_sel)) &
        (df['Overall_Attendance_Pct'] >= att_range[0]) &
        (df['Overall_Attendance_Pct'] <= att_range[1]) &
        (df['Backlogs'] >= backlog_range[0]) &
        (df['Backlogs'] <= backlog_range[1])
    ]

    if cohort_sel is not None and 'Cohort' in df.columns:
        filtered = filtered[filtered['Cohort'].isin(cohort_sel)]

    st.sidebar.caption(f"Showing {len(filtered)} of {len(df)} students")

    return filtered
