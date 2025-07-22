import requests
import os
from datetime import datetime

class ShopifyClient:
    def __init__(self):
        self.api_url = f"https://{os.getenv('SHOP_NAME')}/admin/api/2024-01/graphql.json"
        self.headers = {
            "X-Shopify-Access-Token": os.getenv("ACCESS_TOKEN"),
            "Content-Type": "application/json",
        }

    def graphql_query(self, query, variables=None):
        print("graphql_query: ", query)
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"query": query, "variables": variables or {}}
        )
        response.raise_for_status()
        print("graphql_query result: ", query)

        return response.json()

    def get_order_sales_since(self, since_date):
        query = '''
        query($cursor: String) {
          orders(first: 100, query: "created_at:>=%s", after: $cursor, reverse: true) {
            edges {
              cursor
              node {
                lineItems(first: 10) {
                  edges {
                    node {
                      product { id }
                      quantity
                    }
                  }
                }
              }
            }
            pageInfo { hasNextPage }
          }
        }
        ''' % since_date.isoformat()
        cursor = None
        sales = {}
        while True:
            result = self.graphql_query(query, {"cursor": cursor})
            edges = result["data"]["orders"]["edges"]
            for edge in edges:
                for item in edge["node"]["lineItems"]["edges"]:
                    product = item["node"]["product"]
                    if product:
                        pid = product["id"]
                        qty = item["node"]["quantity"]
                        sales[pid] = sales.get(pid, 0) + qty
            if not result["data"]["orders"]["pageInfo"]["hasNextPage"]:
                break
            cursor = edges[-1]["cursor"]
        return sales

    def get_all_products(self):
        query = '''
        query($cursor: String) {
          products(first: 100, after: $cursor) {
            edges {
              cursor
              node {
                id
                title
                createdAt
              }
            }
            pageInfo { hasNextPage }
          }
        }
        '''
        products = []
        cursor = None
        while True:
            result = self.graphql_query(query, {"cursor": cursor})
            edges = result["data"]["products"]["edges"]
            for edge in edges:
                node = edge["node"]
                products.append({
                    "id": node["id"],
                    "title": node["title"],
                    "created_at": datetime.fromisoformat(node["createdAt"].replace("Z", "+00:00"))
                })
            if not result["data"]["products"]["pageInfo"]["hasNextPage"]:
                break
            cursor = edges[-1]["cursor"]
        return products

    def reorder_collection(self, collection_gid, product_ids):
        mutation = '''
        mutation collectionReorderProducts($id: ID!, $moves: [MoveInput!]!) {
          collectionReorderProducts(id: $id, moves: $moves) {
            job { id status }
            userErrors { field message }
          }
        }
        '''
        moves = [{"productId": pid, "newPosition": i} for i, pid in enumerate(product_ids)]
        result = self.graphql_query(mutation, {"id": collection_gid, "moves": moves})
        if result["data"]["collectionReorderProducts"]["userErrors"]:
            print("Errors:", result["data"]["collectionReorderProducts"]["userErrors"])
        else:
            print("Collection sorted successfully.")