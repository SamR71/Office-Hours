import React from 'react';
import queryString from 'query-string';
import {withRouter} from 'react-router-dom';

class CourseDropDown extends React.Component {
	state = {
		name: "",
		//course: "",
		sections: [],
	};
	
	
	constructor(props) {
		super(props);
		this.state = {name: props.course.courseName, /*course: props.course,*/ sections: props.course.sections/*props.course.getSections()*/};
	}
	
/*
	async componentDidMount() {
		try {
			//get url to send to backend
			var url = 'http://localhost:8000/coursesections/?search=';
			let searchURL = this.props.course;
			let params = queryString.parse(searchURL);
			var query = this.props.course;
			
			//get response, convert to JSON
			const res = await fetch(url+query);
			const sectionsjson = await res.json();
			
			//set state
			this.setState({
				name: this.props.course.name,
				//course: this.props.course,
				sections: sectionsjson
			});
		} catch (e) {
			console.log(e);
		}	
	}
*/
	render() {
		return (
			<div>
				<a class="btn btn-link" data-toggle="collapse" href={"#collapseCourse"+this.state.name} role="button" aria-expanded="false" aria-controls={"collapseCourse"+this.state.name}>
					{this.state.name}
				</a>
				<br></br>
				<div class="collapse" id={"collapseCourse"+this.state.name}>
					<div class="card card-body">
						{/*this.state.course.map(item => (
							<div key={item.id}>
								<CourseDropDown course = {item} />
							</div>
						))*/}

						{/*this.props.course.coursesection_set.all().map(item => (
							<div key={item.id}>
								<CourseDropDown course = {item} />
							</div>
						))*/}
						{this.state.sections.map(item => (
							<div key={item.id}>
								<h2>{item.id}</h2>
								<br></br>
							</div>
						))}
						{/*this.state.name*/}
					</div>
				</div>
			</div>
		);
	}

}
export default withRouter(CourseDropDown);

/**
	<div>
		<a class="btn btn-link" data-toggle="collapse" href={"#collapseCourse"+item.courseName} role="button" aria-expanded="false" aria-controls={"collapseCourse"+item.courseName}>
			{item.courseName}
		</a>
		<br></br>
		<div class="collapse" id={"collapseCourse"+item.courseName}>
			<div class="card card-body">
				{item.courseName}
			</div>
	</div>
*/