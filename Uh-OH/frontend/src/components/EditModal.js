import React from "react";
import {withRouter} from "react-router-dom";

/* The EditModal Component Displays Office Hours Data Pertinent 
 * To Currently Logged In User. 
 */
class EditModal extends React.Component {
	
	
	//State Holds All Data For The Desired Office Hour To Be Updated
	// + All The New Data To Be Updated w/ For The Office Hour
	// + Other Relevant Data Such As Currently Logged In User.
	state = {
		name: "",
		instructorType: "",
		instructor: "",
		instructorID: "",
		type: "",
		place: "",
		newplace: "",
		day: "",
		newday: "",
		start: "",
		newstart: "",
		end: "",
		newend: "",
		id: "",
		strrep: "",
		loggedin: ""
	};
	
	//Constructor That Creates Edit Modal Based On Properties Passed In.
	constructor(props) {
		super(props);
		this.state = {name: props.hour.course,
						instructorType: props.hour.instructorType,
						instructor: props.hour.instructor,
						instructorID: props.hour.instructorID,
						type: props.hour.type,
						place: props.hour.place,
						newplace: props.hour.place,
						day: props.hour.day,
						newday: props.hour.day,
						start: props.hour.start,
						newstart: props.hour.start,
						end: props.hour.end,
						newend: props.hour.end,
						id: props.hour.id,
						strrep: props.hour.strrep};
		//Initialize Calls To Functions.
		this.handleClick = this.handleClick.bind(this);
		this.handleChangeStart = this.handleChangeStart.bind(this);
		this.handleChangeEnd = this.handleChangeEnd.bind(this);
		this.handleChangeDay = this.handleChangeDay.bind(this);
		this.handleChangePlace = this.handleChangePlace.bind(this);
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
		
		//Backend URL For Updating SQLite3 Database Object For Office Hours.
		let url1 = "http://localhost:8000/update/";
		//Backend URL For Updating User Schedules That Contain The Old Office Hours.
		//User Schedules Need To Be Updated To Reflect Changes In Office Hours.
		let url2 = "http://localhost:8000/schedules/update/";
		
		var xhr1 = new XMLHttpRequest();
		var xhr2 = new XMLHttpRequest();
        //Open A POST Request At The Specified URL.
        xhr1.open('POST', url1);
        xhr2.open('POST', url2);
        //Create A Form w/ Appropriate Old Office Hour + New Office Hours Data Padded.
        //Used For Updating Office Hours.
        //Provides Backend w/ Desired OH To Be Updated + New Data To Be Updated.
        const form = new FormData();
        form.set('currentID', this.state.id)
        form.set('currentInstructor', this.state.instructor);
        form.set('oldStartTime', this.state.start);
        form.set('oldEndTime', this.state.end);
        form.set('oldLocation', this.state.place);
        form.set('oldDates', this.state.day);
        form.set('newStartTime', this.state.newstart);
        form.set('newEndTime', this.state.newend);
        form.set('newLocation', this.state.newplace);
        form.set('newDates', this.state.newday);
        form.set('user', this.state.loggedin);
        //Send The Form Data To The POST Request.
        xhr1.send(form);
        xhr2.send(form);

    }
	
	//Reacts To Clicks To Update Start Time.
	handleChangeStart(event) {
		this.setState({newstart: event.target.value});
	}

	//Reacts To Clicks To Update End Time.
	handleChangeEnd(event) {
		this.setState({newend: event.target.value});
	}
	
	//Reacts To Clicks To Update Dates.
	handleChangeDay(event) {
		this.setState({newday: event.target.value});
	}
	
	//Reacts To Clicks To Update Location.
	handleChangePlace(event) {
		this.setState({newplace: event.target.value});
	}
	
    //Main Rendering of EditModal For All Courses:
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
							<h3>{"Start Time: " + this.state.start}</h3>
							{" Edit:  "} 
							<input type="text" value={this.state.newstart} onChange={this.handleChangeStart} />
							<br></br>
							<h3>{"End Time: " + this.state.end}</h3>
							{" Edit:  "} 
							<input type="text" value={this.state.newend} onChange={this.handleChangeEnd} />
							<h3>{"Location: " + this.state.place}</h3>
							{" Edit:  "} 
							<input type="text" value={this.state.newplace} onChange={this.handleChangePlace} />
							<h3>{"Days: " + this.state.day}</h3>
							{" Edit:  "} 
							<input type="text" value={this.state.newday} onChange={this.handleChangeDay} />
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
