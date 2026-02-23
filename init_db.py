"""Initialize the food inventory SQLite database with data from FirstInv.md."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "food_inventory.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS inventory")
    cur.execute("""
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Inventory from FirstInv.md (Polish)
    items = [
        # Konserwy
        ("Pomidory w puszce", 5, "puszka", "Konserwy"),
        ("Ciecierzyca", 5, "puszka", "Konserwy"),
        ("Kukurydza", 5, "puszka", "Konserwy"),
        ("Oliwki zielone", 1, "słoik", "Konserwy"),
        ("Oliwki czarne", 1, "słoik", "Konserwy"),
        ("Passata pomidorowa", 2, "opak.", "Konserwy"),  # 2 x 200ml

        # Przyprawy i sosy
        ("Harissa", 1, "słoik", "Przyprawy i sosy"),
        ("Pesto czerwone", 1, "słoik", "Przyprawy i sosy"),
        ("Pesto zielone", 1, "słoik", "Przyprawy i sosy"),
        ("Kapary", 2, "słoik", "Przyprawy i sosy"),
        ("Anchois", 1, "słoik", "Przyprawy i sosy"),
        ("Pasta miso", 1, "słoik", "Przyprawy i sosy"),
        ("Ocet balsamiczny", 1, "butelka", "Przyprawy i sosy"),
        ("Ocet", 1, "butelka", "Przyprawy i sosy"),
        ("Olej sezamowy", 1, "butelka", "Przyprawy i sosy"),
        ("Sos sojowy", 1, "butelka", "Przyprawy i sosy"),
        ("Olej chili", 1, "butelka", "Przyprawy i sosy"),
        ("Sos worcestershire", 1, "butelka", "Przyprawy i sosy"),
        ("Tahini", 1, "słoik", "Przyprawy i sosy"),

        # Kasze i rośliny strączkowe
        ("Ryż brązowy", 500, "g", "Kasze i rośliny strączkowe"),
        ("Fasola pinto", 500, "g", "Kasze i rośliny strączkowe"),
        ("Groch zielony (suszony)", 500, "g", "Kasze i rośliny strączkowe"),
        ("Soczewica czerwona", 500, "g", "Kasze i rośliny strączkowe"),
        ("Kasza gryczana", 300, "g", "Kasze i rośliny strączkowe"),
        ("Soczewica brązowa", 150, "g", "Kasze i rośliny strączkowe"),
        ("Ryż basmati", 200, "g", "Kasze i rośliny strączkowe"),

        # Makarony i mąki
        ("Makaron risoni", 500, "g", "Makarony i mąki"),
        ("Mąka orkiszowa", 1000, "g", "Makarony i mąki"),  # 1kg
        ("Mąka do pizzy", 1000, "g", "Makarony i mąki"),  # 1kg
        ("Mąka orkiszowa", 200, "g", "Makarony i mąki"),   # second bag
        ("Mąka pszenna", 200, "g", "Makarony i mąki"),
        ("Płatki owsiane", 1, "opak.", "Makarony i mąki"),

        # Pasty curry
        ("Pasta curry czerwona", 2, "opak.", "Pasty curry"),
        ("Pasta curry żółta", 1, "opak.", "Pasty curry"),
        ("Pasta tamaryndowa", 1, "opak.", "Pasty curry"),

        # Pieczenie
        ("Skrobia kukurydziana", 1, "opak.", "Pieczenie"),
        ("Drożdże", 7, "szt.", "Pieczenie"),
        ("Cukier waniliowy", 10, "szt.", "Pieczenie"),
        ("Proszek do pieczenia", 13, "szt.", "Pieczenie"),
        ("Soda oczyszczona", 2, "szt.", "Pieczenie"),
        ("Budyń", 4, "szt.", "Pieczenie"),
        ("Żelatyna", 1, "opak.", "Pieczenie"),
        ("Skórka pomarańczowa (suszona)", 3, "szt.", "Pieczenie"),
        ("Kakao", 1, "opak.", "Pieczenie"),
        ("Czekolada do pieczenia", 1, "opak.", "Pieczenie"),
        ("Laska wanilii", 4, "szt.", "Pieczenie"),

        # Cukier i sól
        ("Cukier", 1500, "g", "Cukier i sól"),
        ("Sól morska", 500, "g", "Cukier i sól"),
        ("Cukier puder", 250, "g", "Cukier i sól"),

        # Orzechy i nasiona
        ("Sezam", 400, "g", "Orzechy i nasiona"),
        ("Pestki słonecznika", 500, "g", "Orzechy i nasiona"),
        ("Pistacje", 250, "g", "Orzechy i nasiona"),
        ("Mieszanka orzechów", 800, "g", "Orzechy i nasiona"),
        ("Migdały", 250, "g", "Orzechy i nasiona"),
        ("Kukurydza na popcorn", 100, "g", "Orzechy i nasiona"),
        ("Nasiona chia", 300, "g", "Orzechy i nasiona"),
        ("Orzechy włoskie", 400, "g", "Orzechy i nasiona"),
        ("Mieszanka nasion", 150, "g", "Orzechy i nasiona"),
        ("Siemię lniane", 400, "g", "Orzechy i nasiona"),
    ]

    cur.executemany(
        "INSERT INTO inventory (name, quantity, unit, category) VALUES (?, ?, ?, ?)",
        items,
    )

    conn.commit()
    print(f"Database created at {DB_PATH}")
    print(f"Inserted {len(items)} items.")

    # Print summary by category
    cur.execute("""
        SELECT category, COUNT(*) as count
        FROM inventory
        GROUP BY category
        ORDER BY category
    """)
    print("\nItems by category:")
    for row in cur.fetchall():
        try:
            print(f"  {row[0]}: {row[1]}")
        except UnicodeEncodeError:
            print(f"  {row[0].encode('ascii', 'replace').decode()}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    create_database()
