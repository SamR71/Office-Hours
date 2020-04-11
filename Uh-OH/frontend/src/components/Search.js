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
	
	// Formats the search query appropriately
	formatSearchQuery(query) {
		// if the query is empty, set it to null
		// check if it is empty by replacing all whitespace with empty chars
		var res = query.replace(/\s/g,'');
		if(res == "")
			query = null;

		// replaces & with %26 to remove the default feature of searching
		// with '&' to allow users to search for classes with '&' in their name
		query = query.replace(/&/g, '%26');
		return query;
	}

	async componentDidMount() {
		try {
			//get url to send to backend
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];

			// format the search query
			query = this.formatSearchQuery(query);

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
				search: this.formatSearchQuery(query)
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
