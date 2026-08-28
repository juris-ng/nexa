# Location Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| coordinates | JSON | (x, y) or (lat, lon) |
| district | UUID | District ID |
| type | Enum | street, park, plaza, etc. |
| access_level | Enum | public, restricted, private |
| importance | Decimal | Strategic importance (0–100) |
| entities_present | Array | Characters, buildings, etc. |

## Notes

- Coordinates enable spatial reasoning.
- Access level determines who can enter.