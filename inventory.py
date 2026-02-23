"""Food inventory CLI -- manage your home food stock."""

import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "food_inventory.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_items(args):
    conn = get_conn()
    query = "SELECT * FROM inventory"
    params = []

    if args.category:
        query += " WHERE category LIKE ?"
        params.append(f"%{args.category}%")

    query += " ORDER BY category, name"
    rows = conn.execute(query, params).fetchall()

    if not rows:
        print("No items found.")
        return

    current_cat = None
    for r in rows:
        if r["category"] != current_cat:
            current_cat = r["category"]
            print(f"\n  [{current_cat}]")
        qty = int(r["quantity"]) if r["quantity"] == int(r["quantity"]) else r["quantity"]
        print(f"    #{r['id']:3d}  {r['name']:<30s} {qty} {r['unit']}")

    print(f"\n  Total: {len(rows)} items")
    conn.close()


def add_item(args):
    conn = get_conn()
    conn.execute(
        "INSERT INTO inventory (name, quantity, unit, category) VALUES (?, ?, ?, ?)",
        (args.name, args.quantity, args.unit, args.category),
    )
    conn.commit()
    print(f"Added: {args.name} ({args.quantity} {args.unit}) in [{args.category}]")
    conn.close()


def remove_item(args):
    conn = get_conn()
    row = conn.execute("SELECT name FROM inventory WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"No item with id {args.id}.")
        return
    conn.execute("DELETE FROM inventory WHERE id = ?", (args.id,))
    conn.commit()
    print(f"Removed: {row['name']} (id {args.id})")
    conn.close()


def update_item(args):
    conn = get_conn()
    row = conn.execute("SELECT * FROM inventory WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"No item with id {args.id}.")
        return

    updates = []
    params = []
    if args.name:
        updates.append("name = ?")
        params.append(args.name)
    if args.quantity is not None:
        updates.append("quantity = ?")
        params.append(args.quantity)
    if args.unit:
        updates.append("unit = ?")
        params.append(args.unit)
    if args.category:
        updates.append("category = ?")
        params.append(args.category)

    if not updates:
        print("Nothing to update. Use --name, --quantity, --unit, or --category.")
        return

    params.append(args.id)
    conn.execute(f"UPDATE inventory SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()
    print(f"Updated item #{args.id}.")
    conn.close()


def search_items(args):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM inventory WHERE name LIKE ? ORDER BY category, name",
        (f"%{args.query}%",),
    ).fetchall()

    if not rows:
        print(f"No items matching '{args.query}'.")
        return

    for r in rows:
        qty = int(r["quantity"]) if r["quantity"] == int(r["quantity"]) else r["quantity"]
        print(f"  #{r['id']:3d}  {r['name']:<30s} {qty} {r['unit']}  [{r['category']}]")

    print(f"\n  Found: {len(rows)} items")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Food Inventory Manager")
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List all items")
    p_list.add_argument("-c", "--category", help="Filter by category")

    # add
    p_add = sub.add_parser("add", help="Add a new item")
    p_add.add_argument("name", help="Item name")
    p_add.add_argument("quantity", type=float, help="Quantity")
    p_add.add_argument("unit", help="Unit (g, ml, can, jar, pack, piece, bottle)")
    p_add.add_argument("category", help="Category")

    # remove
    p_rm = sub.add_parser("remove", help="Remove an item by id")
    p_rm.add_argument("id", type=int, help="Item ID")

    # update
    p_up = sub.add_parser("update", help="Update an item")
    p_up.add_argument("id", type=int, help="Item ID")
    p_up.add_argument("--name", help="New name")
    p_up.add_argument("--quantity", type=float, help="New quantity")
    p_up.add_argument("--unit", help="New unit")
    p_up.add_argument("--category", help="New category")

    # search
    p_search = sub.add_parser("search", help="Search items by name")
    p_search.add_argument("query", help="Search term")

    args = parser.parse_args()

    commands = {
        "list": list_items,
        "add": add_item,
        "remove": remove_item,
        "update": update_item,
        "search": search_items,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
