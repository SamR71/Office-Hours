import React from "react";
import queryString from "query-string";
import CourseDropDown from "./CourseDropDown";
import {withRouter} from "react-router-dom";

/*
The Search React Component = Main Component For User's Searching Class + Office Hours.
*/
class Search extends React.Component {
	//State Stores Courses, If Data Found, + Search Query Entered By User. 
	state =
	{
		courses: [],
		results: false,
		search: "",
	};
	
	//Helper Function:
	//Formats Search Query Appropriately.
	formatSearchQuery(query) {
		//If the query is empty, set it to null.
		//Checks if it is empty by replacing all whitespace with empty characters.
		var res = query.replace(/\s/g,'');
		if(res == "")
			query = null;

		//Replaces & with %26 to remove the default feature of searching
		//with '&' to allow users to search for classes with '&' in their name.
		query = query.replace(/&/g, '%26');
		return query;
	}

	async componentDidMount() {
		try {
			//Get URL To Send To Backend For Search API Calls.
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];

			//Format Search Query.
			query = this.formatSearchQuery(query);

			//Get Response + Convert To JSON.
			const res = await fetch(url + query);
			const coursesJson = await res.json();

			//Set State For Courses Found.
			this.setState({
				courses: coursesJson
			});

			//Update Flag For If There Are Results Yet.
			this.setState({
				results: this.state.courses.length !== 0
			});

			//Store What Was Searched By User.
			this.setState({
				search: this.formatSearchQuery(query)
			});
		}
		 catch(e){
			console.log(e);
		}
	}
	
	//Main Rendering For Search Results:
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
						No Results Found For: {this.state.search} <br/> <br/>
						Search For:
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
