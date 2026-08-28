# Organization Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | String | Organization name |
| type | Enum | government, media, union, corporation, etc. |
| leaders | Array | Character IDs |
| members | Array | Character IDs |
| resources | Decimal | Material resources |
| headquarters | UUID | Location ID |

## Notes

- Organizations differ from factions in being formal institutions.