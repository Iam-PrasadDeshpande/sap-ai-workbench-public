"""Signed approval registry for public research notes.

Maps a session id to the exact content digest (SHA-256, see sessions.digest_of) the owner approved for publication.
This module is part of the Authenticode-signed package and of the public artifact manifest, so an entry can only be
added by the owner through a new signed release with the pinned identity. A content writer cannot approve their own
file by editing JSON. Empty means nothing is approved: every candidate is withheld.

Do not add an entry in a content-only change. An entry is made by the owner, after the review gates, naming the digest
of the exact approved content.
"""
APPROVED_CONTENT_SHA256: dict[str, str] = {
    # KS01 research note R5-editorial-unsigned-candidate. PROPOSED digest, NOT yet owner-approved: this entry is the unsigned
    # candidate's registry value and has effect only after owner digest approval, GPT review and D012 signing.
    # Superseded R3 approval (2026-10-14) was for aadb01ff9ee5b1f403dd738323ab2e370be88284b00e0dd79e746e7a7da813af.
    'KS01': '65e176d175ef3f890d3fb0373822031cb8053beb7fb20629a41c689062856200',
}
