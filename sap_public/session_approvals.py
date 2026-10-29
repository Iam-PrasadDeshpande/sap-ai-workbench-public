"""Owner approval registry for public research notes.

Maps a session id to the exact content digest (SHA-256, see sessions.digest_of) the owner approved for publication.
This module is covered by PUBLIC_MANIFEST.json's SHA-256 file inventory. The public site's owner-approved release
procedure uses that manifest and the exact content digest; it does not use Authenticode. This is separate from private
workbench D012 signing requirements. A content writer cannot approve a note by editing its JSON: only a digest
explicitly registered here is displayed. The manifest detects drift, but is not a cryptographic signature or a defense
against an actor who can change the deployment and manifest together.

Entries are added only after owner approval of the exact content digest and required review/qualification gates.
"""
APPROVED_CONTENT_SHA256: dict[str, str] = {
    # KS01 research note R7 (comprehensive eight-view research content). Owner-approved 2026-10-15 for this exact digest,
    # together with D012 signing, the scoped qualification profile and publication of this release. Earlier
    # approvals do not carry over: R6 was bdb147f90a07f3611f4929b024fa246e0136187a7930d08879aa087a968f29ee, R5 was
    # 65e176d175ef3f890d3fb0373822031cb8053beb7fb20629a41c689062856200 (its approved sentences are reproduced verbatim
    # inside R7, proven by the canonical lineage check) and R3 was
    # aadb01ff9ee5b1f403dd738323ab2e370be88284b00e0dd79e746e7a7da813af.
    'KS01': 'b3f4da6d43b3e2ab16ecb76ced012dbb7170453c89e669166606b6457c93a82e',
    # KS04 research note, public edition 1.0 (CAP MCP: development-time server versus runtime adapter), featured banner order 0.
    # The digest covers the exact public content including the featured object. This entry is part of the UNSIGNED source
    # commit; it takes effect only through an owner-approved, D012-signed and qualified release. Any change to the public
    # KS04 content changes the digest and needs a new entry.
    'KS04': 'c9cd1f31eb0da4c103d24f19cc20183ab06c762d02813282449da8072f5735e1',
    # KS05 R3: owner-approved public POC observations; exact digest is verified in the release evidence.
    'KS05': '45d8776855372687ffedc7eda1a17b4e8a0817990e2be4373e5c6bbb58b05048',
    # KS07: add only under owner-approved exact-content publication gate.
    'KS07': '718e6f64a45c9d49d6ed29acd72be6eb1bf79c6d77b189768378df6aef5d796e',
}
