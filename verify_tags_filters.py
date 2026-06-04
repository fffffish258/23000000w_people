import os
from datetime import datetime, timedelta
from app import create_app
from app.models.item import Item, db

def verify_tags_filters():
    print("=== START TAGS & FILTERS VERIFICATION ===")
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("[INFO] Temporary database created & initialized.")

            # Create some dummy data
            tomorrow = (datetime.utcnow().date() + timedelta(days=1))
            db.session.add(Item(title="Apple", category="Food", expiry_date=tomorrow))
            db.session.add(Item(title="Banana", category="Food", expiry_date=tomorrow))
            db.session.add(Item(title="Book", category="Misc"))
            db.session.add(Item(title="Desk", category="Misc"))
            db.session.commit()
        
        print("\n[TEST 1] Accessing Index without filters (Should show all 4 items)...")
        response = client.get('/')
        assert b"Apple" in response.data
        assert b"Banana" in response.data
        assert b"Book" in response.data
        assert b"Desk" in response.data
        print("[SUCCESS] Test 1: All items loaded correctly.")

        print("\n[TEST 2] Filtering by category 'Food'...")
        response = client.get('/?cat=Food')
        assert b"Apple" in response.data
        assert b"Banana" in response.data
        assert b"Book" not in response.data
        assert b"Desk" not in response.data
        print("[SUCCESS] Test 2: Category 'Food' filter works correctly.")

        print("\n[TEST 3] Filtering by category 'Misc'...")
        response = client.get('/?cat=Misc')
        assert b"Apple" not in response.data
        assert b"Banana" not in response.data
        assert b"Book" in response.data
        assert b"Desk" in response.data
        print("[SUCCESS] Test 3: Category 'Misc' filter works correctly.")

        print("\n[TEST 4] Filtering by keyword 'Apple'...")
        response = client.get('/?q=Apple')
        assert b"Apple" in response.data
        assert b"Banana" not in response.data
        assert b"Book" not in response.data
        assert b"Desk" not in response.data
        print("[SUCCESS] Test 4: Keyword filter works correctly.")

        print("\n[TEST 5] Filtering by category 'Food' and keyword 'Banana'...")
        response = client.get('/?cat=Food&q=Banana')
        assert b"Banana" in response.data
        assert b"Apple" not in response.data
        print("[SUCCESS] Test 5: Category and Keyword combined filter works correctly.")

    print("\n=== ALL TAGS & FILTERS VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    verify_tags_filters()
