import os
from datetime import datetime, timedelta
from app import create_app
from app.models.item import Item, db

# ==============================================================================
# VERIFICATION SCRIPT
# ==============================================================================
# File: verify_expiry.py
# Purpose: Test automatic expiration and hiding logic.
#
# Detailed Explanation:
# The "剩食與雜物互助系統" (剩食互助系統) automatically filters out food items that
# have expired based on their expiry date, and hides any items that have been
# marked as "Taken" (already claimed).
#
# This script simulates a testing environment to verify that:
# 1. Food items expiring today are visible.
# 2. Food items expiring tomorrow are visible.
# 3. Miscellaneous items without an expiration date are visible.
# 4. Food items that expired yesterday are automatically hidden.
# 5. Food items that are expired and already taken are hidden.
# 6. Food items expiring tomorrow but already taken are hidden.
#
# The SQLite database is temporarily populated, queried, and verified.
# This conforms to Step 5 of the Implementation Skill.
#
# To run this script:
# 1. Activate the virtual environment (.venv)
# 2. Install requirements (pip install -r requirements.txt)
# 3. Execute: python verify_expiry.py
#
# Expected output:
# - Today Food
# - Tomorrow Food
# - Misc Item No Expiry
#
# Assertions check that all of the above items are visible and no other
# expired or taken items are listed.
# ==============================================================================
#
# Database Config:
# Uses instance/database.db as the test database.
# Ensure app/models/item.py is correctly implemented.
# Check if Flask app context can be successfully entered.
#
# Author: Antigravity

def verify_expiry():
    app = create_app()
    with app.app_context():
        # Clean and recreate database
        db.drop_all()
        db.create_all()

        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        # Create test items
        items = [
            Item(title="Today Food", category="Food", expiry_date=today, status="Available"),
            Item(title="Tomorrow Food", category="Food", expiry_date=tomorrow, status="Available"),
            Item(title="Misc Item No Expiry", category="Misc", expiry_date=None, status="Available"),
            Item(title="Expired Food (Yesterday)", category="Food", expiry_date=yesterday, status="Available"),
            Item(title="Taken Expired Food", category="Food", expiry_date=yesterday, status="Taken"),
            Item(title="Taken Tomorrow Food", category="Food", expiry_date=tomorrow, status="Taken")
        ]

        for item in items:
            db.session.add(item)
        db.session.commit()

        available_items = Item.get_all_available()
        available_titles = {item.title for item in available_items}
        print("\nAvailable items returned by Item.get_all_available():")
        for title in available_titles:
            print(f"- {title}")

        # Assertions
        expected_visible = {"Today Food", "Tomorrow Food", "Misc Item No Expiry"}
        expected_hidden = {"Expired Food (Yesterday)", "Taken Expired Food", "Taken Tomorrow Food"}

        success = True
        for title in expected_visible:
            if title not in available_titles:
                print(f"[FAIL] Expected '{title}' to be visible, but it was not returned.")
                success = False
        
        for title in expected_hidden:
            if title in available_titles:
                print(f"[FAIL] Expected '{title}' to be hidden, but it was returned.")
                success = False

        if success:
            print("\n[SUCCESS] Verification Successful: Expired items are correctly hidden, and available unexpired items are shown!")
        else:
            print("\n[FAIL] Verification Failed: Some items were not filtered correctly.")

if __name__ == "__main__":
    verify_expiry()
