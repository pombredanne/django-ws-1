========
Overview
========

WS is a Business Process Manager for Django. Uses Celery for asynchronous
task automation and ExtJS for web interface.

WS executes :term:`processes <Process>` following previously defined
:term:`workflows <Workflow>`, creating a :term:`tasks <Task>` for each
node, gided by the :term:`transitions <Transition>` between :term:`nodes
<Node>`.

The user responsible for the :term:`task` is automatically chosen from the
:term:`role` defined in the :term:`node`.
