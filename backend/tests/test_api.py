def test_create_form_success(client):
    payload = {
        "title": "Customer Feedback",
        "description": "Collect customer feedback",
        "fields": [
            {"type": "text", "label": "Name"},
            {"type": "email", "label": "Email"},
            {"type": "select", "label": "Rating", "options": ["Good", "Bad"]},
        ],
    }

    response = client.post("/forms", json=payload)
    assert response.status_code == 201

    body = response.get_json()
    assert body["title"] == "Customer Feedback"
    assert len(body["fields"]) == 3


def test_submit_response_success(client):
    form_payload = {
        "title": "Survey",
        "description": "Simple survey",
        "fields": [
            {"type": "text", "label": "Name"},
            {"type": "checkbox", "label": "Subscribe"},
        ],
    }
    form_resp = client.post("/forms", json=form_payload)
    form_id = form_resp.get_json()["id"]

    response_payload = {
        "form_id": form_id,
        "answers": {"Name": "Alice", "Subscribe": True},
    }

    response = client.post("/responses", json=response_payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["form_id"] == form_id
    assert body["answers"]["Name"] == "Alice"


def test_submit_response_missing_field_returns_422(client):
    form_payload = {
        "title": "Survey",
        "description": "Simple survey",
        "fields": [
            {"type": "text", "label": "Name"},
            {"type": "checkbox", "label": "Subscribe"},
        ],
    }
    form_resp = client.post("/forms", json=form_payload)
    form_id = form_resp.get_json()["id"]

    response_payload = {
        "form_id": form_id,
        "answers": {"Name": "Alice"},
    }

    response = client.post("/responses", json=response_payload)
    assert response.status_code == 422
    body = response.get_json()
    assert "Missing answers for fields" in body["error"]


def test_ai_generate_form_success(client):
    response = client.post("/ai/generate-form", json={"prompt": "Create a feedback form"})
    assert response.status_code == 200

    body = response.get_json()
    assert "fields" in body
    assert len(body["fields"]) >= 1
