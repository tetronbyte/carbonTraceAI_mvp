"""Live market-feed fetchers — EUA carbon price and FX rates.

Both fall back to the static `lookup_tables` values if the HTTP call fails,
so the calc engine is never blocked by a missing internet connection.

Cache lifetime: 6 hours (configurable). Stored in-process via functools.lru_cache.

Sources:
  - EUA: ICE Exchange has no free public API. We use the free Frankfurter
    proxy for EUR exchange rates and a Sandbag / Ember weekly snapshot for
    EUA (override via CARBONTRACE_EUA_OVERRIDE env for live demos).
  - FX:  https://api.frankfurter.app (ECB-based daily rates, free, no key).
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

import requests

from src.utils.logger import get_logger

from . import lookup_tables as lut

log = get_logger(__name__)


@dataclass
class MarketSnapshot:
    eua_eur_per_tco2e: float
    eua_source: str
    fx_to_eur: dict[str, float]
    fx_source: str
    fetched_at: float

    @property
    def age_seconds(self) -> float:
        return time.time() - self.fetched_at


_CACHE: Optional[MarketSnapshot] = None
_CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours
_FRANKFURTER_TIMEOUT = 4.0


def get_market_snapshot(*, force_refresh: bool = False) -> MarketSnapshot:
    """Returns a cached snapshot, refreshing if expired or forced."""
    global _CACHE
    if not force_refresh and _CACHE and _CACHE.age_seconds < _CACHE_TTL_SECONDS:
        return _CACHE

    eua_price, eua_src = _fetch_eua()
    fx_table, fx_src = _fetch_fx_table()
    _CACHE = MarketSnapshot(
        eua_eur_per_tco2e=eua_price,
        eua_source=eua_src,
        fx_to_eur=fx_table,
        fx_source=fx_src,
        fetched_at=time.time(),
    )
    log.info(
        "Market snapshot refreshed: EUA=%.2f EUR/tCO2e (%s), FX=%s (%s)",
        eua_price, eua_src, list(fx_table)[:6], fx_src,
    )
    return _CACHE


def _fetch_eua() -> tuple[float, str]:
    """Free EUA spot price feeds are scarce. Allow override via env, else
    fall back to the static lookup-table value with a stale tag."""
    override = os.getenv("CARBONTRACE_EUA_OVERRIDE")
    if override:
        try:
            return float(override), "env override"
        except ValueError:
            log.warning("CARBONTRACE_EUA_OVERRIDE not numeric — falling back")
    # No free public ICE feed; use static reference. Replace with a paid
    # provider (Refinitiv / Bloomberg) when wiring production.
    return lut.EUA_PRICE_EUR_PER_TCO2E, "static reference (lookup_tables)"


def _fetch_fx_table() -> tuple[dict[str, float], str]:
    """Fetch ECB daily rates from Frankfurter. Returns local→EUR multipliers."""
    needed = ("USD", "ZAR", "MZN", "MAD", "EGP")
    try:
        url = f"https://api.frankfurter.app/latest?to={','.join(needed)}&from=EUR"
        r = requests.get(url, timeout=_FRANKFURTER_TIMEOUT)
        r.raise_for_status()
        payload = r.json()
        # Frankfurter gives EUR→local. We invert to get local→EUR.
        rates = payload.get("rates", {})
        fx = {"EUR": 1.0}
        for ccy, eur_to_local in rates.items():
            if eur_to_local and eur_to_local > 0:
                fx[ccy] = round(1.0 / float(eur_to_local), 6)
        # MZN often missing — keep the static fallback
        for ccy in needed:
            fx.setdefault(ccy, lut.fx_to_eur(ccy))
        return fx, f"ECB via Frankfurter (date={payload.get('date', '?')})"
    except (requests.RequestException, ValueError) as e:
        log.warning("FX fetch failed (%s) — using static table", e)
        return dict(lut.FX_TO_EUR), "static fallback (Frankfurter unreachable)"


# -----------------------------------------------------------------------------
# Convenience getters the engine uses (with cached refresh)
# -----------------------------------------------------------------------------

def current_eua_price() -> float:
    return get_market_snapshot().eua_eur_per_tco2e


def current_fx_to_eur(currency: str) -> float:
    snap = get_market_snapshot()
    return snap.fx_to_eur.get(currency.upper(), lut.fx_to_eur(currency))


def market_provenance() -> dict[str, str]:
    """For the audit trail — what feeds produced today's numbers."""
    snap = get_market_snapshot()
    return {
        "eua_source": snap.eua_source,
        "fx_source": snap.fx_source,
        "fetched_age_seconds": str(int(snap.age_seconds)),
    }
