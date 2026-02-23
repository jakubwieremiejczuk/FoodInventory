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

    # Translated and normalized inventory from FirstInv.md
    items = [
        # Canned goods
        ("Canned tomatoes", 5, "can", "Canned goods"),
        ("Chickpeas", 5, "can", "Canned goods"),
        ("Corn", 5, "can", "Canned goods"),
        ("Green olives", 1, "jar", "Canned goods"),
        ("Black olives", 1, "jar", "Canned goods"),
        ("Tomato passata", 2, "pack", "Canned goods"),  # 2 x 200ml

        # Condiments & sauces
        ("Harissa", 1, "jar", "Condiments"),
        ("Red pesto", 1, "jar", "Condiments"),
        ("Green pesto", 1, "jar", "Condiments"),
        ("Capers", 2, "jar", "Condiments"),
        ("Anchovies", 1, "jar", "Condiments"),
        ("Miso paste", 1, "jar", "Condiments"),
        ("Balsamic vinegar", 1, "bottle", "Condiments"),
        ("Vinegar", 1, "bottle", "Condiments"),
        ("Sesame oil", 1, "bottle", "Condiments"),
        ("Fermented soy sauce", 1, "bottle", "Condiments"),
        ("Chili oil", 1, "bottle", "Condiments"),
        ("Worcestershire sauce", 1, "bottle", "Condiments"),
        ("Tahini", 1, "jar", "Condiments"),

        # Grains & legumes
        ("Brown rice", 500, "g", "Grains & legumes"),
        ("Pinto beans", 500, "g", "Grains & legumes"),
        ("Green peas (dried)", 500, "g", "Grains & legumes"),
        ("Red lentils", 500, "g", "Grains & legumes"),
        ("Buckwheat groats", 300, "g", "Grains & legumes"),
        ("Brown lentils", 150, "g", "Grains & legumes"),
        ("Basmati rice", 200, "g", "Grains & legumes"),

        # Pasta & flour
        ("Risoni pasta", 500, "g", "Pasta & flour"),
        ("Spelt flour", 1000, "g", "Pasta & flour"),  # 1kg
        ("Pizza flour", 1000, "g", "Pasta & flour"),  # 1kg
        ("Spelt flour", 200, "g", "Pasta & flour"),   # second bag
        ("Wheat flour", 200, "g", "Pasta & flour"),
        ("Oat flakes", 1, "pack", "Pasta & flour"),

        # Curry & spice pastes
        ("Red curry paste", 2, "pack", "Curry & spice pastes"),
        ("Yellow curry paste", 1, "pack", "Curry & spice pastes"),
        ("Tamarind paste", 1, "pack", "Curry & spice pastes"),

        # Baking
        ("Cornstarch", 1, "pack", "Baking"),  # Speisestärke
        ("Yeast", 7, "piece", "Baking"),
        ("Vanilla sugar", 10, "piece", "Baking"),
        ("Baking powder", 13, "piece", "Baking"),
        ("Baking soda", 2, "piece", "Baking"),
        ("Pudding mix", 4, "piece", "Baking"),
        ("Gelatin", 1, "pack", "Baking"),
        ("Orange zest (dried)", 3, "piece", "Baking"),
        ("Cocoa powder", 1, "pack", "Baking"),
        ("Baking chocolate", 1, "pack", "Baking"),
        ("Vanilla beans", 4, "piece", "Baking"),

        # Sugar & salt
        ("Sugar", 1500, "g", "Sugar & salt"),
        ("Sea salt", 500, "g", "Sugar & salt"),
        ("Powdered sugar", 250, "g", "Sugar & salt"),

        # Nuts & seeds
        ("Sesame seeds", 400, "g", "Nuts & seeds"),
        ("Sunflower seeds (hulled)", 500, "g", "Nuts & seeds"),
        ("Pistachios", 250, "g", "Nuts & seeds"),
        ("Mixed nuts", 800, "g", "Nuts & seeds"),
        ("Almonds", 250, "g", "Nuts & seeds"),
        ("Popcorn kernels", 100, "g", "Nuts & seeds"),
        ("Chia seeds", 300, "g", "Nuts & seeds"),
        ("Walnuts", 400, "g", "Nuts & seeds"),
        ("Mixed seeds", 150, "g", "Nuts & seeds"),
        ("Flaxseed", 400, "g", "Nuts & seeds"),
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
        print(f"  {row[0]}: {row[1]}")

    conn.close()


if __name__ == "__main__":
    create_database()
