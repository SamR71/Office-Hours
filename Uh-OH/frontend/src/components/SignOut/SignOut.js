import React from "react"
import { Link } from "react-router-dom";
import {useHistory} from "react-router-dom";
import { Redirect } from 'react-router';

/*
The SignOut React Component Serves As The Main Component
For Handling The Main Uh-OH! Logout Page.
This Component Will Allow Users To Enter Their Login Data.
*/
class SignOut extends React.Component{
	
	//State Stores Current User's Username To Be Logged Out.
    constructor(props) {
        super(props);
        this.state = {
            userName: localStorage.getItem("loggedinuser"),
        };
        this.handleClick = this.handleClick.bind(this);
    }

    //HandleClick Indicates User Has Clicked The Big Logout Button.
    handleClick(event)
    {
        event.preventDefault();
        this.props.handle_logout(this.state.userName);
    }

    //Render = Main Display For Sign Out Page
    //Prompts User To Logout By Clicking Button.
    render() {
        return(
			<div class="container">
				<div class="row">
					<div class="col-md-5 mx-auto">
						<div class="myform form ">
							<div class="logo mb-3">
								<div class="col-md-12 text-center">
									<h1>Hello {this.state.userName}, Would You Like To Logout?</h1>
								</div>
								<div class="col-md-12 text-center">
									Click The Button Below To Sign Out From Uh-OH!
								</div>
								<div class="col-md-12 text-center ">
									<button onClick={this.handleClick} class=" btn btn-block mybtn btn-primary tx-tfm">Logout</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
        )
    }
}

export default SignOut
