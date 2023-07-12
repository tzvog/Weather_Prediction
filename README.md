<!DOCTYPE html>
<html>

<head>
  <title>Tomorrow IO request</title>
</head>

<body>
  <h1>Install Requirements</h1>
  <ol>
  <li>flask</li>
  <li>requests</li>
  </ol>


  <h1>How to work the API</h1>
  <h2>Ideally this was written within an IDE (pycharm) all that is needed to be done make sure the app is within the following structure</h2>
  <pre>
  -- api
      -- model
          -- filter_rule
      -- route
          -- weather_view
      -- schema
          -- config
      -- services
          -- error_handlers
          -- rule_function_aggregation_factory
          -- weather_access
  -- venv
  app
  </pre>

  <h2>To run it either use your IDE and run the app.py page or use the python app.py command in your terminal</h2>

  <h1>Assumptions</h1>
  <ol>
    <li>Access to the token will not be stored locally within a config file. Just for this demo, it has been.</li>
    <li>The same parameter can be filtered many times, e.g., temperature>30 or temperature<30.</li>
    <li>no need to specifically test if an operator appears twice within a rule</li>
  </ol>
</body>

</html>