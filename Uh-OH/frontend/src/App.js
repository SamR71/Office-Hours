import React, { Component } from "react";
import {BrowserRouter as Router,Switch, Route} from "react-router-dom";
import Search from "./components/Search";
import Home from "./components/Home";
import Header from "./components/Header";
import LogInApp from "./components/SignIn/SignInApp";



class App extends Component
{
	
	constructor(props) {
		super(props);
		this.state = {
			loggedin: ''
		};
		
		this.handle_login = this.handle_login.bind(this);
	}
	
	handle_login (username, password) {
		var url = 'http://localhost:8000/login/loginuser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
				
				if(xhr.status == 200){
					alert("User logged in!");
					this.setState({loggedin: xhr.responseText});
					localStorage.setItem('loggedinuser', xhr.responseText);
					window.location.href = "/"
				}else{
					alert(xhr.responseText);
				}
            }
        }.bind(this);
        xhr.open('POST', url)
        const form = new FormData()
        form.set('username', username)
        form.set('password', password)
        xhr.send(form)
	}
	
	render(){
		return (
			  <Router>
				  <Switch>
					  <Route path="/Search">
						  <Header/>
						  <Search loggedin={this.state.loggedin}/>
					  </Route>
					  <Route path="/LogIn">
						  <Header/>
						  <LogInApp handle_login={this.handle_login}/>
					  </Route>
					  <Route path="/">
						  <Header/>
						  <Home/>
					  </Route>
				  </Switch>
			  </Router>
		);
	}
}

export default App;
