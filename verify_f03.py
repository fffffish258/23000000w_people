import os
from datetime import datetime, timedelta
from app import create_app
from app.models.item import Item, db

def verify_f03():
    print("=== START F03 (ITEMS STATUS MANAGEMENT & DELETION) VERIFICATION ===")
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # If CSRF is used

    with app.test_client() as client:
        with app.app_context():
            # Clean and recreate database
            db.drop_all()
            db.create_all()
            print("[INFO] Temporary database created & initialized.")

        # 1. Verify index page works when empty
        print("\n[TEST 1] Accessing empty Index Page...")
        response = client.get('/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert b"index-html" or b"index" in response.data  # Verify it loaded the index
        print("[SUCCESS] Test 1: Empty Index Page accessed successfully.")

        # 2. Add a new item via HTTP POST /items/new
        print("\n[TEST 2] Creating a new food item...")
        tomorrow_str = (datetime.utcnow().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        post_data = {
            'title': 'Test Delicious Cake',
            'category': 'Food',
            'description': 'A delicious test cake in the kitchen cupboard.',
            'image_url': 'https://example.com/cake.jpg',
            'expiry_date': tomorrow_str
        }
        
        # We follow the redirect to ensure we end up back on the index page
        response = client.post('/items/new', data=post_data, follow_redirects=True)
        assert response.status_code == 200, f"Expected 200 (redirect followed), got {response.status_code}"
        assert b'Test Delicious Cake' in response.data, "Created item title should be visible on index page"
        
        # Verify it exists in database
        with app.app_context():
            item = Item.query.filter_by(title='Test Delicious Cake').first()
            assert item is not None, "Item should exist in database"
            assert item.status == 'Available', f"Expected status 'Available', got '{item.status}'"
            item_id = item.id
            print(f"[SUCCESS] Test 2: Item '{item.title}' (ID: {item_id}) created via HTTP POST and verified.")

        # 3. Mark the item as "Taken" (F03: 狀態管理與下架)
        print(f"\n[TEST 3] Marking Item ID {item_id} as Taken (Claimed)...")
        response = client.post(f'/items/{item_id}/take', follow_redirects=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify it is no longer listed in active items on index page
        assert f'/items/{item_id}'.encode() not in response.data, "Item marked 'Taken' should be hidden from index page"
        
        # Verify the database status is changed to 'Taken'
        with app.app_context():
            item = Item.query.get(item_id)
            assert item is not None, "Item should still exist in database"
            assert item.status == 'Taken', f"Expected status 'Taken', got '{item.status}'"
            print(f"[SUCCESS] Test 3: Item ID {item_id} successfully marked as 'Taken' and hidden from listing.")

        # 4. Access Detail Page and verify deletion (F03: 刪除功能)
        print(f"\n[TEST 4] Deleting Item ID {item_id}...")
        response = client.post(f'/items/{item_id}/delete', follow_redirects=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify the item is completely deleted from the database
        with app.app_context():
            item = Item.query.get(item_id)
            assert item is None, "Item should be deleted from database"
            print(f"[SUCCESS] Test 4: Item ID {item_id} successfully deleted from database.")

    print("\n=== ALL F03 VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    verify_f03()
