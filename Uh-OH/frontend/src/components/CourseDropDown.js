import React from 'react';
import {withRouter} from 'react-router-dom';

class CourseDropDown extends React.Component {
	state = {
		name: "",
		course: "",
		sections: [],
	};
	
	constructor(props) {
		super(props);
		this.state = {name: props.course.courseName, course: props.course, sections: []};
	}

	//async componentDidMount() {
		
	//}

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
						{this.state.name}
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