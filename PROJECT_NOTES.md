# Food Inventory - Project Notes & Ideas

## What We Have So Far
- **Original inventory** (`FirstInv.md`): ~60 pantry items listed in Polish
- **SQLite database** (`food_inventory.db`): Local DB with all items seeded (English translations)
- **CLI tool** (`inventory.py`): Full CRUD - list, add, remove, update, search
- **Supabase migration** (`migrate_to_supabase.py`): Script to push data to cloud
- **Web app** (`web/index.html`): Dark-themed, mobile-first PWA that connects to Supabase
- **DB init script** (`init_db.py`): Creates and seeds the SQLite database

## Tech Stack
- **Local DB**: SQLite
- **Cloud DB**: Supabase
- **CLI**: Python + argparse
- **Web**: Vanilla HTML/CSS/JS, PWA-ready
- **Python env**: `.venv` in project root

## Database Schema
Table `inventory`: id, name, quantity, unit, category
- Supabase version adds: created_at

## Categories
Canned goods, Condiments, Grains & legumes, Pasta & flour,
Curry & spice pastes, Baking, Sugar & salt, Nuts & seeds

## Ideas / Next Steps
_Pick what sounds interesting or add your own!_

- [ ] Barcode scanning - scan products to add them quickly
- [ ] Expiry date tracking - know when items go bad
- [ ] Shopping list generation - auto-suggest when items run low
- [ ] Recipe integration - link items to recipes, auto-deduct ingredients
- [ ] Multi-user support - share inventory with household members
- [ ] Categories management - add/edit/delete categories from the UI
- [ ] Quantity alerts - notifications when stock is low
- [ ] History/log - track what was added/removed and when
- [ ] Import/export - CSV or JSON backup/restore
- [ ] Better unit handling - convert between g/kg, ml/L automatically
- [ ] Location tracking - which shelf/cupboard/fridge an item is in
- [ ] Photo support - snap a photo of the item
- [ ] Offline-first - service worker for full offline PWA support
- [ ] Authentication - proper login for the web app (Supabase Auth)

## Decisions Made
- Items stored in English in the DB (translated from Polish original)
- Categories are stored as plain text strings
- Web app uses vanilla JS (no framework)
- Dark theme with accent colors (red #e94560, green #4ecca3)

## Notes
_Space for notes and ideas during sessions:_

