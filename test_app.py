import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app import create_app

app = create_app()
app.testing = True

def run_tests():
    with app.test_client() as client:
        # 1. Create
        resp = client.post('/items/new', data={
            'title': 'API Test Item',
            'category': 'Misc',
            'description': 'Test create'
        }, follow_redirects=True)
        if b'API Test Item' not in resp.data:
            print("Create failed")
            return
        print("Create OK")

        # Get the ID of the newly created item
        from app.models.item import Item
        with app.app_context():
            item = Item.query.filter_by(title='API Test Item').first()
            if not item:
                print("Item not found in DB")
                return
            item_id = item.id

        # 2. Edit
        resp = client.post(f'/items/{item_id}/edit', data={
            'title': 'API Test Item Updated',
            'category': 'Misc',
            'description': 'Test edit'
        }, follow_redirects=True)
        if b'API Test Item Updated' not in resp.data:
            print("Edit failed")
            return
        print("Edit OK")

        # 3. Take
        resp = client.post(f'/items/{item_id}/take', follow_redirects=True)
        with app.app_context():
            item = Item.query.get(item_id)
            if item.status != 'Taken':
                print("Take failed")
                return
        print("Take OK")

        # 4. Delete
        resp = client.post(f'/items/{item_id}/delete', follow_redirects=True)
        with app.app_context():
            item = Item.query.get(item_id)
            if item is not None:
                print("Delete failed")
                return
        print("Delete OK")

if __name__ == '__main__':
    run_tests()
