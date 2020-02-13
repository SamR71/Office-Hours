import React from 'react';

class Home extends React.Component{
    render() {

        const homePageStyle = {
            margin: "20px",
            fontFamily: "sans-serif",
        }

        return (
            <div style={homePageStyle}>
                <h1>My Schedule:</h1>
                <p>Put schedule component here when done</p>
                <h2>My Courses:</h2>
                <p>add courses to display here...</p>
            </div>
        );
    }
}

export default Home;