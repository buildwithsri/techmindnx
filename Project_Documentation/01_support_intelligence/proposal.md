Project Proposal
AI-Powered Smart Campus Student Support System
TEAM LEAD-KRISHNA SUBASH
FRONT END-RIYA JACOB
AI DEVELOPER-SAFNA FATHIMA
CONTENT DEVELOPER-PARVATHY UNNIKRISHNAN
BACK END-NEHA ZIYAN,SHWETHA KRISHNA
DATABASE AND AUTHENTICATION DEVELOPER-SNEHA SHAJAN
TESTING/DEPLOYMENT-SHREYA SAGEESH

1. Introduction

The proposed AI-Powered Smart Campus Student Support System is an intelligent platform designed to provide students with quick, personalized, and accessible academic and campus-related support.

2. Problem Statement

Students often face difficulties in getting information about courses, exams, attendance, scholarships, campus services, and academic procedures. Faculty and staff also have limited time to provide individual support to every student.

3. Proposed Solution

The system will use Artificial Intelligence and a 24/7 chatbot to answer student queries, analyze academic patterns, and provide suitable guidance. It can also identify students who may require academic support and generate early alerts.

4. Key Features
🤖 24/7 AI Chatbot for student queries
📚 Academic Guidance and study recommendations
⚠️ Early Warning System for students showing academic difficulties
🏫 Campus Service Information
🔔 Alerts and Reminders for exams, attendance, and important activities
👤 Personalized Student Support
📊 Basic academic performance analysis
5. Technologies
Frontend: Flutter / Web
Backend: Python
AI: NLP & Machine Learning
Database: Firebase / MySQL
Version Control: GitHub
6. Expected Outcome

The system aims to provide a single intelligent platform where students can get academic and campus-related assistance anytime. It will improve accessibility to information, provide personalized guidance, and help identify students who may need additional support at an early stage.

7. Future Scope

The system can later be extended with voice-based assistance, multilingual support, timetable integration, LMS integration, placement guidance, and predictive analytics.

Critical Attendance Risk Escalation & AI Engineering Trigger Response
--------------------------------------------------------------------
```
{
  "event_id": "EVT-2026-09-8831",
  "team": "AI_ENGINEERING",
  "priority": "CRITICAL",
  "status": "ESCALATED",
  "source": "DISASTER_MANAGEMENT_TEAM",

  "action_required": {
    "support_tl": true,
    "trigger_ai_engineering": true,
    "immediate_intervention": true
  },

  "incident_summary": {
    "anomaly_type": "PROJECTED_EXAM_DEBARMENT",
    "risk_level": "CRITICAL",
    "anomaly_confidence": 0.924,
    "current_attendance_pct": 76.2,
    "projected_end_sem_attendance_pct": 67.8,
    "minimum_required_pct": 75.0,
    "days_to_irreversible_limit": 4
  },

  "root_causes": [
    "Consecutive absence in Subject CS301 for 3 sessions",
    "Attendance trajectory indicates projected fall below statutory minimum"
  ],

  "ai_engineering_tasks": [
    "Validate the risk prediction and anomaly confidence",
    "Analyze attendance trajectory and identify intervention window",
    "Generate recommended preventive actions for the TL",
    "Prioritize the student for emergency intervention",
    "Prepare chatbot response and escalation workflow",
    "Ensure academic advisor notification is triggered"
  ],

  "tl_support": {
    "recommendation": "Immediate academic intervention required",
    "urgency": "WITHIN_4_DAYS",

    "suggested_actions": [
      "Contact student through chatbot",
      "Notify academic advisor",
      "Review CS301 attendance and absence pattern",
      "Initiate corrective attendance plan"
    ]
  },

  "chatbot_action": "TRIGGER_PARENT_EMERGENCY_ALERT",

  "portal_action": "HIGHLIGHT_ON_FACULTY_CONSOLE",

  "escalation": {
    "level": "EMERGENCY",
    "next_team": "AI_ENGINEERING_TEAM",
    "requires_tl_acknowledgement": true
  }
}
```

## AI Engineering Trigger Response(README)

The AI Engineering module receives critical alerts from the Disaster Management Team and processes them using NLP-based risk analysis.

### Trigger Workflow

Disaster Management Team
        ↓
Risk Detection
        ↓
AI Engineering Trigger
        ↓
NLP Processing
        ↓
Intent & Entity Extraction
        ↓
Risk Classification
        ↓
Recommended Action
        ↓
Chatbot / TL / Academic Advisor

### Example Scenario

A student currently has 76.2% attendance. Based on the attendance trajectory, the projected semester attendance is 67.8%, which is below the minimum statutory requirement of 75%.

The system identifies this as:

- **Anomaly:** Projected Exam Debarment
- **Risk Level:** Critical
- **Confidence:** 92.4%
- **Intervention Window:** 4 days
- **Required Action:** Immediate academic intervention

### AI Engineering Responsibilities

1. Validate the risk prediction.
2. Analyze the attendance trajectory.
3. Identify the intervention window.
4. Classify the severity of the incident.
5. Generate preventive actions.
6. Trigger the chatbot escalation workflow.
7. Notify the academic advisor.
8. Provide the TL with recommended actions.

### NLP Pipeline

The NLP model processes incoming alerts and extracts important information such as:

- Student-related entities
- Subject names
- Attendance percentages
- Absence patterns
- Risk level
- Anomaly type
- Required actions

The extracted information is converted into a structured JSON response that can be consumed by the chatbot and faculty portal.
