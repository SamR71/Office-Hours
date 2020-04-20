import React, { Component } from "react";
import {BrowserRouter as Router,Switch, Route} from "react-router-dom";
import Search from "./components/Search";
import Home from "./components/Home";
import Header from "./components/Header";
import LogInApp from "./components/SignIn/SignInApp";
import LogOutApp from "./components/SignOut/SignOutApp";

/*
The App React Component = Key React Component That
Routes The User To The Various Pages As Desired.
*/
class App extends Component
{
	//State Stores loggedin = Name of Current User.
	constructor(props) {
		super(props);
		this.state = {
			loggedIn: ''
		};
		
		this.handle_login = this.handle_login.bind(this);
		this.handle_logout = this.handle_logout.bind(this);
	}
	
	//Main Driver Function That Handles User Login.
	//Makes API Calls To Django Backend Login Application.
	handle_login (username, password) {
        //Sends POST Request To Backend Requesting To Log User Into Uh-OH!
		var url = 'http://localhost:8000/login/loginuser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
        	//Case 1: Login Successful
            if (xhr.readyState == XMLHttpRequest.DONE) {
				if(xhr.status == 200){
                    alert("Successfully Logged In!");
                    //Store Login Token Return By Backend = Name of Logged In User.
					this.setState({loggedIn: xhr.responseText});
                    localStorage.setItem('loggedinuser', xhr.responseText);
                    //Redirect User Now To Homepage.
					window.location.href = "/"
				} 
				//Case 2: User Login Failed + Display Error Message.
				else{
					alert(xhr.responseText);
				}
            }
        }.bind(this);
        //Send Appropriate Form Data To Backend.
        xhr.open('POST', url)
        const form = new FormData()
        form.set('username', username)
        form.set('password', password)
        xhr.send(form)
	}
	
	//Main LogOut Functionality. 
	//Similar To Login w/ Backend API Calls Through POST Request.
	handle_logout (username) {
        //Send POST Request To Backend Requesting User To Log Out Via Django Authentication.
		var url = 'http://localhost:8000/login/logoutuser/';
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
        	//Case 1: Sucessfully Logged Out.
            if (xhr.readyState == XMLHttpRequest.DONE) {
				if(xhr.status == 200){
                    alert("Successfully Logged Out!");
                    // Store login token returned by the backend
					this.setState({loggedIn: xhr.responseText});
                    localStorage.setItem('loggedinuser', xhr.responseText);
                    // Redirect to homepage
					window.location.href = "/"
				}
				//Case 2: Failed Logged Out (i.e., User Was Never Logged In?) 
				//Display Returned Error Message From Backend
				else{
					alert(xhr.responseText);
				}
            }
        }.bind(this);
        //Send Appropriate Form Data:
        xhr.open('POST', url)
        const form = new FormData()
        form.set('username', username)
        xhr.send(form)
	}

	//Main Rendering of Uh-OH! Applicaton.
	//Routes User To Correct Pages As Indicated Below.
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
					  <Route path="/LogOut"> 
						  <Header/>
						  <LogOutApp handle_logout={this.handle_logout}/> 
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
