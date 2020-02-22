import React from 'react';
import logo from './UhOhLogo.png';
import {withRouter} from 'react-router-dom'


class Header extends React.Component
{
    constructor(props)
    {
        super(props);

        this.redirectHome = this.redirectHome.bind(this);
        this.redirectLogIn = this.redirectLogIn.bind(this);
        this.redirectSearch = this.redirectSearch.bind(this);
    }

    redirectHome()
    {
        this.props.history.push('/')
    }

    redirectLogIn()
    {
        this.props.history.push('/LogIn')
    }

    redirectSearch()
    {
        this.props.history.push('/Search')
    }

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
                                   placeholder="Search for your courses..."
                                   aria-label="Search"
                                   onClick={this.redirectSearch}
                                   name="course_search_bar"/>
                            <span class="input-group-append">
                                <button onClick={this.redirectLogIn} class="btn btn-light ml-3" type="button">Log In</button>
                            </span>
                        </div>
                    </form>
                </div>
            </nav> 
        );
    }
}

export default withRouter(Header);