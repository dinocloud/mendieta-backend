from distutils.core import setup

setup(
    name="mendieta",
    version='1.0',
    py_modules=["mendieta", "database.database", "model.provisioner", "model.users",
                "schemas.schemas", "utils.utils", "utils.settings", "views.authentication", "views.provisioners_view",
                "views.users_view"],
    data_files=[('init_data.json', ['database/init_data.json']),('requirements.txt', ['requirements.txt'])],
    #metadata
    author="Franco",
    author_email="Franco.salonia@dinocloudconsulting.com",
    description="Backend for Mendieta project",
    license="Public content",
    keywords="backend mendieta dinocloud"
)