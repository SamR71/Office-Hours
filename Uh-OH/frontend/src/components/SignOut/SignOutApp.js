import React from "react";
import { Switch, Route} from "react-router-dom";
import SignOut from "./SignOut";

class SignOutApp extends React.Component{

    render() {
        return(
            <Route exact path="/LogOut">
				<SignOut handle_logout={this.props.handle_logout}/>
			</Route>
        )
    }
}

export default SignOutApp