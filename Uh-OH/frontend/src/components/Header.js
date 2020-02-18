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

    	const searchBarStyle =
        {
            width: "70%",
            marginTop: "20px",
            marginLeft: "100px",
            padding: "5px",
        };

        const logInStyle =
        {
            float: "right",
            display: "block",
            marginRight: "50px",
            marginTop: "20px",
        };

        return (
            <div style={headerStyle}>
                <img onClick={this.redirectHome} style={logoStyle} src={logo} alt="Uh-OH! Logo" height="75" width="75" />
                <button onClick={this.redirectLogIn} style={logInStyle} type="button" className="btn btn-light">Log-In</button>
            	<form>
					<input onClick={this.redirectSearch}
                           style={searchBarStyle}
                           type="text"
                           placeholder="Search for your courses ..."
                           name="course_search_bar"
                    />
				</form>
			</div>
        );
    }
}

export default withRouter(Header);