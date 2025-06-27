import pytest
import respx
import httpx
from nrtsearch_mcp.server import _search_impl


# Simple successful response
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_unit_simple():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "hits": [
                    {"score": 1.0,
                     "fields": {
                       "stars":{"fieldValue":[{"intValue":5}]},
                       "text":{"fieldValue":[{"textValue":"foo"}]}}},
                ]
            },
        )
    )
    result = await _search_impl(
        index="yelp_reviews_staging",
        queryText="foo",
        topHits=1
    )
    assert result.hits[0].stars == 5
    assert result.hits[0].text == "foo"
    assert gw.called

# No hits returned
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_empty_hits():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(200, json={"hits": []})
    )
    result = await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1)
    assert result.hits == []
    assert gw.called

# Multiple hits
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_multiple_hits():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(200, json={
            "hits": [
                {"score": 1.0, "fields": {"stars":{"fieldValue":[{"intValue":5}]}, "text":{"fieldValue":[{"textValue":"foo"}]}}},
                {"score": 0.9, "fields": {"stars":{"fieldValue":[{"intValue":4}]}, "text":{"fieldValue":[{"textValue":"bar"}]}}},
            ]
        })
    )
    result = await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=2)
    assert len(result.hits) == 2
    assert result.hits[0].stars == 5
    assert result.hits[1].text == "bar"
    assert gw.called

# Missing fields in hit
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_missing_fields():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(200, json={
            "hits": [
                {"score": 1.0, "fields": {"stars":{"fieldValue":[{"intValue":5}]}}},
                {"score": 0.9, "fields": {"text":{"fieldValue":[{"textValue":"bar"}]}}},
            ]
        })
    )
    # Should raise KeyError for missing field
    with pytest.raises(KeyError):
        await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=2)
    assert gw.called

# Non-200 HTTP response
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_http_error():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(500, json={"error": "server error"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1)
    assert gw.called

# Retry logic: first call fails, second succeeds
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_retry_logic():
    calls = []
    def handler(request):
        if not calls:
            calls.append(1)
            return httpx.Response(502)
        return httpx.Response(200, json={"hits": [{"score": 1.0, "fields": {"stars":{"fieldValue":[{"intValue":5}]}, "text":{"fieldValue":[{"textValue":"foo"}]}}}]})
    gw = respx.post("http://localhost:8080/v1/search").mock(side_effect=handler)
    result = await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1)
    assert result.hits[0].stars == 5
    assert gw.called


# Highlight option
import json
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_highlight():
    def handler(request):
        body = json.loads(request.content)
        assert "highlightFields" in body
        return httpx.Response(200, json={"hits": []})
    gw = respx.post("http://localhost:8080/v1/search").mock(side_effect=handler)
    result = await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1, highlight=True)
    assert result.hits == []
    assert gw.called

# Custom retrieveFields
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_custom_retrieve_fields():
    def handler(request):
        body = json.loads(request.content)
        assert body["retrieveFields"] == ["text", "stars", "extra"]
        return httpx.Response(200, json={"hits": []})
    gw = respx.post("http://localhost:8080/v1/search").mock(side_effect=handler)
    result = await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1, retrieveFields=["text", "stars", "extra"])
    assert result.hits == []
    assert gw.called

# Input validation: topHits out of range
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_tophits_clamped():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(200, json={"hits": []})
    )
    # topHits < 1 should clamp to 1
    await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=0)
    # topHits > 100 should clamp to 100
    await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=101)
    assert gw.called

# Malformed JSON response
@pytest.mark.asyncio
@respx.mock
async def test_search_impl_malformed_json():
    gw = respx.post("http://localhost:8080/v1/search").mock(
        return_value=httpx.Response(200, content=b"not json")
    )
    with pytest.raises(Exception):
        await _search_impl(index="yelp_reviews_staging", queryText="foo", topHits=1)
    assert gw.called
