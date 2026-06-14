def test_full_signup_and_unregister_workflow(client, reset_activities):
    """Test complete workflow: signup → verify → unregister → verify."""
    # Arrange
    activity_name = "Robotics Club"
    email = "integration_test@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Assert - Verify signup
    check_response_1 = client.get("/activities")
    assert email in check_response_1.json()[activity_name]["participants"]
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Assert - Verify unregister
    check_response_2 = client.get("/activities")
    assert email not in check_response_2.json()[activity_name]["participants"]


def test_activity_capacity_tracking(client, reset_activities):
    """Test that participant count and capacity are tracked correctly."""
    # Arrange
    activity_name = "Chess Club"
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"]
    initial_count = len(initial_participants)
    max_capacity = initial_response.json()[activity_name]["max_participants"]
    
    # Act - Add a new participant
    new_email = "new_chess_player@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Act - Fetch updated activity
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    updated_count = len(updated_participants)
    
    # Assert
    assert updated_count == initial_count + 1
    assert new_email in updated_participants
    assert max_capacity > updated_count  # Still under capacity
