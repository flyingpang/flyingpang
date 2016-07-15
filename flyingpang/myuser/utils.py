# coding: utf-8
import functools
import urlparse
from django.core.exceptions import SuspiciousOperation


def default_redirect(request, fallback_url, **kwargs):
    """
     Evaluates a redirect url by consulting GET POST and the session.
    """

    redirect_field_name = kwargs.get("redirect_field_name", "next")
    # next = request.REQUEST.get(redirect_field_name)
    next = request.GET.get('next', None)
    if not next:
        # try the session if available
        if hasattr(request, "session"):
            session_key_values = kwargs.get("session_key_value", "redirect_to")
            next = request.session.get(session_key_values)
    is_safe = functools.partial(
        ensure_safe_url,
        allowed_protocols=kwargs.get("allowed_protocols"),
        allowed_host=request.get_host()
    )

    redirect_to = next if next and is_safe(next) else fallback_url
    is_safe(redirect_to, raise_on_fail=True)
    return redirect_to


def ensure_safe_url(url, allowed_protocols=None, allowed_host=None, raise_on_fail=False):
    if allowed_protocols is None:
        allowed_protocols = ["http", "https"]
    parsed = urlparse.urlparse(url)
    # perform security checks to ensure no malicious intent
    # (i.e an XSS attack with a data URL)
    safe = True
    if parsed.scheme and parsed.scheme not in allowed_protocols:
        if raise_on_fail:
            raise SuspiciousOperation("Unsafe redirect to URL with protocol '%s'" % allowed_host)
        safe = False
    return safe
