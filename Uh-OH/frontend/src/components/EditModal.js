import React from "react";
import {withRouter} from "react-router-dom";

/* The SectionModal Component displays information about a CourseSection in a Modal Window.
 * The SectionModal displays information from the Meeting Times and Instructors. 
 */
class EditModal extends React.Component {
	
	//State holds the name, id, meeting times, and instructors of this section class
	//as well as loggedin, which provides information about what account the user is logged in to...
	state = {
		name: "",
		instructorType: "",
		instructor: "",
		instructorID: "",
		type: "",
		place: "",
		day: "",
		start: "",
		end: "",
		id: "",
		strrep: "",
		loggedin: ""
	};
	
	constructor(props) {
		super(props);
		this.state = {name: props.hour.course,
						instructorType: props.hour.instructorType,
						instructor: props.hour.instructor,
						instructorID: props.hour.instructorID,
						type: props.hour.type,
						place: props.hour.place,
						day: props.hour.day,
						start: props.hour.start,
						end: props.hour.end,
						id: props.hour.id,
						strrep: props.hour.strrep};
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
					href={"#editModal"+this.state.name+this.state.id}
					role="button"
					aria-expanded="false"
					aria-controls={"#editModal"+this.state.name+this.state.id}>
					{" " +this.state.strrep}
				</a>
				<br></br>
				{/* The Modal itself, labeled again by the section number */}
				<div class="modal fade"
					id={"editModal"+this.state.name+this.state.id}
					tabindex="-1"
					role="dialog"
					aria-labelledby={"#editModal"+this.state.name+this.state.id}
					aria-hidden="true">
					<div class="modal-dialog modal-dialog-centered" role="document">
						<div class="modal-content">
							{/* The Modal Header Content, displaying the course name and section number */}
							<div class="modal-header">
								<h5 class="modal-title" id={"ModalHeader"+this.state.name+this.state.id}>
									{this.state.name}
									<br></br>
								</h5>
								{/* An 'x' button at the top right of the modal to close the modal */}
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>
							{/* The Modal Body Content, displays meeting times and professors with their office hours */}
							<div class="modal-body">

							</div>
							{/* The Modal Footer Content: Holds buttons to interact with the section,
								the first button being to close the modal */}
							<div class="modal-footer">
								<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
								{<button onClick={this.handleClick} type="button" class="btn btn-primary">Edit Office Hours</button>}
							</div>
						</div>
					</div>
				</div>
				<br></br>
			</div>
		);
	}

}
export default withRouter(EditModal);
