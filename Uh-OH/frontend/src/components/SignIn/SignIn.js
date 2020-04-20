import React from "react"
import { Link } from "react-router-dom";
import "./SignIn.css";
import {useHistory} from "react-router-dom";
import { Redirect } from 'react-router';

/*
The SignIn React Component Serves As The Main Component
For Handling The Main Uh-OH! Login Page.
This Component Will Allow Users To Enter Their Login Data.
*/
class SignIn extends React.Component
{
	
	//State Stores Current User's Username + Password.
    constructor(props) {
        super(props);
        this.state = {
            userName: "",
            password: "",
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    //HandleClick Indicates User Has Clicked The Big Login Button.
    handleClick(event)
    {
        event.preventDefault();
        //Invokes Main Driver Handle_Login Function Present In App.js.
        this.props.handle_login(this.state.userName, this.state.password);
    }

    //Handle Change Listens + Adjusts Any of the Username + Password Fields
    //As They Are Entered/Typed Real-Time By User of Uh-OH!
    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        //Adjusts State Values For Username + Password Appropriately.
        this.setState({ [input]: value })
    }

    //Render = Main Display For Sign In Page
    //Includes All Email + Password Fields + Buttons To Login.
    render() 
    {
        return(
			<div class="container">
				<div class="row">
					<div class="col-md-5 mx-auto">
						<div class="myform form ">
							{/*Main Login Header:*/}
							<div class="logo mb-3">
								<div class="col-md-12 text-center">
									<h1>Official Uh-OH! Login</h1>
								</div>
							</div>
							<form action="" method="post" name="login">
								{/*All Form Data Specifiying User Information = Username + Password*/}
								<div class="form-group">
									<label for="exampleInputEmail1">Email Address:</label>
									<input type="email" name="userName"  class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter Email Address" onChange={this.handleChange}/>
								</div>
								<div class="form-group">
									<label for="exampleInputEmail1">Password:</label>
									<input type="password" name="password" id="password"  class="form-control" aria-describedby="emailHelp" placeholder="Enter Password" onChange={this.handleChange}/>
								</div>
								<div class="col-md-12 text-center ">
									<button onClick={this.handleClick} class=" btn btn-block mybtn btn-primary tx-tfm">Login</button>
								</div>
								<div class="col-md-12 ">
									<div class="login-or">
										<hr class="hr-or"/>
									</div>
								</div>
								{/*Unregistered User.*/}
								<div class="form-group">
									<p class="text-center">Don't Have An Uh-OH! Account? <a href="/LogIn/CreateAccount" id="signup">Please Sign Up Here!</a></p>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
        )
    }
}

export default SignIn