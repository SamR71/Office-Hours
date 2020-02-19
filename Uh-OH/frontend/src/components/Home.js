import React from 'react';
import Schedule from "./Schedule";

class Home extends React.Component
{
    render()
    {

        const homePageStyle =
        {
            margin: "20px",
            fontFamily: "sans-serif",
        };

        return(
            <div style={homePageStyle} class="container">
                <h1>My Schedule:</h1>
                <Schedule />
                <h2>My Courses:</h2>
                <p>add courses to display here...</p>
            </div>
        );
    }
}

export default Home;