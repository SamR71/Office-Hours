import React from 'react';
import queryString from 'query-string';
import CourseDropDown from "./CourseDropDown";
import {withRouter} from 'react-router-dom';

class Search extends React.Component {
	state = {
		courses: []
	};
	
	async componentDidMount() {
		try {
			//get url to send to backend
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];
			
			//get response, convert to JSON
			const res = await fetch(url+query);
			const coursesjson = await res.json();
			
			//set state
			this.setState({
				courses: coursesjson
			});
		} catch (e) {
			console.log(e);
		}
	}
	
	render() {
		return (
			<div>
				{/* Display each course as a drop down */}
				{this.state.courses.map(item => (
					<div key={item.id}>
						<CourseDropDown course = {item} loggedin={this.props.loggedin}/>
					</div>
				))}
			</div>
		);
	}
}
export default withRouter(Search);
