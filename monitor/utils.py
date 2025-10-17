import socket

def is_remote_address(addr):
    """Return True if address looks like a remote address."""
    if not addr:
        return False
    ip = addr[0]
    if ip.startswith("127.") or ip == "::1" or ip.startswith("169.254."):
        return False
    return True

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""
