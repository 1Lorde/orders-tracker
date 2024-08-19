import setuptools
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        import os
        from pyshortcuts import make_shortcut
        from pathlib import Path

        make_shortcut(os.path.join(str(Path.home()), 'AppData', 'Local', 'Programs', 'Python', 'Python38', 'Lib',
                                   'site-packages', 'orders_tracker', 'bin', 'start.vbs'),
                      name='Start Orders_Tracker',
                      description='Запуск програми orders-tracker.exe',
                      icon=os.path.join(str(Path.home()), 'AppData', 'Local', 'Programs', 'Python', 'Python38', 'Lib',
                                        'site-packages', 'orders_tracker', 'bin', 'icons', 'start.ico'))

        make_shortcut(os.path.join(str(Path.home()), 'AppData', 'Local', 'Programs', 'Python', 'Python38', 'Lib',
                                   'site-packages', 'orders_tracker', 'bin', 'stop.vbs'),
                      name='Stop Orders_Tracker',
                      description='Зупинка програми orders-tracker.exe',
                      icon=os.path.join(str(Path.home()), 'AppData', 'Local', 'Programs', 'Python', 'Python38', 'Lib',
                                        'site-packages', 'orders_tracker', 'bin', 'icons', 'stop.ico'))


setuptools.setup(
    name="orders-tracker",
    version="1.2",
    author="Vlad Savchuk",
    url="https://github.com/1Lorde",
    description="Orders tracking app.",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='office orders accounting',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    cmdclass={
        'install': PostInstallCommand,
    },
    install_requires=['Babel==2.9.0',
                      'click==7.1.2',
                      'dominate==2.6.0',
                      'Flask==1.1.2',
                      'Flask-Babel==2.0.0',
                      'Flask-Bootstrap==3.3.7.1',
                      'Flask-Datepicker==0.14',
                      'Flask-SQLAlchemy==2.4.4',
                      'Flask-Table==0.5.0',
                      'Flask-WTF==0.14.3',
                      'itsdangerous==1.1.0',
                      'Jinja2==2.11.3',
                      'MarkupSafe==1.1.1',
                      'pytz==2021.1',
                      'six==1.15.0',
                      'SQLAlchemy==1.3.23',
                      'SQLAlchemy-Utils==0.36.8',
                      'visitor==0.1.3',
                      'Werkzeug==1.0.1',
                      'WTForms==2.3.3',
                      'pyshortcuts==1.8.0'],
    entry_points={
        'console_scripts': ['orders-tracker=orders_tracker.app:main']
    },
    package_data={'orders_tracker': ['bin/*',
                                     'bin/icons/*',
                                     'static/*',
                                     'static/img/*',
                                     'static/css/*',
                                     'static/ionicons/*',
                                     'static/ionicons/svg/*',
                                     'static/jquery/*',
                                     'static/jquery/images/*',
                                     'templates/errors/*',
                                     'templates/*',
                                     'blueprints/clients/templates/*',
                                     'blueprints/devices/templates/*',
                                     'blueprints/orders/templates/*',
                                     'blueprints/staff/templates/*',
                                     'blueprints/start/templates/*']}
)
