import React from "react";
import {BrowserRouter as Router,Switch, Route} from "react-router-dom";
import Search from "./components/Search";
import Home from "./components/Home";
import Header from "./components/Header";
import LogInApp from "./components/SignIn/SignInApp";

function App()
{
  return (
      <Router>
          <Switch>
              <Route path="/Search">
                  <Header/>
                  <Search/>
              </Route>
              <Route path="/LogIn">
                  <Header/>
                  <LogInApp/>
              </Route>
              <Route path="/">
                  <Header/>
                  <Home/>
              </Route>
          </Switch>
      </Router>
  );
}

export default App;
