from mystery_models import (
    Evidence,
    EvidenceVisibility,
    Mystery,
    MysteryState,
    StoryBeat,
)


def create_warehouse_fire_mystery() -> tuple[Mystery, list[Evidence]]:
    """
    Creates the Phase 10 long-form mystery example.

    Day 3: Warehouse fire
    Day 14: Missing witness
    Day 23: Financial anomaly
    Day 31: Political connection
    Day 47: NIA discovers evidence
    Day 60: Audience connects clues
    """

    mystery = Mystery(
        title="The Eastern Warehouse Fire",
        premise=(
            "An apparently accidental warehouse fire triggers labour unrest, "
            "but evidence suggests it may conceal a political and financial scheme."
        ),
        hidden_truth=(
            "A corporation executive and a government procurement official "
            "arranged the fire to destroy records tied to fraudulent contracts."
        ),
        suspects=[
            "corporate_executive",
            "procurement_official",
            "warehouse_manager",
            "union_organiser",
        ],
        false_leads=[
            "The fire was caused by an electrical fault.",
            "A union member started the fire during a labour dispute.",
            "The warehouse manager acted alone for insurance money.",
        ],
        resolution=(
            "The audience connects financial, witness and procurement evidence, "
            "exposing the corporate-government corruption scheme."
        ),
        state=MysteryState.HIDDEN,
    )

    evidence_records = [
        Evidence(
            title="Damaged Warehouse Safety Log",
            description=(
                "The safety log shows inspection failures shortly before the fire."
            ),
            source="warehouse archive",
            reliability=62.0,
            location_id="eastern_warehouse",
            visibility=EvidenceVisibility.HIDDEN,
            linked_event_id="warehouse_fire",
            tags=["warehouse", "fire", "safety_log"],
        ),
        Evidence(
            title="Missing Witness Statement Draft",
            description=(
                "A draft statement suggests a warehouse worker saw an unauthorised "
                "visitor before the fire."
            ),
            source="journalist_malik",
            reliability=78.0,
            location_id="eastern_warehouse",
            visibility=EvidenceVisibility.HIDDEN,
            linked_character_id="missing_witness",
            linked_event_id="missing_witness_event",
            tags=["witness", "warehouse", "fire"],
        ),
        Evidence(
            title="Irregular Payment Ledger",
            description=(
                "The ledger contains payments routed through a shell contractor "
                "connected to the corporation."
            ),
            source="financial_audit",
            reliability=88.0,
            location_id="corporation_hq",
            visibility=EvidenceVisibility.HIDDEN,
            linked_character_id="corporate_executive",
            tags=["financial", "corporation", "payments"],
        ),
        Evidence(
            title="Procurement Meeting Record",
            description=(
                "A restricted meeting record links the procurement official to "
                "the shell contractor."
            ),
            source="government archive",
            reliability=91.0,
            location_id="government_building",
            visibility=EvidenceVisibility.HIDDEN,
            linked_character_id="procurement_official",
            tags=["government", "procurement", "corruption"],
        ),
        Evidence(
            title="Encrypted Voice Recording",
            description=(
                "NIA identifies a recording that references destroying warehouse "
                "records before an audit."
            ),
            source="nia_analysis",
            reliability=84.0,
            location_id="eastern_warehouse",
            visibility=EvidenceVisibility.HIDDEN,
            linked_character_id="corporate_executive",
            tags=["nia", "recording", "warehouse", "audit"],
        ),
    ]

    story_beats = [
        StoryBeat(
            simulation_day=3,
            title="Eastern Warehouse Fire",
            description=(
                "A fire damages the Eastern Warehouse and causes immediate "
                "public concern."
            ),
            event_type="warehouse_fire",
            target_state=MysteryState.HINTED,
            reveal_evidence_ids=[evidence_records[0].id],
            related_event_ids=["warehouse_fire"],
        ),
        StoryBeat(
            simulation_day=14,
            title="Key Witness Disappears",
            description=(
                "A warehouse worker who reportedly saw an unauthorised visitor "
                "before the fire disappears."
            ),
            event_type="missing_witness",
            target_state=MysteryState.DISCOVERED,
            reveal_evidence_ids=[evidence_records[1].id],
            related_character_ids=["missing_witness"],
            related_event_ids=["missing_witness_event"],
        ),
        StoryBeat(
            simulation_day=23,
            title="Financial Anomaly Found",
            description=(
                "An irregular payment pattern links the corporation to a shell "
                "contractor."
            ),
            event_type="financial_anomaly",
            target_state=MysteryState.INVESTIGATED,
            reveal_evidence_ids=[evidence_records[2].id],
            related_character_ids=["corporate_executive"],
        ),
        StoryBeat(
            simulation_day=31,
            title="Political Connection Emerges",
            description=(
                "A procurement record creates a possible connection between "
                "the corporation and a government official."
            ),
            event_type="political_connection",
            target_state=MysteryState.PARTIALLY_UNDERSTOOD,
            reveal_evidence_ids=[evidence_records[3].id],
            related_character_ids=["procurement_official"],
        ),
        StoryBeat(
            simulation_day=47,
            title="NIA Discovers Hidden Recording",
            description=(
                "NIA identifies an encrypted recording suggesting that warehouse "
                "records were deliberately destroyed before an audit."
            ),
            event_type="nia_evidence_discovery",
            target_state=MysteryState.NEAR_RESOLUTION,
            reveal_evidence_ids=[evidence_records[4].id],
            nia_discovery=True,
        ),
        StoryBeat(
            simulation_day=60,
            title="Audience Connects the Evidence",
            description=(
                "The audience connects the witness, financial and procurement "
                "evidence, revealing the corporate-government corruption scheme."
            ),
            event_type="audience_revelation",
            target_state=MysteryState.RESOLVED,
            audience_required=True,
        ),
    ]

    mystery.story_beats.extend(story_beats)
    return mystery, evidence_records
