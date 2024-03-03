.. image:: https://github.com/morepath/more.pony/workflows/CI/badge.svg?branch=master
   :target: https://github.com/morepath/more.pony/actions?workflow=CI
   :alt: CI Status

.. image:: https://img.shields.io/pypi/v/more.pony.svg
  :target: https://pypi.org/project/more.pony/

.. image:: https://img.shields.io/pypi/pyversions/more.pony.svg
  :target: https://pypi.org/project/more.pony/


more.pony: Pony ORM integration in Morepath
===========================================

This package provides Morepath integration for the Pony_
Object-Relational Mapper library.

This package binds the database session to the request so
you can interact with the database in your App directly
without using ``db_session``.


Quick start
-----------

Install ``more.pony``:

.. code-block:: console

  $ pip install -U more.pony

Extend your App class from PonyApp:

.. code-block:: python

    from more.pony import PonyApp

    class App(PonyApp):
        pass


Create your model:

.. code-block:: python

  from pony.orm import Database, PrimaryKey, Optional

  db = Database()


  class Document(db.Entity):
      _table_ = 'document'

      id = PrimaryKey(int, auto=True)
      title = Optional(str)
      content = Optional(str)

      def update(self, payload={}):
          self.set(**payload)

      def remove(self):
          self.delete()


Setup the database in your start script:

.. code-block:: python

  import morepath

  from .app import App
  from .model import db


  def run():
      db.bind(provider='sqlite', filename='app.db', create_db=True)
      db.generate_mapping(create_tables=True)

      morepath.autoscan()
      morepath.run(App())


Now you can use the model in your path:

.. code-block:: python

  from .app import App
  from .model import Document


  @App.path(model=Document, path='documents/{id}')
  def get_document(request, id=0):
      return Document[id]

And in your view:

.. code-block:: python

  from .app import App
  from .model import Document


  @App.json(model=Document)
  def document_default(self, request):
      return {
          'id': self.id,
          'title': self.title,
          'content': self.content,
          'link': request.link(self)
      }


  @App.json(model=Document, request_method='PUT')
  def document_update(self, request):
      self.update(request.json)


  @App.json(model=Document, request_method='DELETE')
  def document_remove(self, request):
      self.remove()


Settings
--------

You can set the arguments which are passed to ``db_session``
in the ``pony`` section of your settings.

The default settings are:

.. code-block:: python

  @App.setting_section(section='pony')
  def get_pony_settings():
      return {
          'allowed_exceptions': [],
          'immediate': False,
          'retry': 0,
          'retry_exceptions': [TransactionError],
          'serializable': False,
          'strict': False
      }

More information about the arguments you find in the `Pony API documentation`_.

You can also use the ``database`` settings section for your database setup,
which allows you to use different setups for production, development and
testing environments.

Just create create an App for each environment and load specific
settings files:

.. code-block:: python

  class App(PonyApp):
      pass

  with open('settings/default.yml') as defaults:
    defaults_dict = yaml.load(defaults)

  App.init_settings(defaults_dict)


  class ProductionApp(App):
      pass


  with open('settings/production.yml') as settings:
      settings_dict = yaml.load(settings)

  ProductionApp.init_settings(settings_dict)


  class TestApp(App):
      pass


  with open('settings/test.yml') as settings:
      settings_dict = yaml.load(settings)

  TestApp.init_settings(settings_dict)

The database configuration in the YAML settings
files, depending on the database you use, could
look something like:

.. code-block:: yaml

  database:
    provider: sqlite
    filename: app.db
    create_db: true

In your start script you setup the database and load
the App according to the ``RUN_ENV`` environment variable:

.. code-block:: python

  import os
  import morepath

  from .app import App, ProductionApp, TestApp
  from .model import db


  def setup_db(app):
      db_params = app.settings.database.__dict__.copy()
      db.bind(**db_params)
      db.generate_mapping(create_tables=True)

  def run():
    morepath.autoscan()

    if os.getenv('RUN_ENV') == 'production':
        ProductionApp.commit()
        app = ProductionApp()
    elif os.getenv('RUN_ENV') == 'test':
        TestApp.commit()
        app = TestApp()
    else:
        App.commit()
        app = App()

    setup_db(app)
    morepath.run(app)

Detail about the database configuration you find
in the `PonyOrm documentation`_.


Side effects
------------

If you want to trigger side effects (like sending an email or
writing to filesystem) on database commits you can emit a signal
in the ``@request.after`` of the view which triggers the side effects.

Like this the side effects will be triggered just before the
database session gets committed and only if it wasn't rolled back.

This example uses `more.emit`_:

.. code-block:: python

  @App.json(model=Document, request_method='PUT')
  def document_update(self, request):
      self.update(request.json)

      @request.after
      def after(response):
          request.app.signal.emit('document_updated', self, request)

Altenatively you can use in your model the PonyORM
`after_insert()`_, `after_update()`_ or `after_delete()`_
entity-hooks.
This makes sure that the side effect is triggered
**after** the database session has committed.

The drawback is that you don't have easy access to the
request or app in the model.


.. _Pony: https://ponyorm.com
.. _Pony API documentation:
    https://docs.ponyorm.com/api_reference.html#transactions-db-session
.. _PonyOrm documentation: https://docs.ponyorm.com/api_reference.html#database
.. _more.emit: https://github.com/morepath/more.emit
.. _after_insert(): https://docs.ponyorm.com/api_reference.html#after_insert
.. _after_update(): https://docs.ponyorm.com/api_reference.html#after_update
.. _after_delete(): https://docs.ponyorm.com/api_reference.html#after_delete
