Hagalund is a very basic Pyramid + MongoDB app. It is starting as simply the
result of generating an app with the Pyramid/MongoDB scaffolding. Plus this
README of course. Never underestimate the README.

Heroku
======

This app can be deployed to Heroku. The Procfile, requirements.txt and so on are all present. However you will need
to create the app with the Cedar stack (to get Python support):

    heroku create --stack cedar

Additionally, you should provision a (free) MongoLab MongoDB database:

    heroku addons:add mongolab:starter --app niallo-pyramid-test
