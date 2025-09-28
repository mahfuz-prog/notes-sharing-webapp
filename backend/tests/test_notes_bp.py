from flaskapp.db_models import Notes


# logged in user all notes endpoint
def test_note_list(client, db_session, test_user_1, auth_headers_1):
    response = client.get("/api-v1/notes/", headers=auth_headers_1)
    assert response.status_code == 200

    data = response.get_json()
    assert len(data["notes"]) == 0
    assert "pagination" in response.get_json()
    assert data["pagination"]["currentPage"] == 1
    assert data["pagination"]["hasNext"] is False
    assert data["pagination"]["hasPrev"] is False

    # add 100 notes
    for i in range(1, 101):
        if i % 2 == 0:
            note = Notes(
                title=f"Note title {i}",
                text=f"Note text {i}",
                pin=f"pin{i}",
                user_id=test_user_1.id,
            )
        else:
            note = Notes(
                title=f"Note title {i}", text=f"Note text {i}", user_id=test_user_1.id
            )

        db_session.add(note)
    db_session.commit()

    response = client.get("/api-v1/notes/", headers=auth_headers_1)
    assert response.status_code == 200

    data = response.get_json()
    assert len(data["notes"]) == 6
    assert "pagination" in response.get_json()
    assert data["pagination"]["currentPage"] == 1
    assert data["pagination"]["hasNext"] is True
    assert data["pagination"]["hasPrev"] is False


# delete note endpoint
def test_delete_note(client, db_session, test_note_1, auth_headers_1, auth_headers_2):
    db_session.add(test_note_1)
    db_session.commit()

    # one user try to delete other user note
    response = client.delete(
        f"/api-v1/notes/delete-note/{test_note_1.id}/", headers=auth_headers_2
    )
    assert response.status_code == 403
    assert response.get_json()["error"] == "Delete not allowed!"

    # owner of the note successfuly delete note
    response = client.delete(
        f"/api-v1/notes/delete-note/{test_note_1.id}/", headers=auth_headers_1
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["title"] == test_note_1.title
    assert data["id"] == test_note_1.id


# create new note endpoint
def test_new_note(client, auth_headers_1, test_note_1):
    # pin protected note
    payload = {
        "title": test_note_1.title,
        "text": test_note_1.text,
        "pin": test_note_1.pin,
    }
    response = client.post(
        "/api-v1/notes/new-note/", json=payload, headers=auth_headers_1
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data["info"]["title"] == test_note_1.title
    assert data["info"]["text"] == test_note_1.text
    assert data["info"]["pin"] == test_note_1.pin

    # public note
    payload = {"title": test_note_1.title, "text": test_note_1.text, "pin": ""}
    response = client.post(
        "/api-v1/notes/new-note/", json=payload, headers=auth_headers_1
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data["info"]["title"] == test_note_1.title
    assert data["info"]["text"] == test_note_1.text
    assert data["info"]["pin"] == ""


# edit note endpoint
def test_update_note(client, db_session, test_note_1, auth_headers_1, auth_headers_2):
    db_session.add(test_note_1)
    db_session.commit()

    title = "New title"
    text = "New text"
    pin = "asdf"
    payload = {"title": title, "text": text, "pin": pin, "note_id": test_note_1.id}
    response = client.put(
        "/api-v1/notes/update-note/", json=payload, headers=auth_headers_1
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == test_note_1.id
    assert data["title"] == title
    assert data["text"] == text
    assert data["pin"] == pin

    # one user try to edit other user note
    response = client.put(
        "/api-v1/notes/update-note/", json=payload, headers=auth_headers_2
    )
    assert response.status_code == 403
    assert response.get_json()["error"] == "Delete not allowed!"
