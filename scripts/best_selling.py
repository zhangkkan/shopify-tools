from utils.shopify_client import ShopifyClient
from datetime import datetime, timedelta, timezone

def run_best_selling_sort():
    client = ShopifyClient()
    now = datetime.now(timezone.utc)
    date_30d_ago = now - timedelta(days=30)
    print("date_30d_ago: ", date_30d_ago)


    # 获取销量统计
    sales_map = client.get_order_sales_since(date_30d_ago)
    all_products = client.get_all_products()

    new_products = []
    best_sellers = []
    unsold = []

    for p in all_products:
        pid = p["id"]
        created = p["created_at"]
        sales = sales_map.get(pid, 0)

        if sales > 0:
            best_sellers.append((pid, sales))
        elif created > date_30d_ago:
            new_products.append((pid, created))
        else:
            unsold.append((pid, created))

    best_sellers.sort(key=lambda x: -x[1])
    new_products.sort(key=lambda x: -x[1].timestamp())
    unsold.sort(key=lambda x: -x[1].timestamp())

    best_ids = [pid for pid, _ in best_sellers]
    new_ids = [pid for pid, _ in new_products[:4]]

    while len(new_ids) < 4 and best_ids:
        new_ids.append(best_ids.pop(0))

    final_ids = best_ids[:4] + new_ids + best_ids[4:] + [pid for pid, _ in unsold]
    client.reorder_collection(os.getenv("COLLECTION_GID"), final_ids)

if __name__ == "__main__":
    import os
    run_best_selling_sort()