import requests
import time
import threading

GEO_API = "http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,isp,org,query,message"
GEO_CACHE_TTL = 60 * 60 * 24  # 1 day cache

geo_cache = {}
geo_cache_lock = threading.Lock()


def geo_lookup(ip):
    """Lookup IP geolocation, with caching. Returns dict or None."""
    with geo_cache_lock:
        entry = geo_cache.get(ip)
        if entry and time.time() - entry[0] < GEO_CACHE_TTL:
            return entry[1]

    try:
        resp = requests.get(GEO_API.format(ip=ip), timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                result = {
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "isp": data.get("isp") or data.get("org"),
                    "query": data.get("query"),
                }
            else:
                result = {"error": data.get("message")}
        else:
            result = {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        result = {"error": str(e)}

    with geo_cache_lock:
        geo_cache[ip] = (time.time(), result)

    return result
