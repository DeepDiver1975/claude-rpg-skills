import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import generate_image as generate_image_module
from generate_image import _load_dotenv, generate_image, generate_image_bytes, main


def _install_fake_genai(monkeypatch, client_instance):
    fake_google = types.ModuleType("google")
    fake_genai_mod = types.ModuleType("google.genai")
    fake_types_mod = types.ModuleType("google.genai.types")
    fake_genai_mod.Client = MagicMock(return_value=client_instance)
    fake_types_mod.GenerateContentConfig = MagicMock(side_effect=lambda **kw: kw)
    fake_genai_mod.types = fake_types_mod
    fake_google.genai = fake_genai_mod
    monkeypatch.setitem(sys.modules, "google", fake_google)
    monkeypatch.setitem(sys.modules, "google.genai", fake_genai_mod)
    monkeypatch.setitem(sys.modules, "google.genai.types", fake_types_mod)


def _client_returning(image_bytes: bytes):
    fake_part = MagicMock()
    fake_part.inline_data.data = image_bytes
    fake_response = MagicMock(parts=[fake_part])
    client = MagicMock()
    client.models.generate_content.return_value = fake_response
    return client


def test_generate_image_bytes_returns_the_inline_data_from_the_first_image_part(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    client = _client_returning(b"\x89PNGfakepixels")
    _install_fake_genai(monkeypatch, client)

    result = generate_image_bytes("a cyberpunk portrait, neon lighting")

    assert result == b"\x89PNGfakepixels"
    kwargs = client.models.generate_content.call_args.kwargs
    assert kwargs["contents"] == "a cyberpunk portrait, neon lighting"


def test_generate_image_bytes_raises_without_any_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        generate_image_bytes("some prompt")


def test_generate_image_bytes_raises_on_empty_prompt(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    with pytest.raises(RuntimeError, match="empty"):
        generate_image_bytes("   ")


def test_generate_image_bytes_raises_clearly_when_no_part_has_inline_data(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    client = MagicMock()
    text_only_part = MagicMock(inline_data=None)
    client.models.generate_content.return_value = MagicMock(parts=[text_only_part])
    _install_fake_genai(monkeypatch, client)

    with pytest.raises(RuntimeError, match="no image"):
        generate_image_bytes("a prompt that trips the safety filter")


def test_generate_image_bytes_wraps_sdk_errors(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    client = MagicMock()
    client.models.generate_content.side_effect = RuntimeError("403 quota exceeded")
    _install_fake_genai(monkeypatch, client)

    with pytest.raises(RuntimeError, match="quota exceeded"):
        generate_image_bytes("a prompt")


def test_generate_image_reads_prompt_file_and_writes_png(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    prompt_path = tmp_path / "portrait-rook.txt"
    prompt_path.write_text("chest-up portrait, neon-lit alley", encoding="utf-8")
    client = _client_returning(b"FAKEPNGBYTES")
    _install_fake_genai(monkeypatch, client)

    output_png = tmp_path / "portrait-rook.png"
    generate_image(prompt_path, output_png)

    assert output_png.read_bytes() == b"FAKEPNGBYTES"
    assert client.models.generate_content.call_args.kwargs["contents"] == "chest-up portrait, neon-lit alley"


def test_generate_image_raises_clearly_on_a_missing_prompt_file(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")

    with pytest.raises(RuntimeError, match="couldn't read prompt file"):
        generate_image(tmp_path / "does-not-exist.txt", tmp_path / "out.png")


def test_main_exits_nonzero_with_a_clear_stderr_message_on_missing_key(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    # Isolate from whatever real skills/*/​.env might exist on the machine.
    monkeypatch.setattr(generate_image_module, "DOTENV_PATH", tmp_path / "no-such-dir" / ".env")
    prompt_path = tmp_path / "npc-fixer.txt"
    prompt_path.write_text("a grizzled fixer, neon noir", encoding="utf-8")
    output_png = tmp_path / "npc-fixer.png"
    monkeypatch.setattr(sys, "argv", ["generate_image.py", str(prompt_path), str(output_png)])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code != 0
    assert "GEMINI_API_KEY" in capsys.readouterr().err
    assert not output_png.exists()


def test_load_dotenv_sets_environment_variables_from_a_file(tmp_path, monkeypatch):
    monkeypatch.delenv("MADE_UP_TEST_KEY", raising=False)
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "# a comment\n\nMADE_UP_TEST_KEY=abc123\nQUOTED_KEY=\"has spaces\"\n",
        encoding="utf-8",
    )

    _load_dotenv(dotenv_path)

    assert os.environ["MADE_UP_TEST_KEY"] == "abc123"
    assert os.environ["QUOTED_KEY"] == "has spaces"


def test_load_dotenv_never_overrides_an_already_set_real_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("MADE_UP_TEST_KEY", "real-value")
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("MADE_UP_TEST_KEY=from-dotenv\n", encoding="utf-8")

    _load_dotenv(dotenv_path)

    assert os.environ["MADE_UP_TEST_KEY"] == "real-value"


def test_load_dotenv_is_a_silent_noop_when_the_file_is_missing(tmp_path):
    _load_dotenv(tmp_path / "does-not-exist" / ".env")  # must not raise


def test_generate_image_bytes_picks_up_the_key_from_a_dotenv_file(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("GEMINI_API_KEY=from-dotenv-file\n", encoding="utf-8")
    monkeypatch.setattr(generate_image_module, "DOTENV_PATH", dotenv_path)
    client = _client_returning(b"BYTESFROMDOTENVRUN")
    _install_fake_genai(monkeypatch, client)

    result = generate_image_bytes("a prompt")

    assert result == b"BYTESFROMDOTENVRUN"
    assert os.environ["GEMINI_API_KEY"] == "from-dotenv-file"


def test_dotenv_path_defaults_to_a_dotenv_file_in_the_current_working_directory():
    assert generate_image_module.DOTENV_PATH == Path.cwd() / ".env"


def test_help_works_without_google_genai_installed(monkeypatch):
    # Guards the lazy-import design: argument parsing must not require
    # google.genai to be importable — --help has to work pre-`pip install`.
    monkeypatch.setattr(sys, "argv", ["generate_image.py", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
