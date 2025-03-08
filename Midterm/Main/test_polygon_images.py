import requests
import os

# Use your API key
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "8k2Yd07IqDprBnrMMmG5opfVqeMMrA2y")

def test_polygon_image(ticker):
    """Fetch branding info (image URLs) for a given ticker from Polygon API."""
    url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "results" not in data:
            print(f"❌ ERROR: Ticker '{ticker}' not found.")
            return

        branding = data["results"].get("branding", {})
        logo_url = branding.get("logo_url", "").strip()  # Usually SVG
        icon_url = branding.get("icon_url", "").strip()  # Usually PNG

        # Ensure URLs are complete
        if logo_url and not logo_url.startswith("http"):
            logo_url = f"https://api.polygon.io{logo_url}"
        if icon_url and not icon_url.startswith("http"):
            icon_url = f"https://api.polygon.io{icon_url}"

        print(f"\n🔹 **Testing {ticker}**")
        print(f"✅ Logo URL (SVG): {logo_url if logo_url else 'N/A'}")
        print(f"✅ Icon URL (PNG): {icon_url if icon_url else 'N/A'}")

        # Test if the image URL is actually valid
        if icon_url:
            img_response = requests.get(icon_url)
            if img_response.status_code == 200:
                print(f"🟢 {ticker} icon (PNG) is valid!")
            else:
                print(f"🔴 {ticker} icon (PNG) is NOT loading! Status: {img_response.status_code}")

        if logo_url:
            img_response = requests.get(logo_url)
            if img_response.status_code == 200:
                print(f"🟢 {ticker} logo (SVG) is valid!")
            else:
                print(f"🔴 {ticker} logo (SVG) is NOT loading! Status: {img_response.status_code}")

    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {str(e)}")

# ✅ Test some tickers
tickers_to_test = ["AAPL", "NVDA", "TSLA", "INVALIDTICKER"]
for ticker in tickers_to_test:
    test_polygon_image(ticker)
