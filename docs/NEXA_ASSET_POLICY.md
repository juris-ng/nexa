# NEXA Asset Acquisition and Licensing Policy

## Purpose

Every external asset used in NEXA must be traceable to its source and licence terms before it enters the UE5 production project.

## Asset Register Requirement

Record every asset or asset pack in:

`assets/source_records/asset_register.csv`

Required fields:

- asset_id
- name
- category
- source
- creator
- license
- license_url
- commercial_use
- modification_allowed
- attribution_required
- acquired_date
- project_path
- notes
- status

## Approved Sources

Potential sources include:

- Unreal Engine City Sample
- Fab
- Megascans content available through authorised Epic/Fab workflows
- MetaHuman content and plugins
- Original NEXA-created content
- Compatible assets with verified licences

## Licence Rules

- Confirm the licence for each specific asset or pack.
- Do not assume every free asset has the same commercial permissions.
- Do not upload, resell or redistribute third-party source assets as standalone files.
- Keep receipts, download pages, licence pages and attribution records where applicable.
- Use an asset only after its register entry is complete.
- Keep original downloaded source records outside public Git repositories when licence terms require it.

## Git Rule

Large UE5 assets and third-party marketplace assets should not be casually committed to the main Git repository. Source code, configuration, documents, metadata and asset-register records may be committed. Project assets should later use an appropriate storage and version-control strategy.

## Review Status

Use one of these status values:

- planned
- acquired
- verified
- approved_for_use
- restricted
- replaced
- removed
