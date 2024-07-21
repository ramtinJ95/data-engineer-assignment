from smhi.smhi import SmhiParser


def test_check_connection():
    parser = SmhiParser()
    status_code = parser.check_connection()
    assert status_code == 200, f"Expected status code 200, got {status_code}"


def test_get_list_of_parameters():
    parser = SmhiParser()
    parameters = parser.get_list_of_parameters()
    assert isinstance(parameters, list), "Expected list of parameters"
    assert len(parameters) > 0, "Expected non-empty list of parameters"
    assert all(isinstance(param, tuple) and len(
        param) == 3 for param in parameters), "Each item should be a tuple of length 3"


def test_get_active_stations():
    parser = SmhiParser()
    stations = parser.get_active_stations()
    assert isinstance(stations, list), "Expected list of active stations"
    assert len(stations) > 0, "Expected non-empty list of active stations"


def test_get_average_temps_past_day():
    parser = SmhiParser()
    active_stations = parser.get_active_stations()
    temperatures = parser.get_average_temps_past_day(active_stations)
    assert isinstance(temperatures, list), "Expected list of temperatures"
    assert len(temperatures) > 0, "Expected non-empty list of temperatures"
    assert all(isinstance(temp, tuple) and len(
        temp) == 2 and isinstance(temp[1], float) for temp in temperatures), "Each temperature entry should be a tuple of length 2"
    assert temperatures == sorted(
        temperatures, key=lambda x: x[1]), "Temperatures should be sorted by value"
