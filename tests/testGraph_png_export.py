import icesat2.graph.graph_png_export as graph_png_export

"""Unit tests for graph_png_export.py"""

def test_read_data():
    test_data = graph_png_export.read_data('resources\\csv_data_collection\\foo.csv')
    assert test_data[0] == 2
    assert test_data[4] == 9
    assert test_data[9] == 7