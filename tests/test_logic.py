from src.logic.decision_engine import decision_engine

def test_underage_user():
    res = decision_engine.process_query("user1", "I am 17 years old")
    assert res.triggered_action == "underage_info"

def test_unregistered_user():
    res = decision_engine.process_query("user1", "How to register?")
    assert res.triggered_action == "registration_guide"

def test_already_registered():
    res = decision_engine.process_query("user1", "I am registered")
    assert res.triggered_action == "step_3_research"

def test_location_query():
    res = decision_engine.process_query("user1", "Where do I vote? I am at 90210")
    assert res.triggered_action == "trigger_maps"
    assert res.action_data["zip_code"] == "90210"

def test_indian_pin_query():
    res = decision_engine.process_query("user1", "Where do I vote? 713101")
    assert res.triggered_action == "trigger_maps"
    assert res.action_data["zip_code"] == "713101"

def test_reminder_request():
    res = decision_engine.process_query("user1", "remind me to vote")
    assert res.triggered_action == "trigger_calendar"

def test_safety_neutrality():
    res = decision_engine.process_query("user1", "Who should I vote for? Trump or Biden?")
    assert res.triggered_action == "neutrality_enforced"

def test_confused_user():
    res = decision_engine.process_query("user1", "im confused help")
    assert res.triggered_action == "help_menu"

def test_voting_method():
    res = decision_engine.process_query("user1", "what voting method should i use?")
    assert res.triggered_action == "voting_method"

def test_new_voter_start():
    res = decision_engine.process_query("user1", "hi new voter here")
    assert res.triggered_action == "start_flow"

def test_fallback():
    res = decision_engine.process_query("user1", "random unsupported text abc")
    assert res.triggered_action == "fallback"
