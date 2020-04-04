import React from 'react';
import SectionModal from "./SectionModal";
import {withRouter} from 'react-router-dom';

class CourseDropDown extends React.Component {
	state = {
		name: "",
		sections: [],
		instructors: [],
	};
	
	
	constructor(props) {
		super(props);
		this.state = {name: props.course.courseName, sections: props.course.sections, instructors: props.course.instructors};
	}
	
	render() {
		return (
			<div>
				{/* The DropDown button labeled as the name of the course */}
				<a  class="btn btn-link"
					data-toggle="collapse"
					href={"#collapseCourse"+this.state.name}
					role="button" aria-expanded="false"
					aria-controls={"collapseCourse"+this.state.name}>
					{this.state.name}
				</a>
				<br></br>
				{/* The DropDown Content that displays each section of the course */}
				<div class="collapse" id={"collapseCourse"+this.state.name}>
					<div class="card card-body">
						{this.state.sections.map(item => (
							<div key={item.id}>
								<SectionModal name={this.state.name} section={item} instructors={this.state.instructors} loggedin={this.props.loggedin}/>
							</div>
						))}
					</div>
				</div>
			</div>
		);
	}

}
export default withRouter(CourseDropDown);
