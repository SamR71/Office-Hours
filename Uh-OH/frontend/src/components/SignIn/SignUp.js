import React from "react"
import "./SignIn.css"

class SignUp extends React.Component{

    constructor(props)
    {
        super(props);
        this.state =
        {
            fullName: "",
            email: "",
            password: "",
            repeatPassword: ""
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

    render(){
        return(
            <div className="signup">
                <form>
                    <label htmlFor="fullName"><b>Full Name: </b></label>
                    <input type="text" onChange={this.handleChange} placeholder="Full Name" name="fullName" required />
                    <br/>
                    <label htmlFor="email"><b>Email address: </b></label>
                    <input type="text" onChange={this.handleChange} placeholder="Email address" name="email" required />
                    <br/>
                    <label htmlFor="password"><b>Password: </b></label>
                    <input type="password" onChange={this.handleChange} placeholder="password" name="password" required />
                    <br/>
                    <label htmlFor="repeatPassword"><b>Renter Password: </b></label>
                    <input type="password" onChange={this.handleChange} placeholder="password" name="repeatPassword" required />
                    <br/>
                    <button className="signinbutton" onClick={this.handleClick}>Sign-up</button>
                </form>
            </div>
        )
    }
}

export default SignUp