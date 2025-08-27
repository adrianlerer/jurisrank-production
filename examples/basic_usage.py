#!/usr/bin/env python3
"""
JurisRank Basic Usage Example
============================

Demonstrates basic usage of JurisRank Free Forever API
for legal document analysis and jurisprudence search.

Run: python examples/basic_usage.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jurisrank import JurisRankAPI, get_api_info

def main():
    """Demonstrate basic JurisRank API usage."""

    print("🏛️  JurisRank Free Forever API - Basic Usage Example")
    print("=" * 55)

    # Display API information
    api_info = get_api_info()
    print(f"📊 API Version: {api_info['version']}")
    print(f"🌐 Base URL: {api_info['api_base_url']}")
    print(f"🆓 Free Tier: {api_info['free_tier']}")
    print(f"🗣️  Languages: {', '.join(api_info['supported_languages'])}")
    print()

    # Initialize API client (replace with your free API key)
    api_key = os.getenv("JURISRANK_API_KEY", "demo_key_get_yours_at_api_jurisrank_io")
    client = JurisRankAPI(api_key=api_key)

    print("🔑 API Client initialized")
    print(f"🔗 Using API key: {api_key[:20]}...")
    print()

    # Example 1: Analyze a legal document
    print("📄 Example 1: Legal Document Analysis")
    print("-" * 40)

    # Note: In real usage, provide path to actual PDF/DOCX file
    sample_doc_path = "sample_legal_document.pdf"

    try:
        result = client.analyze_document(sample_doc_path)
        print(f"📑 Document ID: {result.document_id}")
        print(f"⭐ Authority Score: {result.authority_score}/100")
        print(f"🎯 Confidence: {result.confidence:.2%}")
        print(f"📝 Summary: {result.analysis_summary}")
    except Exception as e:
        print(f"⚠️  Note: {e} (This is expected in demo mode)")

    print()

    # Example 2: Search jurisprudence
    print("🔍 Example 2: Jurisprudence Search")
    print("-" * 35)

    search_query = "contract breach damages"
    jurisdiction = "global"

    try:
        results = client.search_jurisprudence(search_query, jurisdiction=jurisdiction)
        print(f"🔎 Query: '{search_query}'")
        print(f"🌍 Jurisdiction: {jurisdiction}")
        print(f"📚 Found {len(results)} relevant cases:")

        for i, doc in enumerate(results[:3], 1):
            print(f"  {i}. {doc.title}")
            print(f"     Court: {doc.court} | Authority: {doc.authority_score}/100")
    except Exception as e:
        print(f"⚠️  Note: {e} (This is expected in demo mode)")

    print()

    # Example 3: Get authority score
    print("⚖️  Example 3: Authority Scoring")
    print("-" * 32)

    court_name = "Supreme Court"

    try:
        authority = client.get_authority_score(court_name)
        print(f"🏛️  Court: {court_name}")
        print(f"📊 Authority Score: {authority}/100")
    except Exception as e:
        print(f"⚠️  Note: {e} (This is expected in demo mode)")

    print()
    print("✨ Ready to revolutionize your legal analysis!")
    print("🚀 Get your free API key: https://api.jurisrank.io/register")

if __name__ == "__main__":
    main()
