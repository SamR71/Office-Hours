import React from "react";
import MeetingTime from "./MeetingTime";
import InstructorInfo from "./InstructorInfo";
import {withRouter} from "react-router-dom";

/* The SectionModal Component displays information about a CourseSection in a Modal Window.
 * The SectionModal displays information from the Meeting Times and Instructors. 
 */
class SectionModal extends React.Component {
	
	//State holds the name, id, meeting times, and instructors of this section class
	//as well as loggedin, which provides information about what account the user is logged in to...
	state = {
		name: "",
		id: "",
		courseMeetingTimes: [],
		instructors: [],
		loggedin: ""
	};
	
	constructor(props) {
		super(props);
		this.state = {name: props.name,
						id: props.section.sectionID,
						courseMeetingTimes: props.section.courseMeetingTimes,
						instructors: props.instructors};
		this.handleClick = this.handleClick.bind(this);
	}
	
	//Set the loggedin state to represent the account the user is logged in with.
	componentDidMount(){
		var user = localStorage.getItem("loggedinuser");
		this.setState({loggedin: user});
	}

	//Handles Click/Opening/Closing of Modal:
	handleClick(event)
    {
        event.preventDefault();
        /*{this.state.instructors.map(item => (
            InstructorInfo instructor=item
            instructor.addToSchedule()
        ))}*/
    }

    //Main Rendering of SectionModal For All Courses:
    //Contains Applicable Meeting Times, Instructor Data, + InstructorOfficeHours Data
    //As Supplied By Backend.
	render() {
		return (
			<div>
				{/* The button for the modal, labeled by the section number.
					The button will toggle the modal, even though the user typically will
					not be able to access the original button when the modal is open */}
				<a class="btn btn-link"
					data-toggle="modal"
					href={"#sectionModal"+this.state.name+this.state.id}
					role="button"
					aria-expanded="false"
					aria-controls={"#sectionModal"+this.state.name+this.state.id}>
					{" Section #" +this.state.id}
				</a>
				<br></br>
				{/* The Modal itself, labeled again by the section number */}
				<div class="modal fade"
					id={"sectionModal"+this.state.name+this.state.id}
					tabindex="-1"
					role="dialog"
					aria-labelledby={"#sectionModal"+this.state.name+this.state.id}
					aria-hidden="true">
					<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							{/* The Modal Header Content, displaying the course name and section number */}
							<div class="modal-header">
								<h5 class="modal-title" id={"ModalHeader"+this.state.name+this.state.id}>
									{this.state.name}
									<br></br>
									{"Section #" + this.state.id}
								</h5>
								{/* An 'x' button at the top right of the modal to close the modal */}
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>
							{/* The Modal Body Content, displays meeting times and professors with their office hours */}
							<div class="modal-body">
								{/* Display the meeting times for the classes as MeetingTime components,
									mapping each courseMeetingTime to a MeetingTime component with its ID as a key*/}
								{this.state.courseMeetingTimes.map(item => (
									<div key = {item.id}>
										<MeetingTime meeting={item} />
									</div>
								))}
								{/* Display the instructors for the classes as InstructorInfo components,
									mapping each Instructor to an InstructorInfo component with its ID as a key*/}
								{this.state.instructors.map(item => (
									<div key = {item.id}>
										<InstructorInfo instructor={item} courseName={this.state.name}/>
									</div>
								))}
							</div>
							{/* The Modal Footer Content: Holds buttons to interact with the section,
								the first button being to close the modal */}
							<div class="modal-footer">
								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
								{/* <button onClick={this.handleClick} type="button" class="btn btn-primary">Add to Schedule</button> */}
							</div>
						</div>
					</div>
				</div>
				<br></br>
			</div>
		);
	}

}
export default withRouter(SectionModal);
