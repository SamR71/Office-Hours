import React from "react";
import { Switch, Route} from "react-router-dom";
import SignIn from "./SignIn";
import SignUp from "./SignUp";
import ForgotPassword from "./ForgotPassword";

class SignInApp extends React.Component
{

	render() 
	{
		return(
			<Switch>
				<Route exact path="/LogIn">
					<SignIn handle_login={this.props.handle_login}/>
				</Route>
				<Route path="/LogIn/CreateAccount">
					<SignUp/>
				</Route>
			</Switch>
		)
	}
}

export default SignInApp