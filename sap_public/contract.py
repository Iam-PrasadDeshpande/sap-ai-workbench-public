"""Public execution contract: the ONLY things the public edition may do.

Everything outside this positive allowlist is unreachable by construction: the public package contains no privileged
module to import (no CAP/Node runner, no ADT client, no database, no owner-decision service, no shell/process API) and
`tests/test_public_isolation.py` proves that from the import graph and by direct negative calls. Nothing here is a
feature flag: there is no switch that enables more.
"""
from __future__ import annotations

EDITION = 'PUBLIC_INTERACTIVE'
VERSION = '0.1.0'

# Fixed hosts and read-only tools. A visitor cannot supply, change or extend these.
ALLOWED_ENDPOINTS = {
    'https://developers.sap.com/mcp/search': frozenset({'semantic_search', 'search_tutorials', 'get_tutorial'}),
    'https://developers.sap.com/mcp/graph': frozenset({'kg_search_concepts'}),
}
ALLOWED_SOURCE_HOST = 'developers.sap.com'
PROTOCOL_VERSION = '2025-06-18'
USER_AGENT = 'SAP-AI-Workbench-Public/0.1 (read-only learning tool)'

LIMITS = {
    'question_max_chars': 300,
    'response_max_bytes': 1_000_000,
    'timeout_seconds': 15,
    'calls_per_lookup': 4,
    'lookups_per_session': 15,
    'min_seconds_between_lookups': 4,
    'cache_ttl_seconds': 600,
    'cache_max_entries': 64,
    'sources_shown': 8,
    'ledger_max_entries': 40,
    'report_max_bytes': 200_000,
    'argument_max_bytes': 2_000,
}

# Evidence classes the public runtime may create, and those it can only describe.
MINTABLE_EVIDENCE = ('DOCUMENTATION', 'PUBLIC_SAP_API', 'SYNTHETIC_DEMONSTRATION')
NOT_CREATABLE_PUBLICLY = ('LOCAL_FRAMEWORK_EVIDENCE', 'SAP_TRIAL_READBACK', 'ENTERPRISE_READBACK')
EVIDENCE_CLASSES = MINTABLE_EVIDENCE + NOT_CREATABLE_PUBLICLY

EVIDENCE_TEXT = {
    'DOCUMENTATION': ('Documentation', 'Published description. It is a claim, not an observation.'),
    'PUBLIC_SAP_API': ("Answer from SAP's public developer service",
                       'SAP content that was actually retrieved. It shows what SAP publishes, not that anything works '
                       'in your system.'),
    'SYNTHETIC_DEMONSTRATION': ('Synthetic demonstration',
                                'Deterministic logic on fabricated records. It demonstrates a technique, not SAP '
                                'behaviour.'),
    'LOCAL_FRAMEWORK_EVIDENCE': ('Local framework execution (private edition only)',
                                 'Produced in the private edition on a private workstation; cannot be created here.'),
    'SAP_TRIAL_READBACK': ('SAP trial readback (private edition only)',
                           'Needs an authorised SAP trial system; cannot be created here.'),
    'ENTERPRISE_READBACK': ('Enterprise readback (not available)',
                            'Needs an enterprise system and authority; cannot be created here.'),
}

# What each kind of claim would need before it could be called proven. Used by the evidence assessment.
CLAIM_REQUIREMENTS = {
    'EXISTS_IN_SAP_DOCS': ('DOCUMENTATION', 'PUBLIC_SAP_API'),
    'TECHNIQUE_IS_SOUND': ('SYNTHETIC_DEMONSTRATION',),
    'WORKS_WITH_SAP_CAP_LOCALLY': ('LOCAL_FRAMEWORK_EVIDENCE',),
    'WORKS_ON_SAP_TRIAL': ('SAP_TRIAL_READBACK',),
    'WORKS_IN_MY_TENANT': ('ENTERPRISE_READBACK',),
}
CLAIM_TEXT = {
    'EXISTS_IN_SAP_DOCS': 'SAP documents or publishes this capability',
    'TECHNIQUE_IS_SOUND': 'This technique produces sound results on example data',
    'WORKS_WITH_SAP_CAP_LOCALLY': 'This works with SAP CAP in a local prototype',
    'WORKS_ON_SAP_TRIAL': 'This works on an SAP trial system',
    'WORKS_IN_MY_TENANT': 'This works in my own SAP tenant',
}

# Capabilities the public edition does NOT have. Listed so tests and the documentation can assert absence.
ABSENT_CAPABILITIES = (
    'sap_credentials', 'adt_mcp_access', 'cap_or_node_execution', 'local_model_inference', 'private_database',
    'approval_services', 'shell_or_process_execution', 'arbitrary_http_fetch', 'unrestricted_mcp_calls',
    'sap_write_path', 'persistent_anonymous_state')
