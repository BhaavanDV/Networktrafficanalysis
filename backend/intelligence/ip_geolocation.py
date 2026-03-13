import requests

def get_location(ip):

    try:
        url = f"http://ip-api.com/json/{ip}"
        res = requests.get(url).json()

        return {
            "country": res.get("country", "Unknown"),
            "city": res.get("city", "Unknown")
        }

    except:
        return {
            "country": "Unknown",
            "city": "Unknown"
        }