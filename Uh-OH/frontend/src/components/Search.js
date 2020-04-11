import React from "react";
import queryString from "query-string";
import CourseDropDown from "./CourseDropDown";
import {withRouter} from "react-router-dom";

class Search extends React.Component {
	state =
	{
		courses: [],
		results: false,
		search: "",
	};
	
	async componentDidMount() {
		try {
			//get url to send to backend
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];

			//get response, convert to JSON
			const res = await fetch(url + query);
			const coursesjson = await res.json();

			//set state
			this.setState({
				courses: coursesjson
			});

			//updating the flag for if there are results yet
			this.setState({
				results: this.state.courses.length !== 0
			});

			//storing what was searched
			this.setState({
				search: query
			});
		}
		 catch(e){
			console.log(e);
		}
	}
	
	render()
	{
		if(this.state.results)
		{
			return(
				<div>
					{/* Display each course as a drop down */}
					{this.state.courses.map(item => (
						<div key={item.id}>
							<CourseDropDown course={item} loggedin={this.props.loggedin}/>
						</div>
					))}
				</div>
			);
		}
		else
		{
			return(
				<div style={{paddingLeft: "50px"}}>
					<br/><br/><br/>
					<h4>
						No results found for: {this.state.search} <br/> <br/>
						Search for:
						<li>Course Names</li>
						<li>CRNs</li>
						<li>Course Numbers</li>
					</h4>
				</div>
			);
		}
	}
}
export default withRouter(Search);
