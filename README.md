# Compiler Project

## Development

### Prerequisites
- Python 3.13+ with [uv](https://github.com/astral-sh/uv)
- Node.js + pnpm

### Setup

```bash
# Python deps
uv sync

# Node deps
cd interface && pnpm install
```

### Running in dev mode

Open two terminals from the project root:

**Terminal 1 — Flask API (port 5000)**
```bash
uv run python api.py
```

**Terminal 2 — React UI (port 5173)**
```bash
cd interface && pnpm dev
```

Then open http://localhost:5173 in your browser.

---

## TODO

### Interface / User Experience
- [ ] Create a graphical interface or web interface
- [ ] Add an upload file feature
- [ ] Add a button to launch analysis
- [ ] Display:
      -tokens
      -AST
      -semantic results
      -detected errors
- [ ] Highlight errors with:
      -line
      -column
- [ ] Add a section for symbol table visualization
- [ ] Add syntax highlighting in the editor if possible
### Testing
- [ ] Add lexer/parser/semantic analyzer unit tests
- [ ] Prepare valid test programs
- [ ] Prepare invalid test programs
- [ ] Add edge case tests:
      -empty input
      -invalid token
      -undeclared variable
### Documentation
- [ ] Document language grammar clearly
- [ ] Explain compiler architecture
- [ ] Add execution instructions
- [ ] Add project structure explanation
- [ ] Add examples of valid and invalid programs
- [ ] Add screenshots of interface once completed
## Optional Extensions

The following features are not required but may be added :

- Lexer: more operators (<, <=, >, >=, ==, !=,&&, ||, !), comments, better error handling
- Parser: conditionals, loops, logical expressions, improved errors
- Semantic: additional checks for operators and conditions


