import React from "react"
import { Link } from "react-router-dom";
import "./SignIn.css";
import {useHistory} from "react-router-dom";
import { Redirect } from 'react-router';

class SignIn extends React.Component{
	
    constructor(props) {
        super(props);
        this.state = {
            userName: "",
            password: "",
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleClick(event)
    {
        event.preventDefault();
        this.props.handle_login(this.state.userName, this.state.password);
    }

    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        this.setState({ [input]: value })
    }

    render() {
        return(
			<div class="container">
				<div class="row">
					<div class="col-md-5 mx-auto">
						<div class="myform form ">
							<div class="logo mb-3">
								<div class="col-md-12 text-center">
									<h1>Welcome To Uh-OH! Login:</h1>
								</div>
							</div>
							<form action="" method="post" name="login">
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