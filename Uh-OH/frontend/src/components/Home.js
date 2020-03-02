import React from "react";
import Schedule from "./Schedule";

class Home extends React.Component
{
    render()
    {

        const homePageStyle =
        {
            margin: "20px"
        };

        return(
            <div style={homePageStyle} class="container-fluid">
                <div class="row justify-content-center">
                    <div class="col-xl-9 mr-5">
                        <h2>My Schedule:</h2>
                        <Schedule />
                        <br></br>
                        <h2>My Courses:</h2>
                        <p>add courses to display here...</p>
                    </div>
                </div>
            </div>
        );
    }
}

export default Home;