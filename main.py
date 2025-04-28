import google.auth
from googleapiclient.discovery import build

# Authenticate using Application Default Credentials
credentials, project = google.auth.default()
service = build('cloudbilling', 'v1', credentials=credentials)

def get_storage_price():
    service_name = "services/6F81-5844-456A"  # This is the service ID for Cloud Storage
    request = service.services().skus().list(parent=service_name)
    response = request.execute()

    # Look for the relevant SKU
    for sku in response.get('skus', []):
        if 'Storage' in sku['description'] and 'Standard Storage' in sku['description'] and 'Multi-Regional' in sku['description']:
            pricing_info = sku['pricingInfo'][0]
            price_per_gb = pricing_info['pricingExpression']['tieredRates'][0]['unitPrice']
            units = int(price_per_gb.get('units', 0))
            nanos = int(price_per_gb.get('nanos', 0))
            price_in_usd = units + nanos / 1e9
            return price_in_usd
    
    raise Exception("Could not find standard multi-regional storage price.")

def calculate_cost(storage_gb):
    price_per_gb = get_storage_price()
    total_cost = storage_gb * price_per_gb
    return total_cost

if __name__ == "__main__":
    storage_size_gb = 10
    cost = calculate_cost(storage_size_gb)
    print(f"Estimated monthly cost for {storage_size_gb} GB in Cloud Storage: ${cost:.4f}")

