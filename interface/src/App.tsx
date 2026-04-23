import { useState } from 'react'
import './App.css'

const EXAMPLES = [
  {
    label: 'Basic assignment',
    code: 'int x;\nx = 5 + 2;\n',
  },
  {
    label: 'String variable',
    code: 'string name;\nname = "Alice";\n',
  },
  {
    label: 'Type mismatch error',
    code: 'int x;\nx = "hello";\n',
  },
  {
    label: 'Undeclared variable',
    code: 'x = 5;\n',
  },
  {
    label: 'String concat',
    code: 'string greeting;\ngreeting = "hello" + " world";\n',
  },
]

type Token = { type: string; value: string | number; line: number; col: number }
type ASTNode = Record<string, unknown>
type SemanticResult = { ok: boolean; symbol_table: Record<string, string> }

type CompileResult = {
  tokens: Token[] | null
  ast: ASTNode | null
  semantic: SemanticResult | null
  error: string | null
  stage: 'lexer' | 'parser' | 'semantic' | 'ok' | null
}

function tokenBadge(type: string) {
  const map: Record<string, string> = {
    NUM: 'badge-num',
    ID: 'badge-id',
    STRING_LITERAL: 'badge-str',
    INT_TYPE: 'badge-kw',
    STRING_TYPE: 'badge-kw',
    KW_IF: 'badge-kw',
    KW_THEN: 'badge-kw',
    KW_ELSE: 'badge-kw',
    ASSIGN: 'badge-op',
    PLUS: 'badge-op',
    MINUS: 'badge-op',
    MUL: 'badge-op',
    DIV: 'badge-op',
    GT: 'badge-op',
    SEMI: 'badge-punct',
    LPAREN: 'badge-punct',
    RPAREN: 'badge-punct',
    LBRACE: 'badge-punct',
    RBRACE: 'badge-punct',
  }
  return map[type] ?? 'badge-default'
}

function ASTTree({ node, depth = 0 }: { node: ASTNode; depth?: number }) {
  if (!node || typeof node !== 'object') return <span className="ast-leaf">{String(node)}</span>

  const type = node.type as string
  const indent = depth * 16

  const renderChildren = () => {
    const skip = new Set(['type', 'line', 'column'])
    return Object.entries(node)
      .filter(([k]) => !skip.has(k))
      .map(([k, v]) => (
        <div key={k} style={{ marginLeft: indent + 12 }}>
          <span className="ast-key">{k}: </span>
          {Array.isArray(v)
            ? v.map((item, i) => (
                <div key={i} style={{ marginLeft: 8 }}>
                  <ASTTree node={item as ASTNode} depth={depth + 1} />
                </div>
              ))
            : typeof v === 'object' && v !== null
            ? <ASTTree node={v as ASTNode} depth={depth + 1} />
            : <span className="ast-leaf">{JSON.stringify(v)}</span>}
        </div>
      ))
  }

  return (
    <div className="ast-node" style={{ marginLeft: indent }}>
      <span className="ast-type">{type}</span>
      {node.name !== undefined && <span className="ast-name"> {String(node.name)}</span>}
      {node.value !== undefined && <span className="ast-value"> = {JSON.stringify(node.value)}</span>}
      {node.var_type !== undefined && <span className="ast-vartype"> ({String(node.var_type)})</span>}
      {node.op !== undefined && <span className="ast-op"> '{String(node.op)}'</span>}
      <div>{renderChildren()}</div>
    </div>
  )
}

export default function App() {
  const [source, setSource] = useState(EXAMPLES[0].code)
  const [result, setResult] = useState<CompileResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState<'tokens' | 'ast' | 'semantic'>('tokens')

  async function run() {
    setLoading(true)
    try {
      const res = await fetch('/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source }),
      })
      const data: CompileResult = await res.json()
      setResult(data)
      if (data.tokens && tab === 'tokens') setTab('tokens')
    } finally {
      setLoading(false)
    }
  }

  const stageColor = (s: string | null) => {
    if (s === 'ok') return 'status-ok'
    if (s) return 'status-error'
    return ''
  }

  return (
    <div className="layout">
      <header className="header">
        <h1>Compiler Playground</h1>
        <p>Lexer · Parser · Semantic Analyzer</p>
      </header>

      <div className="main">
        <div className="panel left-panel">
          <div className="panel-header">
            <span>Source Code</span>
            <select
              onChange={(e) => {
                const ex = EXAMPLES[+e.target.value]
                if (ex) setSource(ex.code)
              }}
              defaultValue=""
            >
              <option value="" disabled>Load example…</option>
              {EXAMPLES.map((ex, i) => (
                <option key={i} value={i}>{ex.label}</option>
              ))}
            </select>
          </div>
          <textarea
            className="editor"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            spellCheck={false}
          />
          <button className="run-btn" onClick={run} disabled={loading}>
            {loading ? 'Running…' : '▶ Run'}
          </button>
        </div>

        <div className="panel right-panel">
          {result && (
            <>
              <div className={`status-bar ${stageColor(result.stage)}`}>
                {result.stage === 'ok'
                  ? '✓ Compilation successful'
                  : `✗ Error in ${result.stage} stage: ${result.error}`}
              </div>

              <div className="tabs">
                {(['tokens', 'ast', 'semantic'] as const).map((t) => (
                  <button
                    key={t}
                    className={`tab ${tab === t ? 'active' : ''}`}
                    onClick={() => setTab(t)}
                  >
                    {t.charAt(0).toUpperCase() + t.slice(1)}
                  </button>
                ))}
              </div>

              <div className="tab-content">
                {tab === 'tokens' && (
                  result.tokens ? (
                    <div className="tokens-grid">
                      <div className="tokens-head">
                        <span>Type</span><span>Value</span><span>Line</span><span>Col</span>
                      </div>
                      {result.tokens.map((tok, i) => (
                        <div key={i} className="token-row">
                          <span className={`badge ${tokenBadge(tok.type)}`}>{tok.type}</span>
                          <span className="tok-val">{String(tok.value)}</span>
                          <span className="tok-pos">{tok.line}</span>
                          <span className="tok-pos">{tok.col}</span>
                        </div>
                      ))}
                    </div>
                  ) : <div className="empty">No tokens (lexer failed)</div>
                )}

                {tab === 'ast' && (
                  result.ast ? (
                    <div className="ast-container">
                      <ASTTree node={result.ast} />
                    </div>
                  ) : <div className="empty">No AST (parser failed or not reached)</div>
                )}

                {tab === 'semantic' && (
                  result.semantic ? (
                    <div className="semantic-container">
                      <div className="sem-ok">✓ Semantic analysis passed</div>
                      <h3>Symbol Table</h3>
                      <table className="sym-table">
                        <thead><tr><th>Variable</th><th>Type</th></tr></thead>
                        <tbody>
                          {Object.entries(result.semantic.symbol_table).map(([name, type]) => (
                            <tr key={name}><td>{name}</td><td><span className="badge badge-kw">{type}</span></td></tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : <div className="empty">No semantic result (analysis failed or not reached)</div>
                )}
              </div>
            </>
          )}

          {!result && (
            <div className="placeholder">
              Write code on the left and click <strong>▶ Run</strong> to compile.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
