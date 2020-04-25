import React from "react";
import "./SignIn.css";

/*
The ForgotPassword Component Represents The Component
That Will Be Triggered In The Case The User Forgets Their Password
+ Desires To Reset Its Value.
*/
class ForgotPassword extends React.Component
{

	//State Stores Email Address of Current User.
	constructor(props)
	{
		super(props);
		this.state = {
			email: ""
		};
		this.handleClick = this.handleClick.bind(this);
		this.handleChange = this.handleChange.bind(this);
	}

	//Click Leads Back To Login Page After Change To Password.
	handleClick()
	{
		this.props.history.push("/LogIn");
	}

	//Handles Changes In Any State Variables Via Reseting/Update To Password.
	handleChange(event)
	{
		const input = event.target.name;
		const value = event.target.value;
		//Adjusts State Values For Email Appropriately.
		this.setState({ [input]: value })
	}

	render()
	{
		return(
			<div className="password">
				<form>
					<label htmlFor="email"><b>E-mail: </b></label>
					<input type="text" onChange={this.handleChange} placeholder="Enter Email Address" name="email" required />
					<br/>
					<button className="signinbutton" onClick={this.handleClick}>Reset Password</button>
				</form>
			</div>
		)
	}
}

export default ForgotPassword