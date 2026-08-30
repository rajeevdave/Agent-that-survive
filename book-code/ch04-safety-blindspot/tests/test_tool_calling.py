"""Tests for Chapter 4: Tool Calling."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../tests"))

import json
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from minimal.main import get_weather, calculate, run_tool_agent
from mocks.mock_provider import MockProvider
from agentic_patterns.llm.providers.base import Message


class TestToolFunctions:
    def test_get_weather_known_city(self):
        result = get_weather("london", "celsius")
        assert result["city"] == "london"
        assert isinstance(result["temperature"], (int, float))
        assert "condition" in result

    def test_get_weather_fahrenheit_conversion(self):
        celsius_result = get_weather("london", "celsius")
        fahrenheit_result = get_weather("london", "fahrenheit")
        expected_f = int(celsius_result["temperature"] * 9 / 5 + 32)
        assert fahrenheit_result["temperature"] == expected_f

    def test_get_weather_unknown_city_returns_defaults(self):
        result = get_weather("unknowncity")
        assert "temperature" in result
        assert "condition" in result

    def test_calculate_basic_arithmetic(self):
        result = calculate("2 + 2")
        assert result["result"] == 4

    def test_calculate_complex_expression(self):
        result = calculate("15 * 7 + 3")
        assert result["result"] == 108

    def test_calculate_rejects_unsafe_expressions(self):
        result = calculate("__import__('os').system('ls')")
        assert "error" in result

    def test_calculate_handles_division_by_zero(self):
        result = calculate("1 / 0")
        assert "error" in result


class TestToolAgent:
    def test_agent_returns_string(self):
        mock = MockProvider(responses=["The weather is nice."])
        result = run_tool_agent("What is the weather?", llm=mock)
        assert isinstance(result, str)

    def test_agent_handles_tool_call_then_response(self):
        """Agent calls tool, receives result, produces final answer."""
        tool_call = [{
            "id": "call_001",
            "type": "function",
            "function": {"name": "get_weather", "arguments": '{"city": "london"}'},
        }]
        mock = MockProvider(
            responses=["", "The weather in London is 15°C and cloudy."],
            tool_calls_sequence=[tool_call, []],
        )
        result = run_tool_agent("Weather in London?", llm=mock)
        assert "london" in result.lower() or "15" in result or "cloudy" in result.lower()
