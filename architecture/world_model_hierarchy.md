# NEXA World Model — Entity Hierarchy

## Hierarchy
WORLD
└── CITY
└── DISTRICT
├── LOCATION
├── BUILDING
├── BUSINESS
├── CHARACTER
└── ORGANIZATION

## Definitions

### WORLD

The top-level container for the entire NEXA simulation.

### CITY

A major urban area within the world. Contains multiple districts.

### DISTRICT

A subdivision of a city. Contains locations, buildings, businesses, characters, and organizations.

### LOCATION

A specific place within a district (e.g., street, park, plaza).

### BUILDING

A structure within a location. May contain businesses, occupants, and security systems.

### BUSINESS

An economic entity operating within a building. Has employees, owner, inventory, revenue, and reputation.

### CHARACTER

An individual person within the world. Has attributes, relationships, goals, and activities.

### ORGANIZATION

A formal group or institution (e.g., government, media, union). May contain members and resources.
