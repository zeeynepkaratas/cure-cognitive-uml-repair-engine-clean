"""Small PURE-derived external repair pilot cases.

These cases are not a replacement for the shared S01-S50 controlled benchmark.
They provide a preliminary external check based on selected PURE requirement
statements, manually curated reference UML models, and controlled injected
PlantUML defects.
"""

from __future__ import annotations


PURE_EXTERNAL_REPAIR_CASES = [
    {
        "case_id": "P01",
        "pure_row": 30,
        "category": "missing_startuml",
        "description": "Defect logging interface with missing @startuml boundary.",
        "srs_metni": (
            "The solution should provide an interface for the user to log any "
            "defects or enhancement requests on the application and track thereafter."
        ),
        "reference_plantuml": """@startuml
class User {}
class DefectRequest {}
class EnhancementRequest {}
class TrackingInterface {}
User --> TrackingInterface
TrackingInterface --> DefectRequest
TrackingInterface --> EnhancementRequest
@enduml""",
        "plantuml_kodu": """class User {}
class DefectRequest {}
class EnhancementRequest {}
class TrackingInterface {}
User --> TrackingInterface
TrackingInterface --> DefectRequest
TrackingInterface --> EnhancementRequest
@enduml""",
    },
    {
        "case_id": "P02",
        "pure_row": 31,
        "category": "missing_enduml",
        "description": "Alert notification flow with missing @enduml boundary.",
        "srs_metni": (
            "The solution should send alerts, such as email and SMS, to the user "
            "whenever any action has been taken on the alert."
        ),
        "reference_plantuml": """@startuml
class User {}
class Alert {}
class EmailNotification {}
class SMSNotification {}
class NotificationService {}
NotificationService --> Alert
NotificationService --> User
NotificationService --> EmailNotification
NotificationService --> SMSNotification
@enduml""",
        "plantuml_kodu": """@startuml
class User {}
class Alert {}
class EmailNotification {}
class SMSNotification {}
class NotificationService {}
NotificationService --> Alert
NotificationService --> User
NotificationService --> EmailNotification
NotificationService --> SMSNotification""",
    },
    {
        "case_id": "P03",
        "pure_row": 33,
        "category": "duplicate_class",
        "description": "Help-desk reports with duplicate report class.",
        "srs_metni": (
            "The solution should enable the help-desk user to view reports on "
            "submitted defects or enhancement requests category-wise, status-wise, and age-wise."
        ),
        "reference_plantuml": """@startuml
class HelpDeskUser {}
class DefectReport {}
class EnhancementRequest {}
class ReportFilter {}
HelpDeskUser --> DefectReport
DefectReport --> ReportFilter
DefectReport --> EnhancementRequest
@enduml""",
        "plantuml_kodu": """@startuml
class HelpDeskUser {}
class DefectReport {}
class DefectReport {}
class EnhancementRequest {}
class ReportFilter {}
HelpDeskUser --> DefectReport
DefectReport --> ReportFilter
DefectReport --> EnhancementRequest
@enduml""",
    },
    {
        "case_id": "P04",
        "pure_row": 37,
        "category": "missing_both_boundaries",
        "description": "Audit trail capture with both PlantUML boundaries removed.",
        "srs_metni": (
            "The System must keep an unalterable audit trail capable of automatically "
            "capturing and storing actions on critical entities, the initiating user, "
            "and the date and time of the event."
        ),
        "reference_plantuml": """@startuml
class AuditTrail {}
class AuditEvent {}
class CriticalEntity {}
class SystemUser {}
AuditTrail --> AuditEvent
AuditEvent --> CriticalEntity
AuditEvent --> SystemUser
@enduml""",
        "plantuml_kodu": """class AuditTrail {}
class AuditEvent {}
class CriticalEntity {}
class SystemUser {}
AuditTrail --> AuditEvent
AuditEvent --> CriticalEntity
AuditEvent --> SystemUser""",
    },
    {
        "case_id": "P05",
        "pure_row": 42,
        "category": "missing_enduml",
        "description": "Audit export case with missing @enduml boundary.",
        "srs_metni": (
            "The System must be able to export audit trails for specified cases "
            "without affecting the audit trail stored by the System."
        ),
        "reference_plantuml": """@startuml
class System {}
class AuditTrail {}
class Case {}
class ExportService {}
System --> ExportService
ExportService --> AuditTrail
ExportService --> Case
@enduml""",
        "plantuml_kodu": """@startuml
class System {}
class AuditTrail {}
class Case {}
class ExportService {}
System --> ExportService
ExportService --> AuditTrail
ExportService --> Case""",
    },
    {
        "case_id": "P06",
        "pure_row": 49,
        "category": "duplicate_class_missing_start",
        "description": "Case access control with duplicate user group and missing start boundary.",
        "srs_metni": (
            "The System must allow the user to limit access to cases to specified "
            "users or user groups."
        ),
        "reference_plantuml": """@startuml
class System {}
class User {}
class UserGroup {}
class Case {}
class AccessControl {}
System --> AccessControl
AccessControl --> User
AccessControl --> UserGroup
AccessControl --> Case
@enduml""",
        "plantuml_kodu": """class System {}
class User {}
class UserGroup {}
class UserGroup {}
class Case {}
class AccessControl {}
System --> AccessControl
AccessControl --> User
AccessControl --> UserGroup
AccessControl --> Case
@enduml""",
    },
    {
        "case_id": "P07",
        "pure_row": 51,
        "category": "missing_startuml",
        "description": "Admin user profile setup with missing @startuml boundary.",
        "srs_metni": (
            "The System must allow only admin-users to set up user profiles and "
            "allocate users to groups."
        ),
        "reference_plantuml": """@startuml
class System {}
class AdminUser {}
class UserProfile {}
class UserGroup {}
System --> AdminUser
AdminUser --> UserProfile
AdminUser --> UserGroup
@enduml""",
        "plantuml_kodu": """class System {}
class AdminUser {}
class UserProfile {}
class UserGroup {}
System --> AdminUser
AdminUser --> UserProfile
AdminUser --> UserGroup
@enduml""",
    },
    {
        "case_id": "P08",
        "pure_row": 59,
        "category": "duplicate_class",
        "description": "Unauthorized access audit logging with duplicate access attempt.",
        "srs_metni": (
            "If the System allows users to make unauthorised attempts to access cases, "
            "it must log these in the audit trail."
        ),
        "reference_plantuml": """@startuml
class System {}
class User {}
class Case {}
class AccessAttempt {}
class AuditTrail {}
System --> AccessAttempt
AccessAttempt --> User
AccessAttempt --> Case
System --> AuditTrail
AuditTrail --> AccessAttempt
@enduml""",
        "plantuml_kodu": """@startuml
class System {}
class User {}
class Case {}
class AccessAttempt {}
class AccessAttempt {}
class AuditTrail {}
System --> AccessAttempt
AccessAttempt --> User
AccessAttempt --> Case
System --> AuditTrail
AuditTrail --> AccessAttempt
@enduml""",
    },
    {
        "case_id": "P09",
        "pure_row": 64,
        "category": "missing_both_boundaries",
        "description": "Simultaneous entity display with both boundaries removed.",
        "srs_metni": "The System must be able to display several entities, such as cases and suspects, simultaneously.",
        "reference_plantuml": """@startuml
class System {}
class DisplayView {}
class Case {}
class Suspect {}
System --> DisplayView
DisplayView --> Case
DisplayView --> Suspect
@enduml""",
        "plantuml_kodu": """class System {}
class DisplayView {}
class Case {}
class Suspect {}
System --> DisplayView
DisplayView --> Case
DisplayView --> Suspect""",
    },
    {
        "case_id": "P10",
        "pure_row": 106,
        "category": "missing_enduml",
        "description": "Clear error messages with missing @enduml boundary.",
        "srs_metni": (
            "The content of error messages shown on the pages or special error pages "
            "should clearly state the reason why the error occurred and, if possible, "
            "actions the user can take to resolve the error."
        ),
        "reference_plantuml": """@startuml
class ErrorMessage {}
class ErrorPage {}
class ErrorReason {}
class UserAction {}
ErrorPage --> ErrorMessage
ErrorMessage --> ErrorReason
ErrorMessage --> UserAction
@enduml""",
        "plantuml_kodu": """@startuml
class ErrorMessage {}
class ErrorPage {}
class ErrorReason {}
class UserAction {}
ErrorPage --> ErrorMessage
ErrorMessage --> ErrorReason
ErrorMessage --> UserAction""",
    },
]
