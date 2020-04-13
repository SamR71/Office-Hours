import React from "react";
import logo from "./UhOhLogo.png";
import {withRouter} from "react-router-dom";

//The Header Component Serves As The Top Toolbar For Uh-OH!
//This Component Illustrates Our Logo + Any/All Login Buttons + Search Bars.

class Header extends React.Component
{
    constructor(props)
    {
        super(props);

        //Currently Supported Redirections Based On User Navigation:
        this.redirectHome = this.redirectHome.bind(this);
        this.redirectLogIn = this.redirectLogIn.bind(this);
        this.redirectSearch = this.redirectSearch.bind(this);

        //State Only Stores The Value Of The Currently Logged In User.
        //Case 1: User Logged In => Button Displays User's Username.
        //Case 2: Not Logged In => Button Displays Log In Which Prompts User To Join/Log In w/ Uh-OH!
        this.state = {
            displayLogInButton: localStorage.getItem("loggedinuser") != "" ? localStorage.getItem("loggedinuser") : "Log In",
        }
    }

    //Redirects User Back To Homepaage.
    redirectHome()
    {
        this.props.history.push("/")
    }

    //Redirects User Back To Login Or Logout Page 
    //Based On Whether They Are Logged In Or Not.
    redirectLogIn(currentButtonValue)
    {
        //Case 1: User Not Logged In.
        if(currentButtonValue == "Log In"){
            this.props.history.push("/LogIn")
        }
        //Case 2: User Logged In + Clicked Button.
        else{
            this.props.history.push("/LogOut");
        }
    }

    //Redirect To Search Page Based On User Clicking Search Bar.
    redirectSearch()
    {
        this.props.history.push("/Search")
    }

    //Main Render Function That Handles/Invokes Above Redirections Based On User Input.
    render()
    {
        const headerStyle =
        {
            backgroundColor: "Grey",
            padding: "5px",
            overflow: "hidden",
        };

        const logoStyle =
        {
            float: "left",
            display: "block",
            marginLeft: "20px",
            href: "/",
        };

        return (
             <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style={headerStyle}>
                <a class="navbar-brand" href="">
                    <img onClick={this.redirectHome} style={logoStyle} src={logo} alt="Uh-OH! Logo" height="75" width="75" />
                </a>
                <button class="navbar-toggler"
                        type="button"
                        data-toggle="collapse"
                        data-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="navbar-collapse collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                    
                    </ul>
                    <form class="mx-2 my-auto d-inline w-100">
                        <div class="input-group">
                            <input class="form-control"
                                   type="search"
                                   placeholder="Search For Your Courses..."
                                   aria-label="Search"
                                   onClick={this.redirectSearch}
                                   name="course_search_bar"/>
                            <span class="input-group-append">
                                <button onClick={() => this.redirectLogIn(this.state.displayLogInButton)} className="btn btn-light ml-3" type="button">{this.state.displayLogInButton}</button>;
                            </span>
                        </div>
                    </form>
                </div>
            </nav> 
        );
    }
}

export default withRouter(Header);