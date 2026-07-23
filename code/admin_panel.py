"""
================================================================================
ADMIN_PANEL.PY — Smart Admin & Daily Attendance Management System
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
[NEW Feature: Admin Panel]
Provides:
  - Student roster management table (view/search all 80 students)
  - Daily attendance marking interface (date picker → checkbox grid → save)
  - Auto-generated Daily Present List and Daily Absent List with counts
  - Faculty Remarks text input for each absent student
  - Attendance threshold monitor: students below 75% auto-flagged
  - Cumulative attendance tracker from daily entries
================================================================================
"""

import datetime
import pandas as pd
import streamlit as st

from config import JNTUK_ATTENDANCE_CUTOFF
from data_loader import load_daily_attendance, save_daily_attendance, get_student_cumulative_attendance
from ui_components import render_metric_card


def render_admin_panel(df: pd.DataFrame):
    """
    Main entry point for the Admin Panel tab.
    Renders the complete admin interface with three sub-sections:
        1. Student Roster & Search
        2. Daily Attendance Marking
        3. Attendance Threshold Alerts

    Args:
        df: Full student DataFrame (requires Roll_No, Student_Name, Gender,
            Overall_Attendance_Pct, Backlogs columns).
    """
    st.markdown(
        '<p class="hero-header">Admin Panel & Daily Attendance</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="hero-subtitle">Manage student roster, mark daily attendance, '
        'and monitor JNTUK 75% threshold compliance</p>',
        unsafe_allow_html=True
    )

    # Sub-navigation within Admin Panel
    admin_tab1, admin_tab2, admin_tab3 = st.tabs([
        "Student Roster",
        "Mark Daily Attendance",
        "Threshold Alerts & Reports"
    ])

    with admin_tab1:
        _render_student_roster(df)

    with admin_tab2:
        _render_daily_attendance_marker(df)

    with admin_tab3:
        _render_threshold_alerts(df)


# ==============================================================================
# SUB-SECTION 1: STUDENT ROSTER
# ==============================================================================

def _render_student_roster(df: pd.DataFrame):
    """Displays the full 80-student roster with search functionality."""
    st.markdown('<div class="section-header">Student Roster (80 Students)</div>',
                unsafe_allow_html=True)

    # Search bar
    search_query = st.text_input(
        "Search by Name or Roll No",
        placeholder="e.g., Ananya or 25A91A4201",
        key="roster_search"
    )

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("👥", str(len(df)), "Total Students", accent="indigo")
    with c2:
        girls = len(df[df['Gender'] == 'Female'])
        render_metric_card("👩", str(girls), "Girls", accent="rose")
    with c3:
        boys = len(df[df['Gender'] == 'Male'])
        render_metric_card("👨", str(boys), "Boys", accent="cyan")
    with c4:
        below_75 = len(df[df['Overall_Attendance_Pct'] < JNTUK_ATTENDANCE_CUTOFF])
        render_metric_card("⚠️", str(below_75), "Below 75%", accent="amber")

    st.markdown("<br>", unsafe_allow_html=True)

    # Apply search filter
    display_df = df.copy()
    if search_query:
        mask = (
            display_df['Student_Name'].str.contains(search_query, case=False, na=False) |
            display_df['Roll_No'].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    # Display roster table
    roster_cols = [
        'Roll_No', 'Student_Name', 'Gender',
        'Overall_Attendance_Pct', 'Lab_Attendance_Pct', 'Backlogs'
    ]
    available_cols = [c for c in roster_cols if c in display_df.columns]

    st.dataframe(
        display_df[available_cols].style.format({
            'Overall_Attendance_Pct': '{:.1f}%',
            'Lab_Attendance_Pct': '{:.1f}%',
        }).apply(
            lambda row: [
                'background-color: #FEF2F2' if row.get('Overall_Attendance_Pct', 100) < 75
                else '' for _ in row
            ], axis=1
        ),
        use_container_width=True,
        height=400,
    )

    st.caption(f"Showing {len(display_df)} of {len(df)} students")


# ==============================================================================
# SUB-SECTION 2: DAILY ATTENDANCE MARKING
# ==============================================================================

def _render_daily_attendance_marker(df: pd.DataFrame):
    """Interactive daily attendance marking interface with remarks."""
    st.markdown(
        '<div class="section-header">Mark Daily Attendance</div>',
        unsafe_allow_html=True
    )

    # Date selector
    selected_date = st.date_input(
        "Select Date",
        value=datetime.date.today(),
        max_value=datetime.date.today(),
        key="att_date"
    )
    date_key = selected_date.strftime("%Y-%m-%d")

    # Load existing data
    daily_data = load_daily_attendance()
    existing_entry = daily_data.get(date_key, {})

    st.info(
        f"Marking attendance for **{selected_date.strftime('%A, %B %d, %Y')}**. "
        f"{'(Previously saved data loaded)' if existing_entry else '(No previous data for this date)'}"
    )

    # Attendance marking form
    with st.form(key=f"attendance_form_{date_key}"):
        st.markdown("#### Mark Present Students")
        st.caption("Check the box for each student who is PRESENT. Unchecked = Absent.")

        # Create columns for the checklist
        attendance_status = {}
        remark_fields = {}

        # Split into chunks for better layout
        students = df[['Roll_No', 'Student_Name', 'Gender']].to_dict('records')

        for i in range(0, len(students), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= len(students):
                    break
                s = students[idx]
                roll = s['Roll_No']

                with col:
                    # Default to existing status if available
                    default_present = existing_entry.get(roll, {}).get('status', 'Present') == 'Present'

                    is_present = st.checkbox(
                        f"{s['Roll_No']} — {s['Student_Name']}",
                        value=default_present,
                        key=f"att_{date_key}_{roll}"
                    )
                    attendance_status[roll] = 'Present' if is_present else 'Absent'

        st.markdown("---")
        st.markdown("#### Faculty Remarks for Absent Students")
        st.caption("Optionally add remarks for students marked absent.")

        # Show remark fields for students marked absent
        absent_rolls = [r for r, s in attendance_status.items() if s == 'Absent']
        if absent_rolls:
            for roll in absent_rolls:
                name = df[df['Roll_No'] == roll]['Student_Name'].values[0]
                existing_remark = existing_entry.get(roll, {}).get('remark', '')
                remark_fields[roll] = st.text_input(
                    f"Remark for {name} ({roll})",
                    value=existing_remark,
                    key=f"remark_{date_key}_{roll}",
                    placeholder="e.g., Medical leave, Prior permission, No information"
                )
        else:
            st.success("All students marked as present!")

        # Submit button
        submitted = st.form_submit_button(
            "Save Attendance",
            type="primary",
            use_container_width=True
        )

        if submitted:
            # Build the entry for this date
            entry = {}
            for roll, status in attendance_status.items():
                entry[roll] = {
                    'status': status,
                    'remark': remark_fields.get(roll, '')
                }

            daily_data[date_key] = entry
            save_daily_attendance(daily_data)
            st.success(
                f"Attendance saved for {selected_date.strftime('%B %d, %Y')}! "
                f"Present: {sum(1 for s in entry.values() if s['status'] == 'Present')} | "
                f"Absent: {sum(1 for s in entry.values() if s['status'] == 'Absent')}"
            )

    # ── Daily Present & Absent Lists ──
    st.markdown("---")
    _render_daily_lists(df, daily_data, date_key, selected_date)


def _render_daily_lists(
    df: pd.DataFrame, daily_data: dict, date_key: str, selected_date
):
    """Renders the daily present/absent summary lists below the form."""
    entry = daily_data.get(date_key, {})
    if not entry:
        st.warning("No attendance data recorded for this date yet.")
        return

    present_rolls = [r for r, v in entry.items() if v.get('status') == 'Present']
    absent_rolls = [r for r, v in entry.items() if v.get('status') == 'Absent']

    # Summary metrics
    p1, p2, p3 = st.columns(3)
    with p1:
        render_metric_card("✅", str(len(present_rolls)), "Present Today", accent="emerald")
    with p2:
        render_metric_card("❌", str(len(absent_rolls)), "Absent Today", accent="rose")
    with p3:
        pct = (len(present_rolls) / len(entry) * 100) if entry else 0
        render_metric_card("📊", f"{pct:.0f}%", "Today's Att. Rate", accent="indigo")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"#### Daily Present List ({len(present_rolls)} students)")
        if present_rolls:
            present_df = df[df['Roll_No'].isin(present_rolls)][['Roll_No', 'Student_Name', 'Gender']]
            st.dataframe(present_df, use_container_width=True, height=250)
        else:
            st.info("No students marked present.")

    with col_b:
        st.markdown(f"#### Daily Absent List ({len(absent_rolls)} students)")
        if absent_rolls:
            absent_data = []
            for roll in absent_rolls:
                name = df[df['Roll_No'] == roll]['Student_Name'].values
                name = name[0] if len(name) > 0 else 'Unknown'
                remark = entry[roll].get('remark', '')
                absent_data.append({
                    'Roll_No': roll,
                    'Student_Name': name,
                    'Remark': remark if remark else '—'
                })
            absent_df = pd.DataFrame(absent_data)
            st.dataframe(absent_df, use_container_width=True, height=250)
        else:
            st.success("No absentees today!")


# ==============================================================================
# SUB-SECTION 3: THRESHOLD ALERTS & REPORTS
# ==============================================================================

def _render_threshold_alerts(df: pd.DataFrame):
    """
    Displays students who are below the JNTUK 75% attendance threshold
    with auto-flagged visual alerts.
    """
    st.markdown(
        '<div class="section-header">JNTUK 75% Attendance Threshold Monitor</div>',
        unsafe_allow_html=True
    )

    below_threshold = df[df['Overall_Attendance_Pct'] < JNTUK_ATTENDANCE_CUTOFF].copy()
    below_threshold = below_threshold.sort_values('Overall_Attendance_Pct', ascending=True)

    # Summary
    total = len(df)
    flagged = len(below_threshold)
    compliant = total - flagged

    m1, m2, m3 = st.columns(3)
    with m1:
        render_metric_card("✅", str(compliant), "Compliant (>=75%)", accent="emerald")
    with m2:
        render_metric_card(
            "⚠️", str(flagged), "Flagged (<75%)",
            delta=f"-{flagged} students" if flagged > 0 else "All clear",
            accent="rose"
        )
    with m3:
        if flagged > 0:
            avg_att = below_threshold['Overall_Attendance_Pct'].mean()
            render_metric_card("📉", f"{avg_att:.1f}%", "Avg Att. of Flagged", accent="amber")
        else:
            render_metric_card("🎉", "100%", "Compliance Rate", accent="emerald")

    st.markdown("<br>", unsafe_allow_html=True)

    if flagged == 0:
        st.success("All students are above the JNTUK 75% attendance threshold!")
        return

    # Alert cards for each flagged student
    st.markdown(f"#### Flagged Students ({flagged} total)")

    for _, row in below_threshold.iterrows():
        severity = "critical" if row['Overall_Attendance_Pct'] < 60 else "warning"
        icon = "🔴" if severity == "critical" else "🟡"

        st.markdown(f"""
        <div class="{'alert-card' if severity == 'critical' else 'threshold-warning'}">
            <strong>{icon} {row['Student_Name']} ({row['Roll_No']})</strong><br>
            <span>Attendance: <strong>{row['Overall_Attendance_Pct']:.1f}%</strong> 
            | Backlogs: <strong>{int(row['Backlogs'])}</strong>
            | Gender: {row['Gender']}
            | Deficit: <strong>{JNTUK_ATTENDANCE_CUTOFF - row['Overall_Attendance_Pct']:.1f}%</strong> below cutoff</span>
        </div>
        """, unsafe_allow_html=True)

    # Export flagged students
    st.markdown("---")
    csv_bytes = below_threshold.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download Flagged Students Report ({flagged} students)",
        data=csv_bytes,
        file_name="flagged_students_below_75pct.csv",
        mime="text/csv",
        use_container_width=True,
    )
