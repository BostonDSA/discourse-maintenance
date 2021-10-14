from pprint import pprint
import os

from pydiscourse import DiscourseClient

client = DiscourseClient(
        'https://vote.bostondsa.org',
        api_username=os.environ.get('DISCOURSE_API_USER'),
        api_key=os.environ.get('DISCOURSE_API_KEY')
)

cats_to_archive = [
    '2021',
    '2020',
    '2019',
    '2019 - Chapter annual convention'
]

cat_ids = []
categories = client.categories()

for category in categories:
    if category['name'] not in cats_to_archive:
        continue

    cat_ids.append(category['id'])
    if category['has_children']:
        cat_ids += category['subcategory_ids']

for cat_id in cat_ids:
    cat = client._get(f"/c/{cat_id}/show.json")['category']

    # Permission types
    # 1: Create, Reply, See
    # 2: Reply, See
    # 3: See

    body = {
        "name": cat['name'],
        "permissions[admins]": 1,
        "permissions[moderators]": 1,
        "permissions[everyone]": 3
    }
    print(f"Updating category {cat_id}...", end="")
    resp = client._put(f"/categories/{cat_id}.json", **body)
    print("success" if resp else "failed")


