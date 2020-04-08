import React from 'react';
import SectionModal from "./SectionModal";
import {withRouter} from 'react-router-dom';

/* The CourseDropDown component displays the sections of a course
 * as a drop down menu. When the course is clicked, the dropdown menu
 * is toggled to show every section of the respective course.
 */
class CourseDropDown extends React.Component {
	/* The state holds the name of the Course, as well as two arrays of
	 * the Intructors and CourseSections that belongs to the Course. 
	*/
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
				{/* The DropDown button is labeled as the name of the course 
					and assigned to toggle the collapsable dropdown menu */}
				<a  class="btn btn-link"
					data-toggle="collapse"
					href={"#collapseCourse"+this.state.name}
					role="button" aria-expanded="false"
					aria-controls={"collapseCourse"+this.state.name}>
					{this.state.name}
				</a>
				<br></br>
				{/* The DropDown Content that displays each section of the course.
					Each SectionModal must be given the name of the course as well as
					the CourseSection class itself and the array of instructors. */}
				<div class="collapse" id={"collapseCourse"+this.state.name}>
					<div class="card card-body">
						{	//Each section is mapped to a <div> class with its ID as the key, and mapped to a SectionModal
							this.state.sections.map(item => (
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
