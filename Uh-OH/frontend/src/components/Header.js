import React from 'react';
import logo from './UhOhLogo.png';


class Header extends React.Component{
    render() {

    	const headerStyle = {
		    backgroundColor: "Grey",
		    padding: "5px",
		    display: "block",
	    };

        return (
            <div style={headerStyle}>
            	<img style={{float: "left"}} src={logo} alt="Uh-OH! Logo" height="75" width="75" />
            	<p style={{float: "right"}}>WILL BE SEARCH BAR</p>
            </div>
        );
    }
}

export default Header;