<body>
  <h1>Install Requirements</h1>
  <ol>
  <li>flask</li>
  <li>requests</li>
  <li>threading</li>
  <li>datetime</li>
  <li>json</li>
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

  <h2>To run it either use your IDE and run the app.py page or 
  in your terminal make sure you are withing the tommorow_io_test directory and 
  use the command "python app.py" and start invoking the API</h2>

  <h1>Assumptions</h1>
  <ol>
    <li>Access to the token will not be stored locally within a config file. Just for this demo, it has been.</li>
    <li>The same parameter can be filtered many times as wanted, e.g., temperature>30 or temperature<30.</li>
    <li> assuming 72 hours from now starts from beginning of the current hour</li>
  </ol>
</body>
