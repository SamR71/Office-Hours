import React from 'react';
import queryString from 'query-string';
import {withRouter} from 'react-router-dom';

class Search extends React.Component {
    state = {
		courses: []
	};
	
	async componentDidMount() {
		try {
			var url = 'http://localhost:8000/courses/?search=';
			let searchURL = this.props.location.search;
			let params = queryString.parse(searchURL);
			var query = params["course_search_bar"];
			
			console.log(url+query);
			
			const res = await fetch(url+query);
			
			console.log(res);
			const coursesjson = await res.json();
			console.log(coursesjson);
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
				{this.state.courses.map(item => (
					<div key={item.id}>
						<h2>{item.courseName}</h2>
						<br></br>
					</div>
				))}
            </div>
        );
    }
}

export default withRouter(Search);