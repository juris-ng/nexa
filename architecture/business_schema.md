# Business Schema

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| name | String | Business name |
| employees | Array | Character IDs |
| owner | UUID | Character ID of owner |
| inventory | JSON | Stock levels |
| revenue | Decimal | Income |
| expenses | Decimal | Costs |
| reputation | Decimal | Public standing |
| location | UUID | Building/location ID |
| prices | JSON | Product/service prices |
| operating_hours | JSON | Open/close times |

## Notes

- Inventory tracks quantities of goods.
- Prices may vary by time, demand, or faction.