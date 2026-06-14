def test_signup_success(client, reset_activities):
    """Test successful signup adds student to activity."""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert new_email in data["message"]
    assert activity_name in data["message"]


def test_signup_activity_not_found(client, reset_activities):
    """Test signup fails when activity doesn't exist."""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    valid_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup?email={valid_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered(client, reset_activities):
    """Test signup fails when student is already registered."""
    # Arrange
    activity_name = "Chess Club"
    already_registered_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={already_registered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_reflects_in_activities_list(client, reset_activities):
    """Test that successful signup updates the activities list."""
    # Arrange
    activity_name = "Programming Class"
    new_email = "test@mergington.edu"
    
    # Act - Sign up the student
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    assert signup_response.status_code == 200
    
    # Act - Fetch updated activities
    activities_response = client.get("/activities")
    
    # Assert
    assert activities_response.status_code == 200
    data = activities_response.json()
    assert new_email in data[activity_name]["participants"]


def test_signup_multiple_students(client, reset_activities):
    """Test multiple students can signup for the same activity."""
    # Arrange
    activity_name = "Art Club"
    students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
    
    # Act - Sign up multiple students
    for email in students:
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Assert - Verify all are in the activity
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    for email in students:
        assert email in participants
