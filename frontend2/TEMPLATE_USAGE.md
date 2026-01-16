# React Node Template - Usage Guide

## Quick Start

### 1. Install Dependencies
```bash
cd web_apps/react_node_template
npm install
```

### 2. Start Development Servers
```bash
# From project root - starts both backend and frontend
python cli.py nodeapps start react_node_template
```

The browser will automatically open to http://localhost:5176

### 3. Customize

1. **Replace Demo Content**: Edit `src/App.jsx` with your own UI
2. **Add API Endpoints**: Add routes in `server.js`
3. **Update Styles**: Modify `src/App.css` and `src/index.css`
4. **Enable Socket.io**: Uncomment Socket.io sections if needed (see guide)

## Template Features

✅ **React 18** - Modern React with hooks  
✅ **Express Backend** - RESTful API server  
✅ **Vite.js** - Fast dev server and optimized builds  
✅ **Socket.io** - Optional real-time features (disabled by default)  
✅ **Color Palette** - Centralized colors from `config/color_palette.json`  
✅ **No Hardcoded Colors** - Everything uses CSS variables  
✅ **Production Ready** - Optimized build configuration  

## File Structure

```
react_node_template/
├── server.js              # Express + Socket.io backend
├── vite.config.js         # Vite config with color palette plugin
├── package.json           # Dependencies
├── index.html            # HTML entry point
├── README.md             # Quick start guide
└── src/
    ├── main.jsx          # React entry point
    ├── App.jsx           # Main component (customize this!)
    ├── App.css           # Component styles
    ├── index.css         # Global styles
    ├── hooks/
    │   └── useColorPalette.js  # Color palette hook
    └── utils/
        └── colorPalette.js     # Color utilities
```

## Ports

- **Backend**: 3002
- **Frontend**: 5176

## Color Palette Integration

All colors come from `config/color_palette.json`. Use CSS variables:

```css
.my-component {
  background-color: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-primary);
}
```

Update `config/color_palette.json` and rebuild to change colors across all apps.

## Enabling Socket.io

1. Uncomment Socket.io sections in `server.js`
2. Uncomment proxy in `vite.config.js`
3. Uncomment connection code in `src/App.jsx`

See `notes/REACT_NODE_TEMPLATE_GUIDE.md` for detailed instructions.

## Documentation

- **Quick Start**: `README.md` (this directory)
- **Complete Guide**: `notes/REACT_NODE_TEMPLATE_GUIDE.md`
- **CLI Usage**: `notes/CLI_GUIDE.md`

## Creating New Instances

To create a new app from this template:

1. Copy the `react_node_template` directory
2. Rename to your app name
3. Update `package.json` name and description
4. Customize the code
5. Add to `run_nodeApps.py` DEFAULT_PORTS if needed

Example:
```bash
cp -r web_apps/react_node_template web_apps/my_new_app
cd web_apps/my_new_app
# Edit package.json, customize code, etc.
```

## Support

For detailed documentation, see:
- `notes/REACT_NODE_TEMPLATE_GUIDE.md` - Comprehensive guide
- `notes/CLI_GUIDE.md` - CLI usage
- Existing apps for examples (`kafka_dashboard_node`, `socketIO_demo`)

