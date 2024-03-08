from webview import *
import model
import os

if __name__ == "__main__":
    _model_ = model.MainModel()
    main_view = create_window("Uni", url="./main_view.html", js_api=_model_)
    start(debug=True)
