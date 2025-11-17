# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-11-17

### Added
- 🎨 Modern dialog system (confirm, info, warning, error dialogs)
- ⌨️ Keyboard shortcut hints on buttons (Ctrl+S, Ctrl+N)
- 🔍 Search functionality with tab highlighting
- 📑 Tab-based note management with hover delete
- 🎯 Auto-select first note on startup
- 🗑️ Dynamic clear/remove button (context-aware)
- ⌨️ Keyboard shortcuts:
  - `Ctrl+S` / `Cmd+S`: Save note
  - `Ctrl+N` / `Cmd+N`: New note
  - `Ctrl+T` / `Cmd+T`: Focus title
  - `Ctrl+F` / `Cmd+F`: Focus search
  - `Escape`: New note mode

### Changed
- 🎨 Migrated from Tkinter to CustomTkinter for modern UI
- 🎨 Improved dialog design with better colors and spacing
- 🎨 Made textbox resizable with window size
- 🧹 Code cleanup: removed unnecessary comments

### Fixed
- 🐛 Fixed tab selection and note loading issues
- 🐛 Improved delete confirmation flow

## [1.0.0] - 2024

### Added
- Modern note-taking interface with CustomTkinter
- JSON-based data storage
- Note validation (max length, empty check)
- Dark theme support
- Configurable settings via config.py
- Utility functions for date formatting

### Features
- Save and clear notes
- Persistent storage
- Note counter display
- Error handling and validation

