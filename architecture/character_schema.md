# Character Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | String | Full name |
| age | Integer | Age in years |
| occupation | String | Job or role |
| location | UUID | Current location ID |
| wealth | Decimal | Net worth |
| health_state | Enum | healthy, injured, ill, critical |
| personality | JSON | Traits (e.g., big5 scores) |
| goals | Array | Current objectives |
| needs | Array | Physiological/social needs |
| fears | Array | Phobias, anxieties |
| beliefs | Array | Ideologies, values |
| relationships | Array | Links to other characters |
| faction | UUID | Associated faction ID |
| reputation | Decimal | Public standing (-100 to +100) |
| memories | Array | Episodic/semantic memories |
| knowledge | Array | Known facts, secrets |
| secrets | Array | Hidden information |
| schedule | JSON | Daily routine |
| current_activity | String | What they are doing now |

## Notes

- All IDs are UUIDs.
- Relationships reference other character IDs.
- Memories include importance, emotional_weight, recency.
- Schedule defines hourly activities.