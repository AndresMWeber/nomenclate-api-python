from flask import current_app
from apispec.exceptions import APISpecError
from apispec_webframeworks.flask import FlaskPlugin
from flask.views import MethodView
from apispec import yaml_utils


class FlaskRestfulPlugin(FlaskPlugin):
    @staticmethod
    def _rule_for_view(view, app):
        if app is None:
            app = current_app

        view_funcs = app.view_functions
        endpoint = None
        for ept, view_func in view_funcs.items():
            if view_func.__name__ == view.__name__:
                endpoint = ept
        if not endpoint:
            raise APISpecError(f"Could not find endpoint for view {view}")

        return app.url_map._rules_by_endpoint[endpoint][0]

    def path_helper(self, operations, *, view, app=None, **kwargs):
        """Path helper that allows passing a Flask view function."""
        rule = self._rule_for_view(view, app=app)
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
        if hasattr(view, "view_class") and issubclass(view.view_class, MethodView):
            for method in view.methods:
                if method in rule.methods:
                    method_name = method.lower()
                    method = getattr(view.view_class, method_name)
                    if method.__doc__:
                        docs = yaml_utils.load_yaml_from_docstring(method.__doc__)
                        operations[method_name] = docs[
                            "schema"  # Access custom static root to allow yaml parsing.
                        ]
        return self.flaskpath2openapi(rule.rule)
