import React from "react";
import "./SignIn.css";

class forgotPassword extends React.Component{

    constructor(props)
    {
        super(props);
        this.state = {
            email: ""
        };
        this.handleClick = this.handleClick.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleClick()
    {
        this.props.history.push("/LogIn");
    }

    handleChange(event)
    {
        const input = event.target.name;
        const value = event.target.value;
        this.setState({ [input]: value })
    }

    render()
    {
        return(
            <div className="password">
                <form>
                    <label htmlFor="email"><b>E-mail: </b></label>
                    <input type="text" onChange={this.handleChange} placeholder="Enter email" name="email" required />
                    <br/>
                    <button className="signinbutton" onClick={this.handleClick}>Reset Password</button>
                </form>
            </div>
        )
    }
}

export default forgotPassword