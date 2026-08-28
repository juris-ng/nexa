# Faction Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | String | Faction name |
| ideology | String | Core beliefs |
| leaders | Array | Character IDs of leaders |
| members | Array | Character IDs of members |
| resources | Decimal | Material resources |
| wealth | Decimal | Total wealth |
| political_power | Decimal | Influence (-100 to +100) |
| public_support | Decimal | Approval (-100 to +100) |
| relationships | JSON | Relations with other factions |
| goals | Array | Strategic objectives |
| conflicts | Array | Active disputes |
| secrets | Array | Hidden information |

## Notes

- Relationships include trust, affection, fear, respect, resentment scores.
- Conflicts reference other faction IDs and dispute types.