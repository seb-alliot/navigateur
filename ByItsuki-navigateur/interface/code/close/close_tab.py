def close_tab_window(tab_widget, index, tab):
    if hasattr(tab, "history_file"):
        file_delete = tab.history_file
        if file_delete.exists():
            file_delete.unlink()
    tab_widget.removeTab(index)
    tab.deleteLater()