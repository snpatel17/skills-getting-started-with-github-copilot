def test_unregister_success(client, reset_activities):
    """Test successful unregister removes student from activity."""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert email_to_remove in data["message"]
    assert activity_name in data["message"]


def test_unregister_activity_not_found(client, reset_activities):
    """Test unregister fails when activity doesn't exist."""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    valid_email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/unregister?email={valid_email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered(client, reset_activities):
    """Test unregister fails when student is not registered."""
    # Arrange
    activity_name = "Chess Club"
    email_not_registered = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_not_registered}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_reflects_in_activities_list(client, reset_activities):
    """Test that successful unregister updates the activities list."""
    # Arrange
    activity_name = "Swimming Club"
    email_to_remove = "maria@mergington.edu"  # Already in Swimming Club
    
    # Verify initial state
    initial_response = client.get("/activities")
    assert email_to_remove in initial_response.json()[activity_name]["participants"]
    
    # Act - Unregister the student
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    assert unregister_response.status_code == 200
    
    # Act - Fetch updated activities
    final_response = client.get("/activities")
    
    # Assert
    assert email_to_remove not in final_response.json()[activity_name]["participants"]


def test_unregister_then_resignup(client, reset_activities):
    """Test student can re-signup after being unregistered."""
    # Arrange
    activity_name = "Debate Team"
    email = "sam@mergington.edu"
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Act - Sign up again
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert signup_response.status_code == 200
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]
