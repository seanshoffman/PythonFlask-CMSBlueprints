import pytest

from pathlib import Path

from redbaron import RedBaron

from tests.utils import template_data, template_functions

main_module = Path.cwd() / 'cms' / '__init__.py'
main_module_exists = Path.exists(main_module) and Path.is_file(main_module)

admin = Path.cwd() / 'cms' / 'admin'
admin_exists = Path.exists(admin) and Path.is_dir(admin)

module = admin / '__init__.py'
module_exists = Path.exists(module) and Path.is_file(module)

models = admin / 'models.py'
models_exists = Path.exists(models) and Path.is_file(models)

def models_code():
    with open(models.resolve(), 'r') as models_source_code:
        return RedBaron(models_source_code.read())

def module_code():
    with open(module.resolve(), 'r') as module_source_code:
        return RedBaron(module_source_code.read())

def main_module_code():
    with open(main_module.resolve(), 'r') as main_module_source_code:
        return RedBaron(main_module_source_code.read())

@pytest.mark.test_admin_blueprint_folder_structure_module1
def test_admin_blueprint_folder_structure_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert module_exists, \
        'Have you added the `__init__.py` file to the `admin` blueprint folder?'
    assert models_exists, \
        'Have you added the `models.py` file to the `admin` blueprint folder?'

@pytest.mark.test_admin_blueprint_models_file_imports_module1
def test_admin_blueprint_models_file_imports_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert models_exists, \
        'Have you added the `models.py` file to the `admin` blueprint folder?'

    import_sql = models_code().find('name', lambda node: \
        node.value == 'flask_sqlalchemy' and \
        node.parent.type == 'from_import' and \
        node.parent.targets[0].value == 'SQLAlchemy') is not None
    assert import_sql, \
        'Are you importing `SQLAlchemy` from `flask_sqlalchemy` at the top of `models.py`?'

    import_datetime = models_code().find('name', lambda node: \
        node.value == 'datetime' and \
        node.parent.type == 'from_import' and \
        node.parent.targets[0].value == 'datetime') is not None
    assert import_datetime, \
        'Are you importing `datetime` from `datetime`?'

    db_assignment = models_code().find('atomtrailers', lambda node: \
        node.value[0].value == 'SQLAlchemy' and \
        node.value[1].type == 'call' and \
        node.parent.type == 'assignment' and \
        node.parent.target.value == 'db')
    db_assignment_exists = db_assignment is not None
    assert db_assignment_exists, \
        'Are you creating an new `SQLAlchemy` instance named `db`?'
    no_arguments = len(db_assignment.find_all('call_argument')) == 0
    assert no_arguments, \
        'Are you passing arguments to the `SQLAlchemy` constructor? If so you can remove them.'

@pytest.mark.test_admin_blueprint_move_model_classes_module1
def test_admin_blueprint_move_model_classes_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert models_exists, \
        'Have you added the `models.py` file to the `admin` blueprint folder?'
    assert main_module_exists, \
        'Have do you have an `__init__.py` file in the `cms` application folder?'

    model_classes = list(models_code().find_all('class').map(lambda node: node.name))
    class_count = len(model_classes) == 4
    type_class = 'Type' in model_classes
    content_class = 'Content' in model_classes
    setting_class = 'Setting' in model_classes
    user_class = 'User' in model_classes
    assert class_count, \
        'Have you moved the four models from `cms/__init__.py` to `cms/admin/models.py`'
    assert type_class, \
        'Have you moved the `Type` model from `cms/__init__.py` to `cms/admin/models.py`'
    assert content_class, \
        'Have you moved the `Content` model from `cms/__init__.py` to `cms/admin/models.py`'
    assert setting_class, \
        'Have you moved the `Setting` model from `cms/__init__.py` to `cms/admin/models.py`'
    assert user_class, \
        'Have you moved the `User` model from `cms/__init__.py` to `cms/admin/models.py`'

    main_module_classes = list(main_module_code().find_all('class').map(lambda node: node.name))
    main_module_class_count = len(main_module_classes) == 0
    assert main_module_class_count, \
        'Have you removed the four models from `cms/__init__.py`?'

    main_module_import = main_module_code().find('from_import', lambda node: \
        node.find('name', value='models'))
    main_module_import_exists =  main_module_import is not None
    assert main_module_import_exists, \
        'Are you importing the correct methods and classes from `cms.admin.models` in `cms/__init__.py`?'
    model_path = list(main_module_import.find_all('name').map(lambda node: node.value))
    import_path = main_module_import is not None and ':'.join(model_path) == 'cms:admin:models'

    assert import_path, \
        'Are you importing the correct methods and classes from `cms.admin.models`?'
    name_as_name_content = main_module_import.find('name_as_name', value='Content') is not None
    assert name_as_name_content, \
        'Are you importing the `Content` model class from `cms.admin.models` in `cms/__init__.py`?'

    name_as_name_type = main_module_import.find('name_as_name', value='Type') is not None
    assert name_as_name_type, \
        'Are you importing the `Type` model class from `cms.admin.models` in `cms/__init__.py`?'

    name_as_name_setting =  main_module_import.find('name_as_name', value='Setting') is not None
    assert name_as_name_setting, \
        'Are you importing the `Setting` model class from `cms.admin.models` in `cms/__init__.py`?'

    name_as_name_user =  main_module_import.find('name_as_name', value='User') is not None
    assert name_as_name_user, \
        'Are you importing the `User` model class from `cms.admin.models` in `cms/__init__.py`?'

@pytest.mark.test_cms_module_import_db_module1
def test_cms_module_import_db_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert main_module_exists, \
        'Have do you have an `__init__.py` file in the `cms` application folder?'

    db_assignment = main_module_code().find('atomtrailers', lambda node: \
        node.value[0].value == 'SQLAlchemy' and \
        node.value[1].type == 'call' and \
        node.parent.type == 'assignment' and \
        node.parent.target.value == 'db') is None
    assert db_assignment, \
        'Have you removed the `SQLAlchemy` instance named `db` from `cms/__init__.py`?'

    main_module_import = main_module_code().find('from_import', lambda node: \
        node.find('name', value='models'))
    main_module_import_exists =  main_module_import is not None
    assert main_module_import_exists, \
        'Are you importing the correct methods and classes from `cms.admin.models`?'
    model_path = list(main_module_import.find_all('name').map(lambda node: node.value))
    main_import_path = main_module_import is not None and ':'.join(model_path) == 'cms:admin:models'
    assert main_import_path, \
        'Are you importing the correct methods and classes from `cms.admin.models` in `cms/__init__.py`?'

    name_as_name_db = main_module_import.find('name_as_name', value='db') is not None
    assert name_as_name_db, \
        'Are you importing the `db` SQLAlchemy instance from `cms.admin.models` in `cms/__init__.py`?'

    init_app_call = main_module_code().find('name', lambda node: \
        node.value == 'init_app' and \
        node.parent.value[0].value == 'db' and \
        node.parent.value[2].type == 'call')
    init_app_call_exists = init_app_call is not None
    assert init_app_call_exists, \
        'Are you calling the `init_app` method on `db`?'
    init_app_arg = init_app_call.parent.find('call_argument').value.value == 'app'
    assert init_app_arg, \
        'Are you passing `app` to the `init_app` method?'

@pytest.mark.test_cms_module_remove_imports_module1
def test_cms_module_remove_imports_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert main_module_exists, \
        'Have do you have an `__init__.py` file in the `cms` application folder?'

    main_import_sql = main_module_code().find('name', lambda node: \
        node.value == 'flask_sqlalchemy' and \
        node.parent.type == 'from_import' and \
        node.parent.targets[0].value == 'SQLAlchemy') is None
    assert main_import_sql, \
        'Have you removed the import for `flask_sqlalchemy` from `cms/__init__.py`?'

    main_import_datetime = main_module_code().find('name', lambda node: \
        node.value == 'datetime' and \
        node.parent.type == 'from_import' and \
        node.parent.targets[0].value == 'datetime') is None
    assert main_import_datetime, \
        'Have you removed the import for `datetime` from `cms/__init__.py`?'

@pytest.mark.test_admin_blueprint_create_blueprint_module1
def test_admin_blueprint_create_blueprint_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert module_exists, \
        'Have you added the `__init__.py` file to the `admin` blueprint folder?'

    blueprint_from = module_code().find('from_import', lambda node: \
        node.value[0].value == 'flask' and \
        'Blueprint' in list(node.targets.map(lambda node: str(node)))) is not None
    assert blueprint_from, \
        'Are you importing `Blueprint` from `flask` in `cms/admin/__init__.py`?'

    admin_bp = module_code().find('assign', lambda node: node.target.value == 'admin_bp')
    admin_bp_exists = admin_bp is not None
    assert admin_bp_exists, \
        'Are you setting the `admin_bp` variable correctly?'

    blueprint_instance = admin_bp.find('atomtrailers', lambda node: node.value[0].value == 'Blueprint')
    blueprint_instance_exists = blueprint_instance is not None
    assert blueprint_instance_exists, \
        'Are you setting the `admin_bp` variable to an instance of `Content`?'

    blueprint_args = list(blueprint_instance.find_all('call_argument').map(lambda node: str(node.target) + ':' + str(node.value)))
    admin_first = "None:'admin'" in blueprint_args
    assert admin_first, \
        "Are you passing the Blueprint instance the correct arguments? The first argument should be: `'admin'`."

    name_second = "None:__name__" in blueprint_args
    assert name_second, \
        'Are you passing the Blueprint instance the correct arguments? The second argument should be: `__name__`.'

    url_prefix = "url_prefix:'/admin'" in blueprint_args
    assert url_prefix, \
        "Are you passing the Blueprint instance the correct arguments? There should be a url_prefix keyword argument set to `'/admin'`."

@pytest.mark.test_admin_blueprint_imports_module1
def test_admin_blueprint_imports_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert module_exists, \
        'Have you added the `__init__.py` file to the `admin` blueprint folder?'

    flask_import = module_code().find('from_import', lambda node: node.value[0].value == 'flask')
    flask_import_exits = flask_import  is not None
    assert flask_import_exits, \
        'Are you importing the correct methods and classes from `flask`?'
    from_flask_imports = list(flask_import.targets.find_all('name_as_name').map(lambda node: node.value ))
    render_template_import = 'render_template' in from_flask_imports
    assert render_template_import, \
        'Are you importing `render_template` from `flask` in `cms/admin/__init__.py`?'
    abort_import = 'abort' in from_flask_imports
    assert abort_import, \
        'Are you importing `abort` from `flask` in `cms/admin/__init__.py`?'

    module_import = module_code().find('from_import', lambda node: node.find('name', value='models'))
    module_import_exists = module_import is not None
    assert module_import_exists, \
        'Are you importing the correct methods and classes from `cms.admin.models` in `cms/admin/__init__.py`?'
    model_path = list(module_import.find_all('name').map(lambda node: node.value))
    import_path = module_import is not None and ':'.join(model_path) == 'cms:admin:models'
    assert import_path, \
        'Are you importing the correct methods and classes from `cms.admin.models` in `cms/admin/__init__.py`?'

    name_as_name_content = module_import.find('name_as_name', value='Content') is not None
    assert name_as_name_content, \
        'Are you importing the `Content` model class from `cms.admin.models` in `cms/admin/__init__.py`?'

    name_as_name_type = module_import.find('name_as_name', value='Type') is not None
    assert name_as_name_type, \
        'Are you importing the `Type` model class from `cms.admin.models` in `cms/admin/__init__.py`?'

    name_as_name_setting =  module_import.find('name_as_name', value='Setting') is not None
    assert name_as_name_setting, \
        'Are you importing the `Setting` model class from `cms.admin.models` in `cms/admin/__init__.py`?'

    name_as_name_user =  module_import.find('name_as_name', value='User') is not None
    assert name_as_name_user, \
        'Are you importing the `User` model class from `cms.admin.models` in `cms/admin/__init__.py`?'

@pytest.mark.test_admin_blueprint_move_routes_module1
def test_admin_blueprint_move_routes_module1():

    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert module_exists, \
        'Have you added the `__init__.py` file to the `admin` blueprint folder?'
    assert main_module_exists, \
        'Have do you have an `__init__.py` file in the `cms` application folder?'

    requested_type = module_code().find('def', name='requested_type') is not None
    assert requested_type, \
        'Did you move the `requested_type` function from `cms/__init__.py` to `cms/admin/__init__.py`?'

    content_route = module_code().find('def', name='content')
    content_route_exists = content_route is not None
    assert content_route_exists, \
        'Did you move the `user` function from `cms/__init__.py` to `cms/admin/__init__.py`?'
    content_decorators = content_route.find_all('dotted_name')
    content_decorator_count = len(content_decorators) == 2
    assert content_decorator_count, \
        'Did you move the `settings` route decorators to `cms/admin/__init__.py`?'
    content_blueprint_route1 = str(content_decorators[0]) == 'admin_bp.route'
    content_blueprint_route2 = str(content_decorators[1]) == 'admin_bp.route'
    assert content_blueprint_route1, \
        'Have you changed the `@app` decorator to `@admin_ap` on the `content` function?'
    assert content_blueprint_route2, \
        'Have you changed the `@app` decorator to `@admin_ap` on the `content` function?'

    create_route = module_code().find('def', name='create')
    create_route_exists = content_route is not None
    assert create_route_exists, \
        'Did you move the `user` function from `__init__.py` to `cms/admin/__init__.py`?'
    create_decorators = create_route.find_all('dotted_name')
    create_decorator_count = len(create_decorators) == 1
    assert create_decorator_count, \
        'Did you move the `settings` route decorators to `cms/admin/__init__.py`?'
    create_blueprint_routes = str(create_decorators[0]) == 'admin_bp.route'
    assert create_blueprint_routes, \
        'Have you changed the `@app` decorator to `@admin_ap` on the `create` function?'

    users_route = module_code().find('def', name='users')
    users_route_exists = content_route is not None
    assert users_route_exists, \
        'Did you move the `user` function from `__init__.py` to `cms/admin/__init__.py`?'
    users_decorators = users_route.find_all('dotted_name')
    users_decorator_count = len(users_decorators) == 1
    assert users_decorator_count, \
        'Did you move the `settings` route decorators to `cms/admin/__init__.py`?'
    users_blueprint_routes = str(users_decorators[0]) == 'admin_bp.route'
    assert users_blueprint_routes, \
        'Have you changed the `@app` decorator to `@admin_ap` on the `users` function?'

    settings_route = module_code().find('def', name='settings')
    settings_route_exists = content_route is not None
    assert settings_route_exists, \
        'Did you move the `settings` function from `__init__.py` to `cms/admin/__init__.py`?'
    settings_decorators = settings_route.find_all('dotted_name')
    settings_decorator_count = len(settings_decorators) == 1
    assert settings_decorator_count, \
        'Did you move the `settings` route decorators to `cms/admin/__init__.py`?'
    settings_blueprint_routes = str(settings_decorators[0]) == 'admin_bp.route'
    assert settings_blueprint_routes, \
        'Have you changed the `@app` decorator to `@admin_ap` on the `settings` function?'

    def_content = main_module_code().find('def', name='content') is None
    assert def_content, \
        'Did you remove the `content` function from `__init__.py`?'

    def_create = main_module_code().find('def', name='create') is None
    assert def_create, \
        'Did you remove the `create` function from `__init__.py`?'

    def_users = main_module_code().find('def', name='users') is None
    assert def_users, \
        'Did you remove the `users` function from `__init__.py`?'

    def_settings = main_module_code().find('def', name='settings') is None
    assert def_settings, \
        'Did you remove the `settings` function from `__init__.py`?'

@pytest.mark.test_cms_module_register_blueprint_module1
def test_cms_module_register_blueprint_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert main_module_exists, \
        'Have do you have an `__init__.py` file in the `cms` application folder?'

    bp_import = main_module_code().find('from_import', lambda node: \
        node.find('name_as_name', value='admin_bp'))
    bp_import_exists = bp_import is not None
    assert bp_import_exists, \
        'Are you importing `admin_bp` from `cms.admin` in `cms/__init__.py`?'

    model_path = list(bp_import.find_all('name').map(lambda node: node.value))
    admin_bp_import = bp_import is not None and ':'.join(model_path) == 'cms:admin'
    assert admin_bp_import, \
        'Are you importing the `admin_bp` Blueprint from `cms.admin`?'

    register_bp_call = main_module_code().find('atomtrailers', lambda node: \
        node.value[0].value == 'app' and \
        node.value[1].value == 'register_blueprint' and \
        node.value[2].type == 'call')
    register_bp_call_exists = register_bp_call is not None
    assert register_bp_call_exists, \
        'Are you calling `register_blueprint` on `app`?'

    register_blueprint_args = list(register_bp_call.find_all('call_argument').map(lambda node: \
        str(node.target) + ':' + str(node.value)))
    register_count = len(register_blueprint_args) == 1
    assert register_count, \
        'Are you only passing one argument to `register_blueprint`?'
    admin_bp_registered = "None:admin_bp" in register_blueprint_args
    assert admin_bp_registered, \
        'Are you passing the Blueprint instance to should be `register_blueprint`?'

@pytest.mark.test_admin_blueprint_template_folder_module1
def test_admin_blueprint_template_folder_module1():
    assert admin_exists, \
        'Have you created the `admin` blueprint folder?'
    assert module_exists, \
        'Have you added the `__init__.py` file to the `admin` blueprint folder?'

    admin_bp = module_code().find('assign', lambda node: \
        node.target.value == 'admin_bp')
    admin_bp_exists = admin_bp is not None
    assert admin_bp_exists, \
        'Are you setting the `admin_bp` variable correctly?'
    blueprint_instance = admin_bp.find('atomtrailers', lambda node: \
        node.value[0].value == 'Blueprint')
    blueprint_instance_exists = blueprint_instance is not None
    assert blueprint_instance_exists, \
        'Are you setting the `admin_bp` variable to an instance of `Content`?'
    blueprint_args = list(blueprint_instance.find_all('call_argument').map(lambda node: \
        str(node.target) + ':' + str(node.value)))
    blueprint_template_folder = "template_folder:'templates'" in blueprint_args
    assert blueprint_template_folder, \
        "Are you passing the Blueprint instance the correct arguments? There should be a `template_folder` keyword argument set to `'/admin'`."

    admin_templates = admin / 'templates'
    admin_templates_exists = Path.exists(admin_templates) and Path.is_dir(admin_templates)
    assert admin_templates_exists, \
        'Have you created a `templates` folder in the `admin` blueprint folder?'

    move = admin_templates / 'admin'
    move_exists = Path.exists(move) and Path.is_dir(move)
    assert move_exists, \
        'Have you move the `admin` folder from the root `templates` folder to the `admin` blueprint `templates` folder?'

    content        = move / 'content.html'
    content_exists = Path.exists(content) and Path.is_file(content)
    assert content_exists, \
        'Is the `content.html` template file in the `cms/admin/templates/admin` folder?'

    content_form        = move / 'content_form.html'
    content_form_exists = Path.exists(content_form) and Path.is_file(content_form)
    assert content_form_exists, \
        'Is the `content_form.html` template file in the `cms/admin/templates/admin` folder?'

    layout        = move / 'layout.html'
    layout_exists = Path.exists(layout) and Path.is_file(layout)
    assert layout_exists, \
        'Is the `layout.html` template file in the `cms/admin/templates/admin` folder?'

    settings        = move / 'settings.html'
    settings_exists = Path.exists(settings) and Path.is_file(settings)
    assert settings_exists, \
        'Is the `settings.html` template file in the `cms/admin/templates/admin` folder?'

    users        = move / 'users.html'
    users_exists = Path.exists(users) and Path.is_file(users)
    assert users_exists, \
        'Is the `users.html` template file in the `cms/admin/templates/admin` folder?'

    links = template_functions('layout', 'url_for')
    page_link_exists = 'admin.content:type:page' in links
    assert page_link_exists, \
        'Have you updated the `url_for` for `Pages` in `admin/templates/admin/layout.html`?'

    post_link_exists     = 'admin.content:type:post' in links
    assert post_link_exists, \
        'Have you updated the `url_for` for `Posts` in `admin/templates/admin/layout.html`?'

    partial_link_exists  = 'admin.content:type:partial' in links
    assert partial_link_exists, \
        'Have you updated the `url_for` for `Partial` in `admin/templates/admin/layout.html`?'

    template_link_exists = 'admin.content:type:template' in links
    assert template_link_exists, \
        'Have you updated the `url_for` for `Templates` in `admin/templates/admin/layout.html`?'

    users_link_exists    = 'admin.users:' in links
    assert users_link_exists, \
        'Have you updated the `url_for` for `Users` in `admin/templates/admin/layout.html`?'

    settings_link_exists = 'admin.settings:' in links
    assert settings_link_exists, \
        'Have you updated the `url_for` for `Settings` in `admin/templates/admin/layout.html`?'
