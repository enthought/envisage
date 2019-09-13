Glossary
========

Application
  The thing that plugins plugin to!

Extension Point
  A well defined place where new functionality and/or data can be contributed
  to an application.

Extension (aka Contribution)
  An *actual* piece of functionality or data that is contributed (this is why
  extensions are often known as contributions). Think of 'extension points' as
  the 'where' and 'extensions' as the 'what'.

Extension Registry
  The place where (by default) all of the extension points and their associated
  extensions are stored.

Service
  In Envisage, a service is *any* object that a developer thinks is
  sufficiently useful to want to share it.

Service Registry
  The 'yellow pages' style mechanism that is used to publish and look up
  services.

Plugin
  The mechanism for delivering new functionality to an application. A plugin
  can do 3 simple things:

  1) offer extension points
  2) make contributions to extension points (including its own)
  3) create and publish services

Plugin Manager
  Finds, starts, and manages the plugins that make up an application.
