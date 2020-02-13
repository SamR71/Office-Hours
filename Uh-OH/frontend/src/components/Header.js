import React from 'react';
import logo from './UhOhLogo.png';


class Header extends React.Component{
    render() {

    	const headerStyle = {
		    backgroundColor: "Grey",
		    padding: "5px",
			overflow: "hidden",
	    };

    	const logoStyle = {
    	    float: "left",
            display: "block",
            marginLeft: "20px",
        };

    	const searchBarStyle = {
            width: "70%",
            marginTop: "20px",
            marginLeft: "100px",
            padding: "5px",
        };

        const logInStyle = {
            float: "right",
            display: "block",
            marginRight: "50px",
            marginTop: "20px",
        };

        return (
            <div style={headerStyle}>
                <img style={logoStyle} src={logo} alt="Uh-OH! Logo" height="75" width="75" />
                <button style={logInStyle} type="button" className="btn btn-light">Log-In</button>
            	<form>
					<input style={searchBarStyle} type="text" placeholder="Search for your courses ..." name="course search bar" />
				</form>
			</div>
        );
    }
}

export default Header;