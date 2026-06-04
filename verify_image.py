import os
from datetime import datetime, timedelta
from app import create_app
from app.models.item import Item, db

def verify_image():
    print("=== START IMAGE DISPLAY FUNCTIONALITY VERIFICATION ===")
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            # Clean and recreate database
            db.drop_all()
            db.create_all()
            print("[INFO] Temporary database created & initialized.")

        # 1. Test case: Item WITH image_url
        print("\n[TEST 1] Creating an item with an image URL...")
        tomorrow_str = (datetime.utcnow().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        post_data_with_img = {
            'title': 'Apple Pie with Image',
            'category': 'Food',
            'description': 'Freshly baked apple pie.',
            'image_url': 'https://example.com/apple_pie.png',
            'expiry_date': tomorrow_str
        }
        
        response = client.post('/items/new', data=post_data_with_img, follow_redirects=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Verify database record
        with app.app_context():
            item_with_img = Item.query.filter_by(title='Apple Pie with Image').first()
            assert item_with_img is not None, "Item should exist in database"
            assert item_with_img.image_url == 'https://example.com/apple_pie.png', f"Expected image_url 'https://example.com/apple_pie.png', got '{item_with_img.image_url}'"
            item_with_img_id = item_with_img.id
            print(f"[SUCCESS] Database record verified for ID {item_with_img_id}.")

        # Verify index page shows the image thumbnail with correct URL
        print("[TEST 2] Verifying image thumbnail on Index Page for item with image...")
        response = client.get('/')
        assert response.status_code == 200
        # The index template should render an img tag with the src attribute containing the image url
        expected_img_tag = f'src="https://example.com/apple_pie.png"'
        assert expected_img_tag.encode() in response.data, "Index page should display the image URL as the img src"
        print("[SUCCESS] Index page correctly displays the image thumbnail.")

        # Verify detail page shows the detail image with correct URL
        print("[TEST 3] Verifying image on Detail Page for item with image...")
        response = client.get(f'/items/{item_with_img_id}')
        assert response.status_code == 200
        assert expected_img_tag.encode() in response.data, "Detail page should display the image URL as the img src"
        print("[SUCCESS] Detail page correctly displays the item image.")

        # 2. Test case: Item WITHOUT image_url (or empty/whitespace)
        print("\n[TEST 4] Creating an item without an image URL...")
        post_data_no_img = {
            'title': 'Banana Bread No Image',
            'category': 'Food',
            'description': 'Homemade banana bread.',
            'image_url': '   ', # Whitespace to test stripping
            'expiry_date': tomorrow_str
        }
        
        response = client.post('/items/new', data=post_data_no_img, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify database record
        with app.app_context():
            item_no_img = Item.query.filter_by(title='Banana Bread No Image').first()
            assert item_no_img is not None, "Item should exist in database"
            assert item_no_img.image_url == '', f"Expected empty image_url string, got '{item_no_img.image_url}'"
            item_no_img_id = item_no_img.id
            print(f"[SUCCESS] Database record verified for ID {item_no_img_id} (image_url is empty).")

        # Verify index page shows "無圖片" placeholder instead of img tag
        print("[TEST 5] Verifying no-image placeholder on Index Page...")
        response = client.get('/')
        assert response.status_code == 200
        assert "無圖片" in response.data.decode('utf-8'), "Index page should display '無圖片' placeholder"
        print("[SUCCESS] Index page correctly displays '無圖片' placeholder.")

        # Verify detail page shows "暫無物品圖片" placeholder instead of img tag
        print("[TEST 6] Verifying no-image placeholder on Detail Page...")
        response = client.get(f'/items/{item_no_img_id}')
        assert response.status_code == 200
        assert "暫無物品圖片" in response.data.decode('utf-8'), "Detail page should display '暫無物品圖片' placeholder"
        print("[SUCCESS] Detail page correctly displays '暫無物品圖片' placeholder.")

    print("\n=== ALL IMAGE DISPLAY FUNCTIONALITY VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    verify_image()
