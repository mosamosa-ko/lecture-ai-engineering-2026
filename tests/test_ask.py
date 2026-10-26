from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_token_usage_and_returns_response_text(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
    )

    class FakeModels:
        def generate_content(self, *, model, contents):
            assert model == ask_module.MODEL
            assert contents == "質問"
            return response

    class FakeClient:
        models = FakeModels()

        def __init__(self, *, api_key):
            assert api_key == "test-api-key"

    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-api-key")
    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)

    assert ask_module.ask("質問") == "回答"
    assert "[usage] 入力トークン数: 12, 出力トークン数: 34" in capsys.readouterr().out
