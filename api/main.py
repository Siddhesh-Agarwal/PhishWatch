import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyUrl

from core import (
    add_data,
    get_domain,
    has_favicon,
    has_valid_dns_record,
    has_valid_ssl_certs,
    is_blacklisted,
    is_not_forwarding,
    is_registered_recently,
    is_using_free_hosting,
    uses_https,
)
from models.Response import CheckListDict, Response

load_dotenv()

DEBUG: bool = True
URI: str = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

app = FastAPI(
    title="PhishWatch",
    debug=DEBUG,
    docs_url="/",
    description="PhishWatch is a tool to help you identify phishing sites.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/check")
async def check(URL: AnyUrl) -> Response:
    url = str(URL)
    domain: str = get_domain(url)
    isPhishing: bool = False
    reasons: list[CheckListDict] = []

    # Check if the URL is not using HTTPS
    if not uses_https(url):
        isPhishing = True
        reasons.append(
            {
                "reason": "Not using HTTPS",
                "intensity": "high",
            }
        )

    # Check if the URL is blacklisted
    if is_blacklisted(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Blacklisted site",
                "intensity": "high",
            }
        )

    # Check if the URL is using a free hosting service
    if is_using_free_hosting(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Using free hosting service",
                "intensity": "medium",
            }
        )

    # Check if the URL is registered for less than 1 year
    if is_registered_recently(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Registered in past 1 years",
                "intensity": "medium",
            }
        )

    # Check if the domain has a valid DNS record
    if not has_valid_dns_record(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Invalid DNS record",
                "intensity": "low",
            }
        )

    # Check if the domain is using a URL shortening service
    # Check if the domain is using a website forwarding service
    if is_not_forwarding(url):
        isPhishing = True
        reasons.append(
            {
                "reason": "Using forwarding/URL shortening service",
                "intensity": "medium",
            }
        )

    # Check if the domain is having valid SSL certificate
    # check if the domain is using a missing HTTP Secure Headers
    # checks if the url returns a 404 response code or not
    if not has_valid_ssl_certs(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Invalid SSL certificate",
                "intensity": "high",
            }
        )

    # Check is the domain has a favicon or not
    if not has_favicon(domain):
        isPhishing = True
        reasons.append(
            {
                "reason": "Missing favicon",
                "intensity": "low",
            }
        )

    data = Response(url=URL, isPhishing=isPhishing, reasons=reasons)
    add_data(data, URI)
    return data
