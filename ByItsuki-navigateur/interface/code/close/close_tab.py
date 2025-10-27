def close_tab_window(tab_widget, index, tab):
    if hasattr(tab, "history_root"):
        file_delete = tab.history_root / "history.json"
        if file_delete.exists():
            file_delete.unlink()
    tab_widget.removeTab(index)
    tab.deleteLater()