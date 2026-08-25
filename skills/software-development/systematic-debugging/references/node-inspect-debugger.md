# Node.js Debugging Reference

Formerly a standalone skill. Content absorbed into `systematic-debugging`.

## Launch Node with inspect

```bash
# Start with inspect
node --inspect=9229 my-script.js

# Break on first line
node --inspect-brk=9229 my-script.js
```

## Chrome DevTools

1. Open `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. Connect to `localhost:9229`

## VS Code Configuration

```json
{
  "name": "Node: Attach",
  "type": "node",
  "request": "attach",
  "port": 9229,
  "restart": true
}
```
