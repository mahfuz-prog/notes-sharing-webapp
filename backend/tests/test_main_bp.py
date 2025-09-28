from flaskapp.db_models import Notes


def test_homepage_stats(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

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

    response = client.get("/api-v1/main/home/")
    data = response.get_json()

    assert response.status_code == 200
    assert "totalUser" in data
    assert "totalNotes" in data
    assert "totalChar" in data
    assert data["totalUser"] == 1
    assert data["totalNotes"] == 100


# single note endpoint
def test_single_note(client, db_session, test_note_1, test_user_1):
    db_session.add(test_note_1)
    db_session.commit()

    payload = {
        "username": test_user_1.username,
        "note_id": str(test_note_1.id),
        "pin": test_note_1.pin,
    }
    response = client.post("/api-v1/main/single-note/", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert "pin" not in data
    assert "isLocked" not in data
    assert "date" in data
    assert data["username"] == test_user_1.username
    assert data["title"] == test_note_1.title
    assert data["text"] == test_note_1.text


# single note endpoint error
def test_test_single_note_error(client, db_session, test_note_1, test_user_1):
    db_session.add(test_note_1)
    db_session.commit()

    # pin required
    payload = {"username": test_user_1.username, "note_id": str(test_note_1.id)}
    response = client.post("/api-v1/main/single-note/", json=payload)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Pin required"

    # pin mismatch
    payload = {
        "username": test_user_1.username,
        "note_id": str(test_note_1.id),
        "pin": "invalid",
    }
    response = client.post("/api-v1/main/single-note/", json=payload)
    assert response.status_code == 403
    assert response.get_json()["error"] == "Invalid pin"


# test user profile endpoint
def test_user_profile(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

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

    response = client.get(f"/api-v1/main/user-profile/{test_user_1.username}/")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 100
    assert "id" in data[0]
    assert "title" in data[0]
    assert "dateCreated" in data[0]
    assert "isLocked" in data[0]
