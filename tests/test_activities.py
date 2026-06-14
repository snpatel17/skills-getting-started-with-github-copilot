def test_get_activities(client, reset_activities):
    """Test GET /activities endpoint returns all activities."""
    # Arrange
    # (activities are already set up by the fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_activities_have_required_fields(client, reset_activities):
    """Test that each activity has all required fields."""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Missing field '{field}' in {activity_name}"
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_activities_have_participants(client, reset_activities):
    """Test that activities have initial participants."""
    # Arrange
    expected_participants = {
        "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
        "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"]
    }
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    for activity_name, expected_emails in expected_participants.items():
        assert activity_name in data
        actual_participants = data[activity_name]["participants"]
        for email in expected_emails:
            assert email in actual_participants
