# pocsmith

`pocsmith` generates modular Python proof-of-concept templates from alias flags or YAML profiles.

## Install

From GitHub with `pipx`:

```bash
pipx install git+https://github.com/pr0f94/pocsmith.git
```

For local development:

```bash
git clone https://github.com/pr0f94/pocsmith.git
cd pocsmith
python3 -m pip install -e .
```

## Quick Start

```bash
pocsmith --profile web-callback -o exploit.py
pocsmith --session --auth-form -o exploit.py
pocsmith --local --proof -o callback.py
```

Existing output files are not overwritten unless `--force` is supplied.

## Aliases

```text
--session
--multi-session
--flask
--cookie
--local
--proof
--netcat
--auth-form
--auth-json
--register-json
--headers
--token-extractor
--html-parser
--csrf
--regex-extract
--base64
--file-upload
--zip-builder
--websocket
--websocket-async
--bruteforce-loop
```

Aliases automatically include their required dependencies. For example, `--cookie` adds Flask and queue support, `--proof`/`--local` add Flask callback support, and `--csrf` adds session and HTML parser support.

## Profiles

Profiles are packaged with `pocsmith` and use alias names:

```yaml
web-callback:
  - session
  - flask
  - cookie
  - proof
```

Profiles are capability-based rather than lab- or exam-specific.

## Generated Runtime Args

Generated exploits only include runtime arguments needed by the selected modules. Target-aware modules use host-only targets and default to HTTP:

```bash
python3 exploit.py --target 192.168.1.10:8080
python3 exploit.py --target target.local --https
```

Callback modules require explicit callback values:

```bash
python3 exploit.py --callback-ip 192.168.45.123 --flask-port 8000
```

Netcat modules require an explicit port:

```bash
python3 exploit.py --nc-port 4444
```

## Generated Template Dependencies

`pocsmith` itself has no third-party runtime dependencies. Generated templates may need packages based on selected aliases:

```text
requests          --session and dependent modules
flask             --flask, --cookie, --local, --proof
beautifulsoup4    --html-parser, --csrf
websocket-client  --websocket
websockets        --websocket-async
```

Install only what the generated template imports.

## Color

`pocsmith` uses colored help and status output when stdout is an interactive terminal. Use `--no-color` or `NO_COLOR=1` to disable color, or `FORCE_COLOR=1` to force it.

## License

MIT
