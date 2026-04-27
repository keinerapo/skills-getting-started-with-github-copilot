from src import app as app_module


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = app_module.activities

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_adds_a_participant_to_activity(client):
    # Arrange
    activity_name = "Science Club"
    email = "new-student@mergington.edu"

    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_delete_signup_removes_a_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_delete_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_delete_signup_returns_404_for_participant_not_in_activity(client):
    # Arrange
    activity_name = "Science Club"
    email = "student@mergington.edu"

    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}