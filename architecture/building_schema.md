# Building Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| location | UUID | Location ID |
| type | Enum | residential, commercial, industrial, government, etc. |
| owner | UUID | Character or organization ID |
| occupants | Array | Character IDs |
| security | Decimal | Security level (0–100) |
| business | UUID | Business ID (if applicable) |
| importance | Decimal | Strategic importance (0–100) |

## Notes

- Type determines permitted activities.
- Security affects crime probability.